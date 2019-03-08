# Unchained Capital - Bitcoin Multisig Transaction Signing Scripts

The included scripts are sufficient to author and
sign transactions independent of the Unchained Capital platform.

Scripts are included to sign with the Trezor One and Ledger Nano S
hardware wallets. Other wallets have not been tested and probably will
not work.

## Requirements

### Trezor Signing

1. Python 3
2. [Pipenv]
3. [Trezor One]

Whenever you are executing a python script, make sure you are in the
virtual environment provided by `pipenv shell`

### Ledger Signing

1. [node.js]
2. [Ledger Nano S]

## Installation

To install dependencies for both Trezor and Ledger Signing:

```
make dev-dependencies
```

## Testing

### Trezor

#### Unit Tests

1. Unplug all hardware wallets.
2. If not already there, enter the virtual environment with `pipenv shell`

```
make python-test
```

#### Integration Tests

1. Plug in a Trezor initialized with these wallet words:
```
merge alley   lucky   axis penalty manage latin   gasp  virus    captain wheel deal
chase fragile chapter boss zero    dirt   stadium tooth physical valve   kid   plunge
```
2. If not already there, enter the virtual environment with `pipenv shell`

```
make python-test-integration
```

Be prepared to press `confirm` many times on your device.


To run the unit and integration tests together, unplug you hardware wallet and
run

```
make python-test-full
```

This will display complete coverage information.

### Ledger

#### Unit Tests

1. Unplug all hardware wallets.

```
make js-test
```

#### Integration Tests

1. Plug in a Ledger with the following wallet words (same as above) and
open the Bitcoin Ledger app.
```
merge alley   lucky   axis penalty manage latin   gasp  virus    captain wheel deal
chase fragile chapter boss zero    dirt   stadium tooth physical valve   kid   plunge
```

```
make js-test-integration
```

## Examples

Examples of the full set of command line scripts are available in
[examples/run_all_trezor.sh] and [examples/run_allledger.sh].

If you are starting from a funded multisig vault and corresponding information,
examples are provided in [examples/spend_only_trezor.sh] and
[examples/spend_only_ledger.sh]. Both signers need identical input and output
files, so either confirm they are the same, or have one signer pass their files
to the other signer.

## Use

The steps are the same for both Trezor and Ledger:

1. Modify the template at either [template/template_trezor.sh] or
[template/template_ledger.sh]
2. Enter the BIP32 For the key you control
3. Enter the amount you are sending (in BTC) to the output address
4. Enter the Output address
5. Enter the Change address (the remaining balance less fees will be sent here)
6. Enter files names
  a. If you have the signature file for the other signer, make sure
  the filename matches the location and name of that file
7. Enter your Redeem Script
8. Enter your Multisig Address (the one you are spending from)
9. Remove the `--testnet` flag if you are constructing a mainnet transaction
9. Plug in and unlock your hardware wallet
10. Execute the script, and confirm the information presented on the wallet
11. The raw transaction will be printed to the terminal

[pipenv]: https://pipenv.readthedocs.io/en/latest/
[trezor one]: https://shop.trezor.io/product/trezor-one-white
[node.js]: https://nodejs.org/en/
[ledger nano s]: https://www.ledger.com/products/ledger-nano-s
