#!/usr/bin/env python

import sys
import argparse

from typing import List

from bitcoin.core import x, script


def generate_multisig_redeem_script(pubkeys: List[str], m: int) -> str:
    """
    Creates a M-of-N P2SH-multisig bitcoin redeemscript

    Args:
        pubkeys: List of hex-encoded compressed public keys

    Returns:
        hex-encoded redeem script

    Example:
        TODO
    """ 
    OP_M = script.CScriptOp.encode_op_n(m)
    OP_N = script.CScriptOp.encode_op_n(len(pubkeys))
    redeem_list = [x(pubkey) for pubkey in pubkeys]
    redeem_list.insert(0, OP_M)
    redeem_list.append(OP_N)
    redeem_list.append(script.OP_CHECKMULTISIG)
    redeem_script = script.CScript(redeem_list).hex()
    return redeem_script


def generate_2of3_redeem_script(pubkeys: List[str]) -> str:

    if len(pubkeys) != 3:
        raise ValueError("3 Public Keys Required")
    
    return generate_multisig_redeem_script(pubkeys, 2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate 2-of-3 P2SH-multisig Bitcoin Redeem Script from Public Keys')
    parser.add_argument('pubkeys',
                        nargs=3,
                        help="Three Compressed Public Keys")

    args = parser.parse_args()

    print(generate_2of3_redeem_script(args.pubkeys))
