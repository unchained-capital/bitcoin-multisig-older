#!/usr/bin/env node

const BigNumber = require('bignumber.js');
const JSONbig = require('json-bigint');
const fs = require('fs');

var { finalizeOutputs } = require('../src/utils/bitcoin/transactions.js')

// Is it simple to allow for more than two outputs?
if (require.main === module) {
    var program = require('commander');
    
    program
        .version('0.1.0','-v, --version')
        .arguments('<address> <inputsFile>')
        .option('--amount <amount>', 'Amount (in BTC) to send to address, required if change_address is given')
        .option('--change_address <change_address>', 'Address to send remaining BTC to after sending amount to address')
        .option('--set_fees <n>', 'Fees in Sat/Byte, defaults to 15 Sat/Byte', parseInt)
        .action(function(address, inputsFile, options) {
            // default fees
            if (!options.set_fees) {
                options.set_fees = 15
            }
            let result = generate_outputs(address,
                                          inputsFile,
                                          options.change_address,
                                          options.amount,
                                          options.set_fees);
            console.log(JSONbig.stringify(result, null, 2));
        })
        .parse(process.argv);
}

function generate_outputs(address, inputsFile, changeAddress, amount, setFees) {
    let fixedOutputs = [];
    let remainingAddress;

    // Load UTXO set
    var utxos = JSONbig.parse(fs.readFileSync(inputsFile, 'utf8'));
    
    // Convert output amount to satoshis
    // and assign remainingAddress and fixedOutputs
    if (amount) {
        amount = new BigNumber(amount).shiftedBy(8);
        fixedOutputs.push({"address": address,"amount": amount});
        remainingAddress = changeAddress;
    } else {
        remainingAddress = address;
    }

    return finalizeOutputs(remainingAddress, utxos, fixedOutputs, setFees);
}
