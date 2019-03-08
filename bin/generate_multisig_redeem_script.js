#!/usr/bin/env node

var program = require('commander');

var { generateMultisigRedeemScript } = require('../src/utils/bitcoin/btc_utils.js')

if (require.main === module) {
    program
        .version('0.1.0','-v, --version')
        .arguments('<pubkey1> <pubkey2> <pubkey3>')
        .action(function(pubkey1, pubkey2, pubkey3) {
            let result = generateMultisigRedeemScript(pubkey1, pubkey2, pubkey3);
            console.log(result);
        })
        .parse(process.argv);
}
