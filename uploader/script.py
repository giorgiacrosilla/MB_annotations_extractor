import os
import rdflib
import configparser

PREFIXES = [
("crmdig", "<http://www.ics.forth.gr/isl/CRMdig/>"),
("crminfluence", "<http://www.cidoc-crm.org/cidoc-crm/influence/>"),
("oa", "<http://www.w3.org/ns/oa#>"),
("crmsci", "<http://www.ics.forth.gr/isl/CRMsci/>"),
("Help", "<http://help.researchspace.org/resource/>"),
("bds", "<http://www.bigdata.com/rdf/search#>"),
("crmba", "<http://www.cidoc-crm.org/cidoc-crm/CRMba/>"),
("prov", "<http://www.w3.org/ns/prov#>"),
("xsd", "<http://www.w3.org/2001/XMLSchema#>"),
("mbdiaries-annotation", "<https://mbdiaries.itatti.harvard.edu/annotation/>"),
("rdfs", "<http://www.w3.org/2000/01/rdf-schema#>"),
("iiif", "<http://iiif.io/api/>"),
("crm", "<http://www.cidoc-crm.org/cidoc-crm/>"),
("sim", "<http://purl.org/ontology/similarity/>"),
("fc", "<https://collection.itatti.harvard.edu/resource/custom/fc/>"),
("rdf", "<http://www.w3.org/1999/02/22-rdf-syntax-ns#>"),
("User", "<http://www.researchspace.org/resource/user/>"),
("mbdiaries-type", "<https://mbdiaries.itatti.harvard.edu/resource/type/>"),
("forms", "<http://www.researchspace.org/resource/system/forms/>"),
("owl", "<http://www.w3.org/2002/07/owl#>"),
("rshelp", "<http://researchspace.org/help/>"),
("sp", "<http://spinrdf.org/sp#>"),
("Platform", "<http://www.researchspace.org/resource/system/>"),
("mbdiaries", "<https://mbdiaries.itatti.harvard.edu/resource/>"),
("fr", "<https://collection.itatti.harvard.edu/resource/custom/fr/>"),
("crmgeo", "<http://www.ics.forth.gr/isl/CRMgeo/>"),
("skos", "<http://www.w3.org/2004/02/skos/core#>"),
("mbdiaries_forms", "<http://mbdiaries.itatti.harvard.edu/resource/forms>"),
("schema", "<http://schema.org/>"),
("rso", "<http://www.researchspace.org/ontology/>"),
("Admin", "<http://www.researchspace.org/resource/admin/>"),
("vitiiif", "<https://iiif.itatti.harvard.edu/iiif/2/>"),
("ontodia", "<http://ontodia.org/schema/v1#>"),
("frbroo", "<http://iflastandards.info/ns/fr/frbr/frbroo/>"),
("crmarchaeo", "<http://www.cidoc-crm.org/cidoc-crm/CRMarchaeo/>"),
("rsp", "<http://www.researchspace.org/resource/>"),
("Default", "<https://collection.itatti.harvard.edu/resource/>"),
("mbdiaries-document", "<https://mbdiaries.itatti.harvard.edu/document/>"),
("mbdiaries-ontology", "<https://mbdiaries.itatti.harvard.edu/ontology/>"),
("ldp", "<http://www.w3.org/ns/ldp#>")
]

def _get_credentials(t="mb_diaries"):
  """
  Retrieves the credentials for a specific type from a configuration file.

  Parameters:
  type (str): The type of credentials to retrieve.

  Returns:
  dict: A dictionary containing the username, password, and endpoint for the specified type.
  """
  config = configparser.ConfigParser()
  try:
    path = os.path.join(os.path.dirname(__file__), 'config.ini')
    config.read(path)

    return {
        "username": config.get(t, "username"),
        "password": config.get(t, "password"),
        "endpoint": config.get(t, "endpoint")
    }

  except Exception as ex:
    print('Error. Have you created the config.ini file? see readme.md')

def prepend_prefixes(file_path):
    """
    Prepends the prefixes to a .trig file using rdflib.

    Parameters:
    file_path (str): The path to the .trig file.

    Returns:
    None
    """
    new_content = ''
    with open(file_path, 'r', encoding='utf-8') as file:
      content = file.read()
      
      if "@prefix" not in content:
        for prefix in PREFIXES:
          new_content += f'@prefix {prefix[0]}: {prefix[1]} .\n'
      
        new_content = f'{new_content}\n{content}'
      file.close()
      
    with open(file_path, 'w', encoding='utf-8') as file:
      file.write(new_content)
      file.close()

def upload_trig_file(file):
    """
    Uploads all .trig files in a specified folder and subfolders to a specified endpoint.

    Parameters:
    input_path (str): The path containing .trig files to upload.
    diary (str): The identifier for the diary context.
    config (dict): A dictionary containing the configuration for the upload.

    Returns:
    None
    """
    credentials = _get_credentials()

    print(f'\nUploading file: {file}')
    upload_endpoint = f'{credentials["endpoint"]}ldp-container'

    # DELETE existing graph
    #delete_response = _del(upload_endpoint, credentials)
    #print(f'DELETE Response: {delete_response}')

    command = f'curl -u {credentials["username"]}:{credentials["password"]} -X POST -H \'Content-Type: application/trig\' --data-binary \'@{filename}\' {upload_endpoint}'
    print(f'POST\t{os.system(command)}')

if __name__ == "__main__":

    rdf_output_folder = os.path.join(os.path.dirname(__file__), os.pardir, 'test')

    # Define paths and configurations
    diary = "example_diary"  # Replace with your diary identifier

    for file in os.listdir(rdf_output_folder):
      filename = os.path.join(rdf_output_folder, file)
      prepend_prefixes(filename)
      upload_trig_file(filename)
    