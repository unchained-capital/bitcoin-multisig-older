var chai = require('chai');  
var assert = chai.assert;

const cmd = require('./cmd');

describe('CLI: generate_multisig_address', function() {

    it('should print the correct testnet output', async function() {
        let redeemScript = "5221026c76fc386b6c339577eea265242eb902df43155a0eaf23af1f96c5d9f2d10f63210329b59270b95c8478fa36e0cf6f474736513d4e0157626b762dca41729e7756c22102b5b79489d0e3810ef911bfde82aad7d65e6d5fb4147686139d291f66eefd964d53ae";

        const response = await cmd.execute(
            'bin/generate_multisig_address.js',
            [redeemScript, '--testnet']
        );
        assert.equal(response,"2NAy762TReQqjNbNLdh3sK7cnje4GA4UfoW\n");
    });
});
