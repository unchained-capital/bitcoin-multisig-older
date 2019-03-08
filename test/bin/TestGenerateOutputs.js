var chai = require('chai');  
var assert = chai.assert;

const fs = require('fs');

const cmd = require('./cmd');

describe('CLI: generate_outputs', function() {

    it('should print the correct testnet outputs with change address', async function() {
        let outputamount = 0.1;
        let outputaddress = "2NCcmVAirNBDTQYvecdDpKNJVdKJruwdUSZ";
        let changeaddress = "2MyvsR5gizb6JHSECL6csBHwpW1wL8xqHp4";

        let inputsfile = "./test/vectors/inputs.json";
        
        let outputsFile = "./test/vectors/outputs.json";
        let expectedOutput = fs.readFileSync(outputsFile, 'utf8');

        const response = await cmd.execute(
            'bin/generate_outputs.js',
            [outputaddress,
             inputsfile,
             '--change_address',
             changeaddress,
             '--amount',
             outputamount]
        );
        assert.equal(response, expectedOutput);
    });

    it('should print the correct testnet outputs with single output', async function() {
        assert(false, "TODO: Write Test");
    });
    
    
});
