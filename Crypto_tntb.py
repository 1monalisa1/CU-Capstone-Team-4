import requests
import json
import os
from dotenv import load_dotenv, find_dotenv

from pathlib import Path
from web3.auto import w3

load_dotenv(find_dotenv())

pinata_api_key = os.environ.get("pinata_api_key")
pinata_secret_api_key = os.environ.get("pinata_secret_api_key")
crypto_address = os.environ.get("crypto_address")

# if we are hardcoding instead of instead of load_dotenv
# crypto_address = "0x53319E332DEC195CC42FeAa0D3B31c2482A24791"

headers = {
    "Content-Type": "application/json",
    "pinata_api_key": pinata_api_key,
    "pinata_secret_api_key": pinata_secret_api_key,
}


def initContract():
    with open(Path("WineRegistry_tntb.json")) as json_file:
        abi = json.load(json_file)

    return w3.eth.contract(address=cryptofax_address, abi=abi)


def convertDataToJSON(time, description):
    data = {
        "pinataOptions": {"cidVersion": 1},
        "pinataContent": {
            "name": "Appraisal Report",
            "description": description,
            "image": "ipfs://bafybeihsecbomd7gbu6qjnvs7jinlxeufujqzuz3ccazmhvkszsjpzzrsu",
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