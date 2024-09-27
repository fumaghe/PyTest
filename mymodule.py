import requests
import io
from bs4 import BeautifulSoup
import logging
import jsonschema

# Funzione per estrarre il primo link di status da CIR
def extract_first_status_link(session, url):
    try:
        response = session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        status_links = soup.find('table').find_all('a')
        if not status_links:
            return None
        first_link = "https://cir-reports.cir-safety.org/" + status_links[0]['href'].replace("../", "")
        return first_link
    except requests.RequestException as e:
        logging.error(f"Error retrieving status link from CIR: {e}")
        return None

# Funzione per processare un ingrediente e ottenere il PDF CIR
def get_pdf_for_ingredient(session, ingredient_id):
    url = f"https://cir-reports.cir-safety.org/cir-ingredient-status-report/?id={ingredient_id}"
    pdf_link = extract_first_status_link(session, url)
    if pdf_link:
        response = session.get(pdf_link)
        if response.status_code == 200:
            return io.BytesIO(response.content)
    return None

# Funzione per ottenere il CID di un ingrediente da PubChem
def get_pubchem_cid(session, ingredient_name):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{ingredient_name}/cids/JSON"
    try:
        response = session.get(url)
        response.raise_for_status()
        data = response.json()
        return str(data['IdentifierList']['CID'][0])
    except (requests.RequestException, KeyError, IndexError, ValueError) as e:
        logging.error(f"Error retrieving PubChem CID for {ingredient_name}: {e}")
        return None

# Funzione per validare un JSON con uno schema
def validate_json_schema(data, schema):
    try:
        jsonschema.validate(instance=data, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as e:
        logging.error(f"JSON Schema validation error: {e}")
        return False
