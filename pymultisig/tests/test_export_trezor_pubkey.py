import pytest

import trezorlib
from trezorlib.exceptions import TrezorFailure


from pymultisig.export_trezor_pubkey import export_trezor_pubkey


class TestExportTrezorPubkey(object):

    def test_no_trezor_raises_error(self):
        with pytest.raises(ConnectionError):
            export_trezor_pubkey("m/45'/1'/0'/0/0")
        

    @pytest.mark.integration
    def test_valid_vectors(self, valid_vectors):
        for vector in valid_vectors:
            path1 = vector['path1']
            path2 = vector['path2']
            path3 = vector['path3']
            pubkey1 = vector['pubkey1']
            pubkey2 = vector['pubkey2']
            pubkey3 = vector['pubkey3']
            assert(export_trezor_pubkey(path1) == pubkey1)
            assert(export_trezor_pubkey(path2) == pubkey2)
            assert(export_trezor_pubkey(path3) == pubkey3)

    @pytest.mark.integration
    def test_invalid_path_raises_error(self):
        with pytest.raises(TrezorFailure):        
            export_trezor_pubkey("m/123345678901234546/0")

    @pytest.mark.integration
    def test_non_numeric_path_raises_error(self):
        with pytest.raises(ValueError):        
            export_trezor_pubkey("m/asdf/0")
            
    
