from pymultisig.generate_outputs import generate_outputs

class TestGenerateOutputs(object):

    def test_vector1_one_output(self):
        result = generate_outputs("2NCcmVAirNBDTQYvecdDpKNJVdKJruwdUSZ",
                                  "pymultisig/tests/fixtures/vector1_inputs.json")
        expected = [{'address': '2NCcmVAirNBDTQYvecdDpKNJVdKJruwdUSZ',
                     'amount': 20985975}]
        assert(result == expected)

    def test_vector1_one_output_set_fees(self):
        result = generate_outputs("2NCcmVAirNBDTQYvecdDpKNJVdKJruwdUSZ",
                                  "pymultisig/tests/fixtures/vector1_inputs.json",
                                  set_fees=30)
        expected = [{'address': '2NCcmVAirNBDTQYvecdDpKNJVdKJruwdUSZ',
                     'amount': 20971950}]
        assert(result == expected)
        
    def test_vector1_two_outputs(self):
        result = generate_outputs("2NCcmVAirNBDTQYvecdDpKNJVdKJruwdUSZ",
                                  "pymultisig/tests/fixtures/vector1_inputs.json",
                                  "2MyvsR5gizb6JHSECL6csBHwpW1wL8xqHp4",
                                  "0.1")
        expected = [{'address': '2NCcmVAirNBDTQYvecdDpKNJVdKJruwdUSZ',
                     'amount': 10000000},
                    {'address': '2MyvsR5gizb6JHSECL6csBHwpW1wL8xqHp4',
                     'amount': 10985465}]
        assert(result == expected)

    def test_vector1_two_outputs_set_fees(self):
        result = generate_outputs("2NCcmVAirNBDTQYvecdDpKNJVdKJruwdUSZ",
                                  "pymultisig/tests/fixtures/vector1_inputs.json",
                                  "2MyvsR5gizb6JHSECL6csBHwpW1wL8xqHp4",
                                  "0.1",
                                  set_fees=30)
        expected = [{'address': '2NCcmVAirNBDTQYvecdDpKNJVdKJruwdUSZ',
                     'amount': 10000000},
                    {'address': '2MyvsR5gizb6JHSECL6csBHwpW1wL8xqHp4',
                     'amount': 10970930}]
        assert(result == expected)

    def test_vector1_two_outputs_full_precision(self):
        result = generate_outputs("2NCcmVAirNBDTQYvecdDpKNJVdKJruwdUSZ",
                                  "pymultisig/tests/fixtures/vector1_inputs.json",
                                  "2MyvsR5gizb6JHSECL6csBHwpW1wL8xqHp4",
                                  "0.12345678")
        expected = [{'address': '2NCcmVAirNBDTQYvecdDpKNJVdKJruwdUSZ',
                     'amount': 12345678},
                    {'address': '2MyvsR5gizb6JHSECL6csBHwpW1wL8xqHp4',
                     'amount': 8639787}]
        assert(result == expected)
        
