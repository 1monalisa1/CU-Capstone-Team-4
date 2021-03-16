from Contract import convertDataToJSON, pinJSONtoIPFS, initContract, w3
import sys

# access the smart contract through Contract.py using ABI
wineSupplyChain = initContract()

# function to call the RegisterWine function in the smart contract
def callRegisterWine():
    # prompt user inputs of parameters needed for the RegisterWine function
    name = input("Wine Name: ")
    vintage = int(input("Vintage (year of manufacture): "))
    origin = input("Origin (country): ")
    producer = input("Producer name: ")
    initial_value = int(input("Price: "))
    possessor = input("Current owner name: ")
    owner = input("ETH Address of the current owner: ")
    token_uri = input("Token URI: ")

    # call the RegisterWine function
    txn_hash = wineSupplyChain.functions.registerWine(owner, name, vintage, origin, producer, initial_value, possessor, token_uri).transact({"from": w3.eth.accounts[0]})
    txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)
    
    return txn_receipt


# function to call the getWineInfo function in the smart contract
def callGetWineInfo():
    token_id = int(input("Token id: "))
    txn_hash = wineSupplyChain.functions.getWineInfo(token_id).transact({"from": w3.eth.accounts[0]})
    txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)
    wine = wineSupplyChain.functions.rare_wines(token_id).call()
    # the number of entities in a supply chain could increase, so every time a user gets the token info,
    # this function gets the current length of the dynamic array (= number of entities)
    length = wineSupplyChain.functions.getLength(token_id).call()
    owner_chain_list = []
    print("Wine name:", wine[0], "\nVintage:", wine[1], "\nOrigin:", wine[2], "\nProducer:", wine[3], \
          "\nAppraisal value:", wine[4], "\nCurrent possessor:", wine[6], "\nPossessor's ETH address:", wine[5])
    print("\nChain of the ownership:")
    # print all the entities name in the dynamic array using the length we got by getLength function
    for i in range(length):
        owner_chain_list.append(wineSupplyChain.functions.owner_chains(token_id, i).call())
        print(owner_chain_list[i])


# function to call the registerEntity function in the smart contract
def callRegisterEntity():
    name = input("Name: ")
    entity_address = input("Address: ")
    txn_hash = wineSupplyChain.functions.registerEntity(name, entity_address).transact({"from": w3.eth.accounts[0]})
    txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)
    return txn_receipt


# function to call the getEntityInfo function in the smart contract
def callGetEntityInfo():
    entity_id = int(input("ID: "))
    txn_hash = wineSupplyChain.functions.getEntityInfo(entity_id).transact({"from": w3.eth.accounts[0]})
    txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)

    return print(txn_hash, txn_receipt)


# function to call the transferOwnership function in the smart contract
def callTransferOwnership(token_id):
    #token_id = int(input("Token ID: "))
    new_owner_id = int(input("New Owner ID: "))
    qualityCheck = bool(input("The wine isn't damaged (true/false): "))
    tamperProof = bool(input("The wine isn't tampered with (true/false): "))
    # w3.eth.accounts[0] points to the first account on Ganache
    # once a token is transferred, the holder of the account does not own the token
    # only the new token owner can call this function to transfer the token to another entity
    # to do so, we need to change w3.eth.accounts[0] to the account of the current owner
    # in the demo, at the second transfer, we changed [0] to [1] because after the first transfer, 
    # the holder of the second account on Ganache became the token holder
    txn_hash = wineSupplyChain.functions.transferOwnership(token_id, new_owner_id, qualityCheck, tamperProof).transact({"from": w3.eth.accounts[0]})
    txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)
    return txn_receipt


# function to call the event ChangeToken to display all transaction records of a token
def callEventChangeToken(token_id):
    transfer_filter = wineSupplyChain.events.ChangeToken.createFilter(
        fromBlock="0x0", argument_filters={"token_num": token_id}
    )
    print("Ownership Chain: The token with token ID " + str(token_id) + " was:")
    transaction_records = transfer_filter.get_all_entries()
    for i in range(len(transaction_records)):
        print('transferred from ' + transaction_records[i]['args']['transferor'] + \
              ' to ' + transaction_records[i]['args']['transferee'] + \
              ' at ' + str(transaction_records[i]['args']['time']) + ' in UNIX time.')
    return ""


# function to create a report of new appraisal as preparation of calling the newAppraisal function in the smart contract
def createAppraisalReport():
    date = input("Date of the appraisal: ")
    new_value = int(input("New Value: "))
    token_id = int(input("Token ID: "))
    json_data = convertDataToJSON(date, new_value)
    report_uri = pinJSONtoIPFS(json_data)
    return token_id, new_value, report_uri


# function to call the newAppraisal function in the smart contract
def callNewAppraisal(token_id, new_value, report_uri):
    txn_hash = wineSupplyChain.functions.newAppraisal(token_id, new_value, report_uri).transact({"from": w3.eth.accounts[0]})
    txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)
    return txn_receipt

# function to call the event Appraisal
def callEventAppraisal(token_id):
    appraisal_filter = wineSupplyChain.events.Appraisal.createFilter(
        fromBlock="0x0", argument_filters={"token_id": token_id}
    )
    return appraisal_filter.get_all_entries()


def main():
    # terminal command to issue a new token
    if sys.argv[1] == "register_wine":
        registration_receipt = callRegisterWine()
        print(registration_receipt)

    # terminal command to get the latest information of the token
    elif sys.argv[1] == "wine_info":
        callGetWineInfo()

    # terminal command to register entities involved in a wine supply chain
    elif sys.argv[1] == "register_entity":
        entity_receipt = callRegisterEntity()
        print(entity_receipt)

    # terminal command to get the information of an entity
    elif sys.argv[1] == "entity_info":
        callGetEntityInfo()

    # terminal command to transfer a token to a new entity
    elif sys.argv[1] == "transfer_ownership":
        token_id = int(sys.argv[2])
        transfer_receipt = callTransferOwnership(token_id)
        print(transfer_receipt)

    # terminal command to get the transaction history of a token
    elif sys.argv[1] == "ownership_chain":
        token_id = int(sys.argv[2])
        reports = callEventChangeToken(token_id)
        print(reports)

    # terminal command to reevaluate a value of wine
    elif sys.argv[1] == "appraisal_report":
        token_id, new_value, report_uri = createAppraisalReport()
        receipt = callNewAppraisal(token_id, new_value, report_uri)
        print(receipt)
        print("Report URI:", report_uri)

    # terminal command to get the latest value of a token
    elif sys.argv[1] == "get_appraisal_report":
        token_id = int(sys.argv[2])
        wine = wineSupplyChain.functions.rare_wines(token_id).call()
        reports = callEventAppraisal(token_id)
        print(reports)
        print("Wine is:", wine[0], " Owner is:", wine[6], " Appraised value:", wine[4])


main()