import csv
import os
import product
from collections import OrderedDict


def generate_csv_name():
    base_name = "export-{}.csv"
    for i in range(1, 1000):
        name = base_name.format(i)
        if not os.path.isfile(name):
            break
    return name


def generate_csv(data):
    # headers = OrderedDict([("c1", None), ("c2", None), ("c3", None), ("c4", None)])
    headers = OrderedDict(product.Product().__dict__)
    csv_file_name = generate_csv_name()
    print("\nGenerating CSV File: {}".format(csv_file_name))
    with open(csv_file_name, "w", newline="", encoding="utf-8") as fobj:
        dw = csv.DictWriter(fobj, delimiter=",", fieldnames=headers)
        dw.writeheader()
        for row in data:
            dw.writerow(row)
    return None



# data = [{
#     "c1": "data1",
#     "c2": "data2",
#     "c3": "data3",
#     "c4": "data4",
# }]


# def read_csv():
#     csv_file = get_csv_file()
#     with open(csv_file, 'r' ) as fobj:
#         reader = csv.DictReader(fobj)
#         data = list(reader)
#     return data
