import json

import pytest

from pymultisig.sign_multisig_spend import sign_tx

class TestSignTx(object):

    def test_incorrect_address_raises_error(self, valid_vectors):
        vector = valid_vectors[0]
        with pytest.raises(ValueError):
            result = sign_tx(vector['path1'],
                             vector['mainnet_address'],
                             vector['redeem_script'],
                             vector['inputs_file'],
                             vector['outputs_file'],
                             testnet=vector['testnet'])


    
    @pytest.mark.integration    
    def test_valid_vectors(self, valid_vectors):
        for vector in valid_vectors:
            
            if (vector['testnet']):
                address = vector['testnet_address']
            else:
                address = vector['mainnet_address']
                
            result = sign_tx(vector['path1'],
                             address,
                             vector['redeem_script'],
                             vector['inputs_file'],
                             vector['outputs_file'],
                             testnet=vector['testnet'])
            with open(vector['sig1_file'], 'r') as f:
                expected_sig = json.load(f)
            assert(result == expected_sig)
            result = sign_tx(vector['path2'],
                             address,
                             vector['redeem_script'],
                             vector['inputs_file'],
                             vector['outputs_file'],
                             testnet=vector['testnet'])
            with open(vector['sig2_file'], 'r') as f:
                expected_sig = json.load(f)
            assert(result == expected_sig)
            result = sign_tx(vector['path3'],
                             address,
                             vector['redeem_script'],
                             vector['inputs_file'],
                             vector['outputs_file'],
                             testnet=vector['testnet'])
            with open(vector['sig3_file'], 'r') as f:
                expected_sig = json.load(f)
            assert(result == expected_sig)

