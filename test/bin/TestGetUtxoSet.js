var chai = require('chai');  
var assert = chai.assert;

const fs = require('fs');

const cmd = require('./cmd');

describe('CLI: get_utxo_set', function() {

    it('should print the correct testnet output @integration-ledger', async function() {
        
        let oldTestnetAddress = "n1a44regv5cocoqDgEBtCvf8P6SjDqKyFP";
        let utxoFile = "./test/vectors/n1a44regv5cocoqDgEBtCvf8P6SjDqKyFP_utxos.json";
        let expectedOutput = fs.readFileSync(utxoFile, 'utf8');
        
        const response = await cmd.execute(
            'bin/get_utxo_set.js',
            [oldTestnetAddress, '--testnet']
        );
        assert.equal(response,expectedOutput);
    });

    it('should print the correct mainnet output @integration-ledger', async function() {
        
        let oldMainnetAddress = "1JfbZRwdDHKZmuiZgYArJZhcuuzuw2HuMu";
        let utxoFile = "./test/vectors/1JfbZRwdDHKZmuiZgYArJZhcuuzuw2HuMu_utxos.json";
        let expectedOutput = fs.readFileSync(utxoFile, 'utf8');
        
        const response = await cmd.execute(
            'bin/get_utxo_set.js',
            [oldMainnetAddress]
        );
        assert.equal(response,expectedOutput);
    });
    
});
