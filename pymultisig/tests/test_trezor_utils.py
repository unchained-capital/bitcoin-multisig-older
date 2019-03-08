import pytest

import trezorlib

from pymultisig import trezor_utils


class TestGetTrezorClient(object):

    def test_no_trezor_raises_connection_error(self):
        with pytest.raises(ConnectionError):
            client = trezor_utils.get_trezor_client()            
            
    @pytest.mark.integration
    def test_returns_client(self):
        client = trezor_utils.get_trezor_client()
        assert isinstance(client, trezorlib.client.TrezorClient)

        

