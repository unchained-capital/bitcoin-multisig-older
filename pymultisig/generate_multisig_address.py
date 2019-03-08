#!/usr/bin/env python


import sys
import argparse

from typing import List

import bitcoin
from bitcoin.core import x
from bitcoin.core.script import CScript
from bitcoin.wallet import P2SHBitcoinAddress

def generate_multisig_address(redeemscript: str, testnet: bool = False) -> str:
    """
    Generates a P2SH-multisig Bitcoin address from a redeem script

    Args:
        redeemscript: hex-encoded redeem script
                      use generate_multisig_redeem_script to create the redeem script
                      from three compressed public keys
         testnet: Should the address be testnet or mainnet?

    Example:
        TODO
    """

    if testnet:
        bitcoin.SelectParams('testnet')
    else:
        bitcoin.SelectParams('mainnet')

    redeem_script = CScript(x(redeemscript))

    addr = P2SHBitcoinAddress.from_redeemScript(redeem_script)

    return str(addr)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate Bitcoin P2SH-multisig address from redeem script')
    parser.add_argument('redeemscript',
                        help="Redeem Script, use generate_multisig_redeem_script")
    parser.add_argument('--testnet',
                        help='set to testnet (true if present)',
                        dest='testnet',
                        action='store_true')

    args = parser.parse_args()

    print(generate_multisig_address(args.redeemscript, testnet=args.testnet))
