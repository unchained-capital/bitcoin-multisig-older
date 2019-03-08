#!/usr/bin/env node

require('babel-polyfill');

const JSONbig   = require('json-bigint');
const fs        = require('fs');

const TransportHID = require("@ledgerhq/hw-transport-node-hid").default;
const LedgerBtc = require("@ledgerhq/hw-app-btc").default;

var { signMultisigSpendLedger } = require('../src/utils/bitcoin/ledger');


if (require.main === module) {
    var program = require('commander');

    program
        .version('0.1.0','-v, --version')
        .arguments('<path> <address> <redeemScript> <inputsFile> <outputsFile>')
        .option('--testnet', 'Generate Testnet Address (boolean)')
        .action(async function(path, address, redeemScript, inputsFile, outputsFile, options) {
            if (!options.testnet) {
                options.testnet = false;
            }

            let result = await sign_multisig_spend(path,
                                                   address,
                                                   redeemScript,
                                                   inputsFile,
                                                   outputsFile,
                                                   options.testnet);
            console.log(JSONbig.stringify(result, null, 2));
        })
        .parse(process.argv);
}

async function sign_multisig_spend(path,
                                   address,
                                   redeemScript,
                                   inputsFile,
                                   outputsFile,
                                   testnet) {

    var inputs = JSONbig.parse(fs.readFileSync(inputsFile, 'utf8'));    
    var outputs = JSONbig.parse(fs.readFileSync(outputsFile, 'utf8'));

    const transport = await TransportHID.create();
    const ledgerbtc = new LedgerBtc(transport);            
    
    return  signMultisigSpendLedger(path,
                                    address,
                                    redeemScript,
                                    inputs,
                                    outputs,
                                    testnet,
                                    ledgerbtc);

}
