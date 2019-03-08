var chai = require('chai');  
var assert = chai.assert;

const fs = require('fs');

const cmd = require('./cmd');

describe('CLI: sign_multisig_spend', function() {

    it('should print the correct testnet output @integration-ledger', async function() {
        this.timeout(20000);
        let path1 = "m/45'/1'/502'/200/26";
        let path2 = "m/45'/1'/501'/200/26";        
        
        let inputsFile = "./test/vectors/inputs.json";
        let outputsFile = "./test/vectors/outputs.json";
        let sigFile1 = "./test/vectors/sig1.json";
        let sigFile2 = "./test/vectors/sig2.json";        

        let multisigAddress = "2NAy762TReQqjNbNLdh3sK7cnje4GA4UfoW";
        let redeemScript = "5221026c76fc386b6c339577eea265242eb902df43155a0eaf23af1f96c5d9f2d10f63210329b59270b95c8478fa36e0cf6f474736513d4e0157626b762dca41729e7756c22102b5b79489d0e3810ef911bfde82aad7d65e6d5fb4147686139d291f66eefd964d53ae";
        
        let expectedOutput1 = fs.readFileSync(sigFile1, 'utf8');
        let expectedOutput2 = fs.readFileSync(sigFile2, 'utf8');        
        
        const response1 = await cmd.execute(
            'bin/sign_multisig_spend.js',
            [path1,
             multisigAddress,
             redeemScript,
             inputsFile,
             outputsFile,
             '--testnet']
        );
        const response2 = await cmd.execute(
            'bin/sign_multisig_spend.js',
            [path2,
             multisigAddress,
             redeemScript,
             inputsFile,
             outputsFile,
             '--testnet']
        );        
        assert.equal(response1, expectedOutput1);
        assert.equal(response2, expectedOutput2);
    });
});
