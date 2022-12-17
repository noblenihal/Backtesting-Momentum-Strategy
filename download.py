import os
import datetime
import requests
import traceback
import shutil
import re
from zipfile import ZipFile, ZipInfo



def downloadHistoricalStockList(startYear, endYear, path="data"):

    if not os.path.exists(os.path.join(os.getcwd(), path)):
        os.makedirs(path)
    else:
        return

    for year in range(startYear, endYear+1):
        for month in range(1,13):

            date = datetime.datetime.strptime(f"{month}-{year}", "%m-%Y").strftime("%b%y").lower()
            url = "https://www1.nseindia.com/content/indices/mcwb_"+date+".zip"

            try:
                response = requests.get(url, stream=True)
                filename = url.split('/')[-1]

                with open(os.path.join(path, filename),'wb') as outputFile:
                    outputFile.write(response.content)
    
            except:
                with open("log.txt",'a+') as logFile:
                    logFile.write(f"File for {date} was not downloaded\n")


def extract(path="data"):
    folderpath = path
    filepaths  = [os.path.join(folderpath, name) for name in os.listdir(folderpath)]
    
    for file in filepaths:
        try:
            with ZipFile(file, 'r') as zipObj:
                listOfFileNames = zipObj.namelist()
                flag = 0 
                for fileName in listOfFileNames:
                    if re.search(r"(^nifty50)|(^niftymcwb)|([A-Za-z0-9]\/nifty50)|([A-Za-z0-9]\/niftymcwb)", fileName, flags=re.IGNORECASE):
                        flag+=1
                        if r"/" in fileName :
                            zipObj.extract(fileName, 'extracted')
                        else:
                            final_path = file.split('\\')[-1]
                            zipObj.extract(fileName, 'extracted\\'+ final_path)
                if flag == 0:
                    raise Exception 
        except:
            with open("log.txt",'a+') as logFile:
                logFile.write(f"{file} was not extracted\n")
            
        
def move_files():
    curr_dir = os.getcwd()
    src_dir = curr_dir+'\extracted'
    dest_dir = "CSVs"

    if not os.path.exists(os.path.join(os.getcwd(), dest_dir)):
        os.makedirs(dest_dir)    

    for root, dirs, files in os.walk((os.path.normpath(src_dir)), topdown=False):
        file = root.split("\\")[-1]
        filename = (file.split('_')[-1])[0:5]

        for name in files:
            if name.endswith('.csv'):
                os.rename((os.path.join(root, name)), os.path.join(root, filename+'.csv'))
                # print ("Found")
                SourceFolder = os.path.join(root,filename+'.csv')
                shutil.copy2(SourceFolder, dest_dir) 
                
            





# downloadHistoricalStockList(2008, 2022, "data")
# extract("data")
# move_files()