
#  when did the appraisal happen
#  where
#  token_id to associate with the report

from crypto import convertDataToJSON, pinJSONtoIPFS, initContract, w3
import sys

wine_registry = initContract()

def createAppraisalReport():
    time = input("Date of Appraisal: ")
    description = input("New Value: ")
    token_id = int(input("Token ID: "))

    json_data = convertDataToJSON(time, description)
    report_uri = pinJSONtoIPFS(json_data)
    return token_id, report_uri


def reportRegistry(token_id, report_uri):
    # accounts[0] is the first accouht on ganache, so the info is coming fro me the account owner
    tx_hash = wine_registry.functions.reportWineBottle(token_id, report_uri).transact(
    {"from": w3.eth.accounts[0]}
    )
    txn_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return txn_receipt


def getRegistryReports(token_id):
    appraisal_filter = wine_registry.events.Appraisal.createFilter(
        fromBlock="0x0", argument_filters={"token_id": token_id}
    )
    return appraisal_filter.get_all_entries()


# sys.argv is the list of arguments passed from the command line
# sys.argv[0] is always the name of the script
# sys.argv[1] is the first argument, and so on (like here it is the date)
# For example:
#        sys.argv[0]        sys.argv[1]    sys.argv[2]
# python appraisal.py        report
# python appraisal.py        get            1
def main():
    if sys.argv[1] == "report":
        token_id, report_uri = createAppraisalReport()
        receipt = reportRegistry(token_id, report_uri)
        print(receipt)
        print("Report URI:", report_uri)

    if sys.argv[1] == "get":
        token_id = int(sys.argv[2])
        # this is the third argument on the command line
        bottle = wine_registry.functions.rare_wines(token_id).call()
        # we get the information about the bottle from the solidity contract
        #  rare_wines is a function in the solidity contract and here we are calling the fn
        reports = getRegistryReports(token_id)
        print(reports)
        print("Wine bottle name is", Winenot[0], "and is produced by", Winenot[1], "vintage", Winenot[2])
        #  returns the vin in position zero and the appraisal in position one


main()
