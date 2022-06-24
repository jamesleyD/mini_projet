import pandas as pd
import requests
import csv

print("the script has started...\n")

API_URL = "https://api-adresse.data.gouv.fr/search/"
FILE = pd.read_csv('CSV/test_adresses.csv')
CSV_HEADER = "contact_id|address"


colum_list = ["contact_id", "score", "label", "housenumber",
              "name", "postcode", "citycode", "city", "x", "y", "street"]
csv_array = [colum_list]


def csv_split(string, mode):
    """ Split and return the address or id of the contact"""
    split = string.split("|")

    if mode == "id":
        return split[0]
    if mode == "adr":
        return split[1]

    return split


def best_score(json):
    """Return the item with the highest score"""
    res = 0
    last_score = -1

    for element in json:
        if (element["properties"]["score"] > last_score):
            res = element
            last_score = element["properties"]["score"]

    return res


def create_row(json, id):
    """Create and return a new array that defines a row based on column_list"""
    new_row = []

    for colum in colum_list:
        if (colum == "contact_id"):
            new_row.append(id)
        else:
            new_row.append(json[colum])

    return new_row


def start_script(row):
    """Function that finds the best address of a contact and saves the information in the csv_array"""
    parsed_adress = csv_split(row, "adr")  # initial address retrieval
    parsed_id = csv_split(row, "id")  # contact id retrieval

    # parameters for the GET request
    query = {"q": parsed_adress.replace(" ", "+")}

    response = requests.get(API_URL, params=query)
    r = response.json()["features"]

    # search for the best score
    best = best_score(r)
    csv_array.append(create_row(best["properties"], parsed_id))
 


for row in FILE[CSV_HEADER]:
    print("\nfind the best address for ")
    print(row)

    start_script(row)


with open('CSV/result.csv', 'w', newline='') as new_file:
    print("\ncreating a new csv file...")
    # create the csv writer
    writer = csv.writer(new_file)

    # write all rows to csv file
    writer.writerows(csv_array)

print("\nDone: the result can be found at the location: CSV/result.csv")
