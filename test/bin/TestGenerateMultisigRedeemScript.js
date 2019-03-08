var chai = require('chai');  
var assert = chai.assert;

const cmd = require('./cmd');

describe('CLI: generate_multisig_redeem_script', function() {

    it('should print the correct output', async function() {
        let pubkey1="026c76fc386b6c339577eea265242eb902df43155a0eaf23af1f96c5d9f2d10f63";
        let pubkey2="0329b59270b95c8478fa36e0cf6f474736513d4e0157626b762dca41729e7756c2";
        let pubkey3="02b5b79489d0e3810ef911bfde82aad7d65e6d5fb4147686139d291f66eefd964d";

        const response = await cmd.execute(
            'bin/generate_multisig_redeem_script.js',
            [pubkey1, pubkey2, pubkey3]
        );
        assert.equal(response,
                     "5221026c76fc386b6c339577eea265242eb902df43155a0eaf23af1f96c5d9f2d10f63210329b59270b95c8478fa36e0cf6f474736513d4e0157626b762dca41729e7756c22102b5b79489d0e3810ef911bfde82aad7d65e6d5fb4147686139d291f66eefd964d53ae\n"
                    );
    });
});

