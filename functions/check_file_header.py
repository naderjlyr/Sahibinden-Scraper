import os.path
import json
import sys

import pandas as pd

class FlowException(Exception):
    pass
def checkFileHeader(header_added):
    jsonpath = 'C:\\Users\\nader\\PycharmProjects\\sahibindenScraper\\data.json'
    csvpath = 'C:\\Users\\nader\\PycharmProjects\\sahibindenScraper\\file.csv'
    with open(jsonpath, encoding='utf-8') as readData:
        jsonData = list(json.loads(readData.read()).keys())
        # print(jsonData)
        try:
            currentData = pd.read_csv(csvpath, usecols=["ad"]).stack().to_numpy().tolist()
            # print(currentData)
            if currentData:
                header_added = True
                for item in currentData:
                    if str(item) in jsonData:
                        print("a record is found, and removed : " + str(item))
                        jsonData.remove(str(item))
            return jsonData,header_added
        except Exception as e:
            trace_back = sys.exc_info()[2]
            line = trace_back.tb_lineno
            raise FlowException("coudldn't remove the ids from csv.",
                                "Process Exception in line {}".format(line),
                                e)