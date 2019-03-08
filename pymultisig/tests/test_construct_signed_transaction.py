import pytest

from pymultisig.construct_signed_transaction import construct_signed_transaction


class TestConstructSignedTransaction(object):

    def test_valid_vectors(self, valid_vectors):
        for vector in valid_vectors:
            result = construct_signed_transaction(vector['redeem_script'],
                                                  vector['broadcast_sigfiles'],
                                                  vector['inputs_file'],
                                                  vector['outputs_file'],
                                                  testnet=vector['testnet'])
            expected = vector['broadcast_tx']
            assert(result == expected)

    def test_valid_vectors_reordered_sigs(self, valid_vectors):
        for vector in valid_vectors:
            sigfiles = vector['broadcast_sigfiles'][::-1]
            result = construct_signed_transaction(vector['redeem_script'],
                                                  sigfiles,
                                                  vector['inputs_file'],
                                                  vector['outputs_file'],
                                                  testnet=vector['testnet'])
            expected = vector['broadcast_tx']
            assert(result == expected)
            

            
    def test_one_sig_file_raises_error(self, valid_vectors):
        with pytest.raises(ValueError):
            vector = valid_vectors[0]
            result = construct_signed_transaction(vector['redeem_script'],
                                                  vector['sig1_file'],
                                                  vector['inputs_file'],
                                                  vector['outputs_file'],
                                                  testnet=vector['testnet'])


