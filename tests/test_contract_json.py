import pytest
from tests.mymodule import get_pubchem_cid, validate_json_schema

pubchem_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "IdentifierList": {
            "type": "object",
            "properties": {
                "CID": {
                    "type": "array",
                    "items": {
                        "type": "number"
                    }
                }
            },
            "required": ["CID"]
        }
    },
    "required": ["IdentifierList"]
}

@pytest.fixture
def mock_pubchem_data():
    return {
        "IdentifierList": {
            "CID": [12345]
        }
    }

def test_pubchem_contract(mock_pubchem_data):
    assert validate_json_schema(mock_pubchem_data, pubchem_schema) == True
