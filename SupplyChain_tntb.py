from Crypto_tntb import convertDataToJSON, pinJSONtoIPFS, initContract, w3
import sys

wine_registry = initContract()

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

    elif sys.argv[1] == "get":
        token_id = int(sys.argv[2])
        wine = wine_registry.functions.rare_wines(token_id).call()
        reports = callEventAppraisal(token_id)

        print(reports)
        print("Wine is:", wine[0], " Owner is:", wine[4], " Appraised value:", wine[2])


main()