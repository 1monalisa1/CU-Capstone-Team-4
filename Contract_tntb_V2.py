import requests
import json
import os
from dotenv import load_dotenv, find_dotenv

from pathlib import Path
from web3.auto import w3

load_dotenv(find_dotenv())

pinata_api_key = os.environ.get("pinata_api_key")
pinata_secret_api_key = os.environ.get("pinata_secret_api_key")
# crypto_address = os.environ.get("crypto_address")

# if we are hardcoding instead of instead of load_dotenv
crypto_address = "0x456f89B33eC1Ccec744aF77b61363eb61fAD5b55"

headers = {
    "Content-Type": "application/json",
    "pinata_api_key": pinata_api_key,
    "pinata_secret_api_key": pinata_secret_api_key,
}


def initContract():
    with open(Path("SupplyChain_tntb_V2.json")) as json_file:
        abi = json.load(json_file)

    return w3.eth.contract(address=crypto_address, abi=abi)


def convertDataToJSON(time, new_value):
    data = {
        "pinataOptions": {"cidVersion": 1},
        "pinataContent": {
            "name": "Appraisal Report",
            "new value": new_value,
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