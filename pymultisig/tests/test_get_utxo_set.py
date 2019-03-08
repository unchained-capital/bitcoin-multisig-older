import json

import pytest

from unittest.mock import patch

from pymultisig.get_utxo_set import get_utxo_set

class TestGetUTXOSet(object):

    @patch('pymultisig.get_utxo_set.BlockExplorer.get_address')
    def test_valid_vectors(self, mock_get_address, explorer_output, valid_vectors):
        mock_get_address.return_value = explorer_output
        result = get_utxo_set("2NAy762TReQqjNbNLdh3sK7cnje4GA4UfoW", True)
        with open(valid_vectors[0]['inputs_file'], 'r') as f:
            expected = json.load(f)
        assert(result == expected)

    @pytest.mark.integration
    def test_block389_testnet(self, explorer_old_outputs):
        result = get_utxo_set("n1a44regv5cocoqDgEBtCvf8P6SjDqKyFP", True)
        expected = explorer_old_outputs["testnet_n1a44regv5cocoqDgEBtCvf8P6SjDqKyFP"]
        assert(result == expected)

        
    @pytest.mark.integration
    def test_block5_mainnet(self, explorer_old_outputs):
        result = get_utxo_set("1JfbZRwdDHKZmuiZgYArJZhcuuzuw2HuMu")
        expected = explorer_old_outputs["mainnet_1JfbZRwdDHKZmuiZgYArJZhcuuzuw2HuMu"]
        assert(result == expected)

