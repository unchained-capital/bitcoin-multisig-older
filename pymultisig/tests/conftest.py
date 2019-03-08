import json
import pickle

import pytest

@pytest.fixture()
def valid_vectors():
    with open("pymultisig/tests/fixtures/valid_vectors.json", 'r') as f:
        vectors = json.load(f)
    return vectors


@pytest.fixture()
def explorer_output():
    with open('pymultisig/tests/fixtures/explorer_output.pkl', 'rb') as input:
        return pickle.load(input)

@pytest.fixture()
def explorer_old_outputs():
    with open('pymultisig/tests/fixtures/explorer_old_outputs.json', 'r') as f:
        vectors = json.load(f)
    return vectors
    
