#!/usr/bin/env python


import sys
import argparse
import json

from typing import List
from decimal import Decimal

try:
    from pymultisig.btc_utils import estimate_transaction_fees
except ModuleNotFoundError:
    from btc_utils import estimate_transaction_fees

def generate_outputs(address: str,
                     inputs: str = None,
                     change_address: str = None,
                     amount: str = None,
                     set_fees: int = 15) -> dict:
    """
    Generate Output data for use in signing and tranasction construction
    One or Two output options.
    With One output, fees are removed from the one output,
    With two outputs, fees are removed from the change address output.
    Defaults to 15 sat/byte, but is optionally settable

    Args:

    Returns:

    Example:
        TODO
    """

    # Calculate total input amount (satoshis)    
    with open(inputs, 'r') as f:
        utxos = json.load(f)    

    total_amount = 0
    for utxo in utxos:
        total_amount += utxo['amount']

    # Convert from BTC to Satoshis
    if amount is not None:
        amount = int(Decimal(amount) * 10 ** 8)

    # Calculate Fees
    if change_address is not None:
        num_outputs = 2
    else:
        num_outputs = 1

    fee_amount = estimate_transaction_fees(len(utxos), num_outputs, set_fees)
    
    # Set change amount    
    if change_address is not None:
        change_amount = total_amount - amount - fee_amount
    else:
        amount = total_amount - fee_amount

    # Construct main output
    outputs = []
    outputs.append({"address": address,
                    "amount": amount})
    

    # Optionally, construct second output
    if change_address is not None:
        outputs.append({"address": change_address,
                        "amount": change_amount})

    return outputs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate Bitcoin Redeem Script from Public Keys ')
    
    parser.add_argument('address',
                        help="Address to Send to, defaults to all if change_address is not given")
    parser.add_argument('inputs',
                        help="inputs json file (see get_utxo_set.py)")
    parser.add_argument('--change_address',
                        help="Address to send remaining BTC to after sending amount to address")    
    parser.add_argument('--amount',
                        help="Amount (in BTC) to send to address, required if change_address is given")
    parser.add_argument('--set_fees',
                        type=int,
                        help="Fees in Sat/Byte, defaults to 15 Sat/Byte")    

    args = parser.parse_args()

    if args.set_fees is None:
        set_fees = 15
    else:
        set_fees = args.set_fees
    
    result = generate_outputs(args.address,
                              args.inputs,                              
                              args.change_address,
                              args.amount,
                              set_fees)
    print(json.dumps(result, indent=2))

