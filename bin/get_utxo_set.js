#!/usr/bin/env node

const JSONbig = require('json-bigint');

var program = require('commander');

var { getUtxoSet } = require('../src/utils/bitcoin/blockexplorer.js')

if (require.main === module) {
    program
        .version('0.1.0','-v, --version')
        .arguments('<address>')
        .option('--testnet', 'set to testnet (true if present)')
        .action(async function(address, options) {
            let result = await getUtxoSet(address, options.testnet);
            console.log(JSONbig.stringify(result, null, 2));
        })
        .parse(process.argv);
}
