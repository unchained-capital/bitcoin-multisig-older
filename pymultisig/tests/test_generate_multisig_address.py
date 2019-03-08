import pytest

import binascii

from pymultisig.generate_multisig_address import generate_multisig_address


class TestGenerateMultisigAddress(object):

    def test_testnet(self, valid_vectors):
        for vector in valid_vectors:
            redeem_script = vector['redeem_script']
            expected_address = vector['testnet_address']
            result = generate_multisig_address(redeem_script, True)
            assert(result == expected_address)

    def test_mainnet(self, valid_vectors):
        for vector in valid_vectors:
            redeem_script = vector['redeem_script']
            expected_address = vector['mainnet_address']
            result = generate_multisig_address(redeem_script)
            assert(result == expected_address)

    def test_invalid_hex_raises_error(self):
        with pytest.raises(binascii.Error):
            result = generate_multisig_address("deadbeefz")
        with pytest.raises(binascii.Error):
            result = generate_multisig_address("deadbeefzz")

            
