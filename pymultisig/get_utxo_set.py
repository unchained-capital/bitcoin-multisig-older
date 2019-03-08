#!/usr/bin/env python


import sys
import argparse
import json
import requests

from typing import List

import blockchain.blockexplorer as BlockExplorer
import blockchain.util as util


def get_utxo_set(address: str, testnet: bool = False) -> List[str]:
    """
    Retrieves UTXO (unspent transaction outputs) for a given address
    This is used to determine output amounts and fees.
    UTXOs are pulled from online block explorers

    Args:
        address: bitcoin address in Base58Check encoding (standard address format)
        testnet: Is the address on testnet or mainnet?

    Returns:
        List of Output Dict objects with txid, n, and amount keys

    Example:
        TODO
    """

    if testnet:
        util.BASE_URL = "https://testnet.blockchain.info/"
    else:
        util.BASE_URL = "https://blockchain.info/"

    transactions = BlockExplorer.get_address(address).transactions
    utxos = []
    for tx in transactions:
        for utxo in tx.outputs:
            if not utxo.spent and utxo.address == address:
                utxos.append({"txid": tx.hash, "n": utxo.n, "amount":utxo.value})


    for utxo in utxos:
        url = util.BASE_URL + "tx/" + utxo['txid'] + "?format=hex"
        res = requests.get(url=url)
        utxo['rawRefTx'] = res.content.decode()
        
    return utxos


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Get available UTXOs for a given bitcoin address')
    parser.add_argument('address',
                        help="Address to spend from")
    parser.add_argument('--testnet',
                        help='set to testnet (true if present)',
                        dest='testnet',
                        action='store_true')

    args = parser.parse_args()

    result = get_utxo_set(args.address, args.testnet)
    print(json.dumps(result, indent=2))
