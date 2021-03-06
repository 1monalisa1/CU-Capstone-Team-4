import requests
import json
# import os

#from dotenv import load_dotenv
from pathlib import Path
from web3.auto import w3
#  w3 to help communication with our solidity contract on our local blockchain

# load_dotenv()

pinata_api_key =  "70c4f2ba1e0d36d5ab57"

pinata_secret_api_key = "84575d6badd84f9b305d0b82672f0afe0e1cb100bf809f03330bd8092d08fbf0"
cryptofax_address = "0xDD9C20EF9f08B468F87990d5996f58eFd7E27F68"


headers = {
    "Content-Type": "application/json",
    "pinata_api_key": pinata_api_key,
    "pinata_secret_api_key": pinata_secret_api_key
}


def initContract():
    with open(Path("WineRegistry.json")) as json_file:
        abi = json.load(json_file)

    return w3.eth.contract(address=cryptofax_address, abi=abi)

#  using the data 
def convertDataToJSON(time, description):
    data = {
        "pinataOptions": {"cidVersion": 1},
        "pinataContent": {
            "name": "Example Appraisal Report",
            "description": description,
            "image": "ipfs://bafybeig6jj2f6bp2grmuauvdqjds667qsdxc3m6opslxnsnd27egrxdiiq",
            "time": time,
        },
    }
    return json.dumps(data)


def pinJSONtoIPFS(json):
    r = requests.post(
        "https://api.pinata.cloud/pinning/pinJSONToIPFS", data=json, headers=headers
    )
    ipfs_hash = r.json()["IpfsHash"]
    return f"ipfs://{ipfs_hash}"
    #  we need this Ipfs hash for our report_uri
    #  the return fn will take the hipfs hash and append it to ipfs://

    
