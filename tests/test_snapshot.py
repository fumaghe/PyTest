import pytest

def test_pubchem_snapshot(snapshot):
    mock_data = {
        "IdentifierList": {
            "CID": [12345]
        }
    }
    # Salva lo snapshot o confronta con lo snapshot esistente
    snapshot.assert_match(mock_data, 'pubchem_snapshot')
