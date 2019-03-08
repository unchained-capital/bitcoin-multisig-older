#!/usr/bin/env python

import sys
import argparse
import json

try:
    from pymultisig import trezor_utils
    from pymultisig import btc_utils
    from pymultisig.generate_multisig_address import generate_multisig_address
except ModuleNotFoundError:
    import trezor_utils
    import btc_utils
    from generate_multisig_address import generate_multisig_address


import trezorlib
from trezorlib import messages as proto
from trezorlib import btc as trezorbtc


def sign_tx(path,
            multisig_address,            
            redeemscript,
            utxo_file,
            output_file,
            testnet=False):
    """
    Sign a spend of a bitcoin 2-of-3 P2SH-multisig address
    using a Trezor One Hardware Wallet

    Args:
        path: BIP32 path of key with which to sign
        multisig_address: Address that is being spent
        redeemscript: redeem script corresponding to multisig_address
        utxo_file: JSON file of UTXOs for multisig_address
                   (see get_utxo_set.py)
        output_file: JSON file of destination addresses and amounts
                     (see generate_outputs.py)
        testnet: Is this a testnet or mainnet address?

    Returns:
        Dictionary with two keys:
        pubkey: public key corresponding to the private key used for signing
        signatures: a list of signatures, one per utxo

    Raises:
        ValueError: If multisig_address is not correct for the given redeemscript

    Example:
       TODO
    """

    with open(utxo_file, 'r') as f:
        utxos = json.load(f)

    with open(output_file, 'r') as f:
        outputs = json.load(f)
        
    # Verify that Pubkeys and Address match
    check_address = generate_multisig_address(redeemscript, testnet)
    parsed_redeem_script = btc_utils.parse_redeem_script(redeemscript)

    if multisig_address != check_address:
        raise ValueError("Incorrect Redeem Script")

    if testnet:
        coin = 'Testnet'
    else:
        coin = 'Bitcoin'


    input_script_type = proto.InputScriptType.SPENDMULTISIG
    output_script_type = proto.OutputScriptType.PAYTOADDRESS

    tx_api = trezorlib.coins.tx_api[coin]
    client = trezor_utils.get_trezor_client()
    #client.set_tx_api(tx_api)


    # Get signing node:
    expanded_path = trezorlib.tools.parse_path(path)
    signer = trezorbtc.get_public_node(client, expanded_path, show_display=True).node    
    
    # blank HDNodes with public_keys
    nodes = [proto.HDNodePathType(node=proto.HDNodeType(public_key=bytes.fromhex(h),
                                                        depth=0,
                                                        fingerprint=0,
                                                        child_num=0,
                                                        chain_code=b'0'*32),
                                  address_n=[]
                                  ) for h in parsed_redeem_script['pubkeys']]
    trezor_inputs = []
    for utxo in utxos:
        multisig = proto.MultisigRedeemScriptType(
            pubkeys=nodes,
            m=parsed_redeem_script['m']
        )

        _input = proto.TxInputType(
            prev_hash=bytes.fromhex(utxo['txid']),
            prev_index=utxo['n'],
            amount=utxo['amount'],
            address_n=trezorlib.tools.parse_path(path),
            script_type=input_script_type,
            multisig=multisig
        )
        trezor_inputs.append(_input)

    txes = {}
    for tx in trezor_inputs:
        tmptx = tx_api[tx.prev_hash]
        txes[tx.prev_hash] = tmptx        

    # make this multi-output, probably from file
    trezor_outputs = []
    for output in outputs:
        trezor_outputs.append(
            proto.TxOutputType(
                address=output['address'],
                amount=output['amount'],
                script_type=output_script_type,
            )
        )

    output_signatures, serialized_tx = trezorbtc.sign_tx(client, coin, trezor_inputs, trezor_outputs, prev_txes=txes)

    signature_blob = {"pubkey": signer.public_key.hex(),
                      "signatures": [s.hex() for s in output_signatures]
                      }
    client.close()

    return signature_blob    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Sign a multisig bitcoin transaction using Trezor One')
    parser.add_argument('path',
                        help="Trezor path, for example: \"m/45'/0'/120'/20/0\"")
    parser.add_argument('address',
                        help='the multisig address')
    parser.add_argument('redeemscript',
                        help="hex-encoded Redeem Script")
    parser.add_argument('utxo_file',
                        help="JSON file containing utxo set")
    parser.add_argument('output_file',
                        help="JSON file containing the address(es) to send to and amounts")
    parser.add_argument('--testnet',
                        help='set to testnet (true if present)',
                        dest='testnet',
                        action='store_true')

    args = parser.parse_args()

    sigs = sign_tx(args.path,
                   args.address,                   
                   args.redeemscript,
                   args.utxo_file,
                   args.output_file,
                   args.testnet)
    
    print(json.dumps(sigs, indent=2))
