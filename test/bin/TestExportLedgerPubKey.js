var chai = require('chai');  
var assert = chai.assert;

const cmd = require('./cmd');

describe('CLI: export_ledger_pubkey', function() {

    it('should print the correct output @integration-ledger', async function() {
    this.timeout(20000);
        const response = await cmd.execute(
            'bin/export_ledger_pubkey.js',
            ["m/45'/1'/500'/200/26"]
        );
        assert.equal(response,
                     "026c76fc386b6c339577eea265242eb902df43155a0eaf23af1f96c5d9f2d10f63\n"
                    );
    });
});

