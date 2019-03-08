#!/usr/bin/env node

var program = require('commander');

var { generateMultisigAddress } = require('../src/utils/bitcoin/btc_utils.js')

if (require.main === module) {
    program
        .version('0.1.0','-v, --version')
        .arguments('<redeemscript>')
        .option('--testnet', 'Generate Testnet Address (boolean)')
        .action(function(redeemscript, options) {
            let result = generateMultisigAddress(redeemscript, options.testnet);
            console.log(result);
        })
        .parse(process.argv);
}
