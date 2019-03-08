import pytest

from pymultisig.btc_utils import (estimate_transaction_fees,
                                  parse_redeem_script)


class TestEstimateTransactionFees(object):

    def test_returns_fees(self):
        assert(estimate_transaction_fees(1, 1, 15) == 5115)
        assert(estimate_transaction_fees(1, 2, 15) == 5625)
        assert(estimate_transaction_fees(1, 3, 15) == 6135)
        assert(estimate_transaction_fees(2, 1, 15) == 9570)
        assert(estimate_transaction_fees(2, 2, 15) == 10080)
        assert(estimate_transaction_fees(2, 3, 15) == 10590)
        assert(estimate_transaction_fees(3, 1, 15) == 14025)
        assert(estimate_transaction_fees(3, 2, 15) == 14535)
        assert(estimate_transaction_fees(3, 3, 15) == 15045)
        assert(estimate_transaction_fees(1, 3, 30) == 12270)
        assert(estimate_transaction_fees(3, 1, 30) == 28050)



class TestParseRedeemScript(object):

    def test_invalid_hex_raises_error(self):
        with pytest.raises(ValueError):
            parse_redeem_script("zzzz")

    def test_invalid_script_raises_error(self):
        with pytest.raises(ValueError):
            parse_redeem_script("deadbeef")
        
    def test_non_2of3_multisig_raises_error(self):
        # 1-of-1 multisig from tx:
        # 7edb32d4ffd7a385b763c7a8e56b6358bcd729e747290624e18acdbe6209fc45
        rs = "5141042f90074d7a5bf30c72cf3a8dfd1381bdbd30407010e878f3"\
             "a11269d5f74a58788505cdca22ea6eab7cfb40dc0e07aba200424a"\
             "b0d79122a653ad0c7ec9896bdf51ae"
        with pytest.raises(ValueError):
            parse_redeem_script(rs)
        
    def test_vectors(self, valid_vectors):
        for vector in valid_vectors:
            result = parse_redeem_script(vector['redeem_script'])
            expected = vector['parsed_redeem_script']
            assert(result == expected)
    
