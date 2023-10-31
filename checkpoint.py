import requests
import json
import time
import chemlab_new as btp
import os

CACHE_FILENAME = "cache.json"
PUBCHEM_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"
PROPERTIES = "/property/MolecularFormula,MolecularWeight,IsomericSMILES,CanonicalSMILES,InChI,InChIKey,IUPACName,RotatableBondCount/JSON"



# checkpoint file where other files methods are being called to get the results and return to the htmlapp or main file!
def open_cache() :
    
    try :
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except :
        cache_dict ={}
    
    return cache_dict


def save_cache(cache_dict) :
    
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME, "w")
    fw.write(dumped_json_cache)
    fw.close()


# def make_request(url) :
    
#     response = requests.get(url)
#     result = json.loads(response.text)

#     return result


# def make_request_with_cache(url) :
    
#     if url in CACHE_DICT.keys():
#         print("using cache...", url)
#         return CACHE_DICT[url]

#     else:
#         print("making request...", url)
#         if "www.drugs.com" not in url :
#             CACHE_DICT[url] = make_request(url)
#         else :
#             response= requests.get(url)
#             CACHE_DICT[url] = response.text
#             save_cache(CACHE_DICT)
#         return CACHE_DICT[url]

def make_request(url):
    response = requests.get(url)
    result = json.loads(response.text)
    return result

def make_request_with_cache(url):
    if url in CACHE_DICT.keys():
        print("Using cache...", url)
        return CACHE_DICT[url]
    else:
        print("Making request...", url)
        CACHE_DICT[url] = make_request(url)
        return CACHE_DICT[url]

# Retrieves all the info using a smile from chemdatafile when passing an argument ingredient
# This function is called from the main html app when a search query is done 
def get_MolFromSmile(ingredient):
    
    Retrieved_Info=[]
    try:
        Retrieved_Info=btp.QueryDB.MolFromSmile("hyd", ingredient)
    except Exception as e:
        print(f"{ingredient} does not exist with the smile representation on the database file!")
    return Retrieved_Info



# Retrieves all the info with the stoichiometric values
# This function is called from the main html app when a checkbox for search with stoichiometric values is checked
def get_MolFromStoichiometry(c_val=5, h_val=4):
    print(c_val,h_val)
    try:
        Mol_List=btp.QueryDB.MolFromStoichiometry('hyd',int(c_val),int(h_val))
        print(Mol_List)
        return Mol_List
    except Exception as e:
        print(f"No molecule exists with the given stoichiometry on the database file!")

# Retrieves the information using pubchem url to get all the information when a name of the molecule is provided
def get_physical_properties(ingredient):
    
    url = PUBCHEM_URL + ingredient + PROPERTIES
    result = make_request_with_cache(url)
    properties = result["PropertyTable"]["Properties"][0]
    
    return properties

from rdkit import Chem
from rdkit.Chem import Draw

def get_rdkit_image(ingredient):
    mol = Chem.MolFromSmiles(ingredient)
    img = Draw.MolToImage(mol)
    return img
    


# to get the picture of a particular molecule from the pubchem page!
def get_molecular_picture(ingredient) :
    

    pic_url = PUBCHEM_URL + ingredient + "/PNG"

    return pic_url


CACHE_DICT = open_cache()

if __name__ == '__main__':
    comp = "benzene"
    properties = get_physical_properties(comp) if comp is not None else None

