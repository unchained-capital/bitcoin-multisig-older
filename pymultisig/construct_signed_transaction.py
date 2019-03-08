#!/usr/bin/env python


import sys
import argparse
import json

from typing import List

from bitcoin import SelectParams
from bitcoin.core import lx, x, b2x
from bitcoin.core import script
from bitcoin.core.script import SIGHASH_ALL, OP_0
from bitcoin.core import COutPoint, CMutableTxOut, CMutableTxIn, CMutableTransaction
from bitcoin.wallet import CBitcoinAddress

try:
    from pymultisig import btc_utils
    from pymultisig.generate_multisig_address import generate_multisig_address
except ModuleNotFoundError:
    import btc_utils
    from generate_multisig_address import generate_multisig_address


def construct_signed_transaction(redeem_script: str,
                                 sig_files: List[str],
                                 inputs_file: str,
                                 outputs_file: str,
                                 testnet: bool = False) -> str:
    """
    Construct a hex-encoded serialized bitcoin transaction 
    fully-signed and ready for broadcast for a 2-of-3 P2SH-multisig
    address

    Args:
        redeem_script: hex-encoded redeem script (see generate_multisig_redeem_script.py)
        sig_files: List of 2 JSON signature files containing a public key and 
                   signatures for each UTXO (see sign_multisig_spend.py)
        inputs_file: JSON file of UTXOs to be spent (see get_utxo_set.py)
        outputs_file: JSON file of destination addresses (see generate_outputs.py)
        testnet: Is this a testnet or mainnet transaction?

    Returns:
        fully-signed hex-encoded serialized Bitcoin transaction

    Raises:
        ValueError: If sig_files doesn't have exactly 2 elements.

    Example:
        TODO
    """

    if testnet:
        SelectParams('testnet')
    else:
        SelectParams('mainnet')

    # Input validation
    if len(sig_files) != 2:
        raise ValueError("Two Signature Files are Required")

    # load inputs, outputs, and signatures
    with open(inputs_file, 'r') as f:
        inputs = json.load(f)

    with open(outputs_file, 'r') as f:
        outputs = json.load(f)

    signatures = []
    for sig_file in sig_files:
        with open(sig_file, 'r') as f:
            signatures.append(json.load(f))

    # Order Signatures
    parsed_redeem_script = btc_utils.parse_redeem_script(redeem_script)    
    sig1_index = parsed_redeem_script['pubkeys'].index(signatures[0]['pubkey'])
    sig2_index = parsed_redeem_script['pubkeys'].index(signatures[1]['pubkey'])
    if sig2_index < sig1_index:
        signatures = [signatures[1], signatures[0]]

    # Construct ScriptSigs
    zipped_sigs = zip(signatures[0]['signatures'],signatures[1]['signatures'])
    scriptsigs = [script.CScript([OP_0,
                                  x(sig1) + bytes([SIGHASH_ALL]),
                                  x(sig2) + bytes([SIGHASH_ALL]),
                                  x(redeem_script)]
                                 ) for (sig1,sig2) in zipped_sigs]

    # Construct Inputs List
    TxIns = []
    for input in inputs:
        txid = lx(input['txid'])
        vout = input['n']
        TxIns.append(CMutableTxIn(COutPoint(txid, vout)))

    # Insert ScriptSigs        
    for i in range(len(TxIns)):
        TxIns[i].scriptSig = scriptsigs[i]

    # Construct Outputs List
    TxOuts = []
    for output in outputs:
        output_script = CBitcoinAddress(output['address']).to_scriptPubKey()
        TxOuts.append(CMutableTxOut(output['amount'],output_script))

    # Construct TX
    tx = CMutableTransaction(TxIns, TxOuts)

    return b2x(tx.serialize())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Construct fully-signed serialized bitcoin tx ready for broadcast.')
    
    parser.add_argument('redeem_script',
                        help='hex-encoded redeem script')
    parser.add_argument('sig_files',
                        nargs=2,
                        help="Signatures Files")
    parser.add_argument('inputs_file',
                        help='json file of inputs')
    parser.add_argument('outputs_file',
                        help='json file of outputs')
    parser.add_argument('--testnet',
                        help='set to testnet (true if present)',
                        dest='testnet',
                        action='store_true')          

    args = parser.parse_args()

    print(construct_signed_transaction(args.redeem_script,
                                       args.sig_files,
                                       args.inputs_file,
                                       args.outputs_file,
                                       args.testnet))
