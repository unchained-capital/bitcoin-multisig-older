#!/usr/bin/env python

import sys
import argparse

import trezorlib
from trezorlib import btc as trezorbtc

try:
    from pymultisig import trezor_utils
except ModuleNotFoundError:
    import trezor_utils


def export_trezor_pubkey(path: str) -> str:
    """
    Export compressed public key from Trezor One at given BIP32 path

    Args:
        path: BIP32 path string

    Returns: 
        hex-encoded public key

    Example:
        TODO
    """
    client = trezor_utils.get_trezor_client()

    expanded_path = trezorlib.tools.parse_path(path)
    hdnode = trezorbtc.get_public_node(client, expanded_path, show_display=True).node
    pubkey = hdnode.public_key.hex()
    client.close()
    return pubkey



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Export Compressed Public Key' \
                                     'From a Trezor One at a Given BIP32 path')
    parser.add_argument('path', help="Trezor path, for example: \"m/45'/0'/120'/20/0\"")

    args = parser.parse_args()
    print(export_trezor_pubkey(args.path))
