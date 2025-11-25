import helper
import os
import json 

if not os.path.exists("/data/copySheet.csv"):
    print("khong co")

def getJsonData() -> json:
    with open("data/history.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return {"History Content": data['preContent'],"History Date": data['timeStamp']}

print(getJsonData())
updatingData = getJsonData()

helper.getUpdateSheet("copySheet",updatingData['History Content'], updatingData['History Date'])
