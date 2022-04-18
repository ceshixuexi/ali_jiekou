import os

import json


def analyze_file(file_name):

    with open("..%sdata%s%s" % (os.sep, os.sep, file_name), "rb") as f:
        case_data = json.load(f)
        data_list = list()
        for i in case_data.values():
            data_list.append(i)

        return data_list
if __name__=="__main__":
    print(analyze_file('ali_request.json'))