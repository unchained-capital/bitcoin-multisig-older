#!/usr/bin/env node

require('babel-polyfill');

const TransportHID = require("@ledgerhq/hw-transport-node-hid").default;
const LedgerBtc = require("@ledgerhq/hw-app-btc").default;

var program = require('commander');

var { exportLedgerPubKey } = require('../src/utils/bitcoin/ledger');

if (require.main === module) {
    program
        .version('0.1.0','-v, --version')
        .arguments('<path>')
        .action(async function(path) {
            const transport = await TransportHID.create();
            const ledgerbtc = new LedgerBtc(transport);
            let result = await exportLedgerPubKey(path, ledgerbtc);
            console.log(result);
        })
        .parse(process.argv);
}


