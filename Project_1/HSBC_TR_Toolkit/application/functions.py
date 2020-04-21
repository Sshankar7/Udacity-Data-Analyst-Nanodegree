from csv import reader 
from application import Config
from flask import Response, json, stream_with_context
import pandas as pd
import os 

filename = "Path_Updates.csv"
UPLOADED_PATH = os.path.join(Config.BASE_DIR, Config.UPLOAD_FOLDER, filename)
ALLOWED_EXTENSIONS = {'csv'}

def file_contents():
    ctr = 0
    flag = ""
    
    with open(UPLOADED_PATH, 'r') as f:
        csv_reader = reader(f)
        # Skip Header
        next(csv_reader, None)
        for row in csv_reader:
            if row[2] == "":
                ctr += 1
    if ctr < 1:
        flag = "upPaths"
    return flag

def path_data():
    with open(UPLOADED_PATH, 'r') as f:
        csv_reader = reader(f)
        next(csv_reader, None)
        data = [row for row in csv_reader]
    return data

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def regions_list():
    path = os.path.join(Config.BASE_DIR, Config.APP_STATIC_FOLDER)
    region_file = pd.read_csv(path+"/REGIONS_LIST.csv")
    return region_file


def progress(current,total):
    def generate(current, total):
        x = 0
        x = int((current/total)*100)
        #print(x)
        yield str(x)
        
    return generate(current, total)