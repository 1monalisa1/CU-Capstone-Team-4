from Contract_tntb import convertDataToJSON, pinJSONtoIPFS, initContract, w3
import sys

wine_registry = initContract()

def callRegisterWineBottle():
    owner = input("Address: ")
    name = input("Wine Name: ")
    producer = input("Producer name: ")
    initial_value = int(input("Price: "))
    possessor = input("Possessor name: ")
    token_uri = input("Token URI: ")

    txn_hash = wine_registry.functions.registerWineBottle(owner, name, producer, initial_value, possessor, token_uri).transact({"from": w3.eth.accounts[0]})
    txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)

    return txn_receipt

def callGetWineInfo():
    token_id = int(input("Token id: "))
    txn_hash = wine_registry.functions.getWineInfo(token_id).transact({"from": w3.eth.accounts[0]})
    txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)
    wine = wine_registry.functions.rare_wines(token_id).call()
    owner_chain = wine_registry.functions.owner_chains(token_id, 0).call()

    return print("Wine Info: ", wine[0:5], "Owner Chain: ", owner_chain[0:])

def callRegisterEntity():
    _name = input("Name: ")
    _entity_address = input("Address: ")
    txn_hash = wine_registry.functions.registerEntity(_name, _entity_address).transact({"from": w3.eth.accounts[0]})
    txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)

    return txn_receipt

def callGetEntityInfo():
    entity_id = int(input("ID: "))
    txn_hash = wine_registry.functions.getEntityInfo(entity_id).transact({"from": w3.eth.accounts[0]})
    txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)
    entity = wine_registry.functions.entities(entity_id).call()

    return print("Entity is: ", entity[0], "Address is: ", entity[1])

def callTransferOwnership():
    token_id = int(input("Token ID: "))
    new_owner_id = int(input("New Owner ID: "))
    txn_hash = wine_registry.functions.transferOwnership(token_id, new_owner_id).transact({"from": w3.eth.accounts[0]})
    txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)

    return txn_receipt


def createAppraisalReport():

    date = input("Date of the appraisal: ")
    new_value = int(input("New Value: "))
    token_id = int(input("Token ID: "))

    json_data = convertDataToJSON(date, new_value)
    report_uri = pinJSONtoIPFS(json_data)

    return token_id, new_value, report_uri

def callNewAppraisal(token_id, new_value, report_uri):
    txn_hash = wine_registry.functions.newAppraisal(token_id, new_value, report_uri).transact({"from": w3.eth.accounts[0]})
    txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)

    return txn_receipt

def callEventAppraisal(token_id):
    appraisal_filter = wine_registry.events.Appraisal.createFilter(
        fromBlock="0x0", argument_filters={"token_id": token_id}
    )
    return appraisal_filter.get_all_entries()
 

def main():
    if sys.argv[1] == "report":
        token_id, new_value, report_uri = createAppraisalReport()
        receipt = callNewAppraisal(token_id, new_value, report_uri)

        print(receipt)
        print("Report URI:", report_uri)

    elif sys.argv[1] == "register_wine":
        # owner, name, producer, initial_value, possessor, token_uri = callRegisterWineBottle()
        registration_receipt = callRegisterWineBottle()
        print(registration_receipt)
    
    elif sys.argv[1] == "info":
        callGetWineInfo()
    
    elif sys.argv[1] == "register_entity":
        entity_receipt = callRegisterEntity()
        print(entity_receipt)

    elif sys.argv[1] == "entity_info":
        callGetEntityInfo()

    elif sys.argv[1] == "transfer_ownership":
        transfer_receipt = callTransferOwnership()
        print(transfer_receipt)

    elif sys.argv[1] == "get":
        token_id = int(sys.argv[2])
        wine = wine_registry.functions.rare_wines(token_id).call()
        reports = callEventAppraisal(token_id)

        print(reports)
        print("Wine is:", wine[0], " Owner is:", wine[4], " Appraised value:", wine[2])


main()