
from bitcoin.core import script


def estimate_transaction_fees(num_inputs: int,
                              num_outputs: int,
                              fees_per_byte_in_satoshis: int) -> int:
    """
    Estimate total transaction fee for non-segwit, 2-of-3 P2SH-multisig UTXO spends

    Fee estimation is based of the following encoding assumptions
    10 Overhead bytes:
      version - 4
      input count - 1
      output count - 1
      locktime - 4
    
    297 Bytes per 2/3-multisig utxo:
      prev_tx - 32
      index -4
      scriptsize - 3
      scriptsig - 254
      sequence - 4
    
    34 Bytes per output (conservative assuming P2PKH)

    Args:
        num_inputs: number of UTXOs being spent
        num_outputs: number of outputs
        fees_per_byte_in_satoshis:

    Returns:
        Total transaction fee in satoshis

    Example:
        TODO
    """
    
    tx_length_in_bytes = 10 + (297 * num_inputs) + (34 * num_outputs)

    fees_in_satoshis   = tx_length_in_bytes * fees_per_byte_in_satoshis

    return fees_in_satoshis


def parse_redeem_script(redeemscript: str) -> dict:
    """
    Parses a 2-of-3 P2SH-multisig redeem script

    Args:
        redeemscript: hex-encoded redeem script

    Returns:
        Dictionary with two keys:
            m: M for M-of-N multisig
            pubkeys: three hex-encoded compress public keys

    Raises:
        ValueError: If the redeem script isn't valid 2-of-3 script

    Example:
        TODO
    """
    
    parsed = script.CScript.fromhex(redeemscript)

    parsed_ops = tuple([i if (type(i) == script.CScriptOp or type(i) == int) else type(i) for i in parsed])

    parsed_items = [x for x in parsed]

    multisig_template = (2, bytes, bytes, bytes, 3, script.OP_CHECKMULTISIG)
    
    if parsed_ops != multisig_template:
        raise ValueError("Redeem Script is not Valid 2-of-3 Multisig")
    else:
        return {"m": parsed_items[0],
                "pubkeys": [parsed_items[1].hex(),
                            parsed_items[2].hex(),
                            parsed_items[3].hex()
                            ]
                }
    
