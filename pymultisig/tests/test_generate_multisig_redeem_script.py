import pytest

from pymultisig.generate_multisig_redeem_script import (generate_multisig_redeem_script,
                                                        generate_2of3_redeem_script)


class TestGenerateMultisigRedeemScript(object):

    def test_valid_vectors(self, valid_vectors):
        for vector in valid_vectors:
            pubkeys = [vector['pubkey1'],
                       vector['pubkey2'],
                       vector['pubkey3']]
            redeem_script = vector['redeem_script']
            result = generate_multisig_redeem_script(pubkeys, 2)
            assert(result == redeem_script)

    def test_out_of_order_valid_vectors(self, valid_vectors):
        for vector in valid_vectors:
            pubkeys = [vector['pubkey2'],
                       vector['pubkey1'],
                       vector['pubkey3']]
            redeem_script = vector['redeem_script']
            result = generate_multisig_redeem_script(pubkeys, 2)
            assert(result != redeem_script)
            
class TestGenerate2Of3RedeemScript(object):

    def test_valid_vectors(self, valid_vectors):
        for vector in valid_vectors:
            pubkeys = [vector['pubkey1'],
                       vector['pubkey2'],
                       vector['pubkey3']]
            redeem_script = vector['redeem_script']
            result = generate_2of3_redeem_script(pubkeys)
            assert(result == redeem_script)

    def test_out_of_order_valid_vectors(self, valid_vectors):
        for vector in valid_vectors:
            pubkeys = [vector['pubkey2'],
                       vector['pubkey1'],
                       vector['pubkey3']]
            redeem_script = vector['redeem_script']
            result = generate_2of3_redeem_script(pubkeys)
            assert(result != redeem_script)

    def test_two_pubkeys_is_error(self, valid_vectors):
        with pytest.raises(ValueError):
            for vector in valid_vectors:
                pubkeys = [vector['pubkey2'],
                           vector['pubkey1']]
                result = generate_2of3_redeem_script(pubkeys)

            
