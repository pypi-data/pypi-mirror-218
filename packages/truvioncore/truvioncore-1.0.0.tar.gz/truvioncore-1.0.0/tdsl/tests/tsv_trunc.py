import sys
import os

import csv
import json
from tdsl.express import twk_hammer

if __name__ == '__main__':

    fn = '/Users/mat/Documents/__src__/labs/ETFData/test_suppression.json'
    js = ''
    rows = []
    with open(fn, 'r') as j_file:
        d = json.load(j_file)
        print(f'. {len(d)}')

    #     for line in j_file:
    #         try:
    #             line = line.replace('"', "'").strip("\n")
    #             line = f'"{line}"'
    #             d = json.loads(line)
    #             rows.append(d)
    #         except Exception as e:
    #             print(e)
    #             print(f'. bad line - {line}')
    #             rows.append(twk_hammer(json.loads(line)))
    # print(f'. len rows {len(rows)}')

    # output
    #
    # Invalid \escape: line 1 column 175 (char 174)
    # . bad line - "{'attributes': {'type': 'Lead', 'url': '/services/data/v42.0/sobjects/Lead/00Q1U00000JYpqgUAD'}, 'Id': '00Q1U00000JYpqgUAD', 'Name': 'Susan Eovacious', 'Street': '32246 VÃÂ\xada Arias', 'City': 'Temecula', 'State': 'CA', 'Country': None, 'PostalCode': '92592', 'Phone': '9512971216', 'VendorLeadID__c': None, 'Days_Since_Modified__c': 412.0, 'DoNotCall': True, 'Direct_Mail_Opt_Out__c': True, 'FirstName': 'Susan', 'LastName': 'Eovacious'}"
    # . len rows 42915


    # i = 0
    # fn = '/Users/mat/Documents/__src__/labs/ETFData/Kasayama/loaders/quantarium/sample/Full/Quantarium_OpenLien_King_20210203_00001.TSV'
    # fout = 'dump.tsv'
    # with open(fn, 'r') as tsv_file:

    #     with open(fout, 'w', newline='') as file_out:
    #         writer = csv.writer(file_out, delimiter='\t')
    #         reader = csv.reader(tsv_file, delimiter='\t')
    #         for line in reader:
    #             i += 1
    #             if i == 1:
    #                 print(f'. header {line}')
    #                 continue
    #             if i > 1000:
    #                 break

    #             writer.writerow(line)



