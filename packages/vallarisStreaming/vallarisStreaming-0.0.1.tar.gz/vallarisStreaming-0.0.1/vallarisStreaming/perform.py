################# Vallaris Maps ##################
############## By : sattawat arab ###############
###### GIS Backend Engineer #########
########### i-bitz company limited ##############
##################### 2020 ######################

import time
import tempfile
import os
from os import listdir
from os.path import isfile, join
import json
import uuid
import urllib.request
from urllib.request import urlopen
from urllib.request import urlretrieve
import cgi
import requests
import tarfile
from geopandas import GeoSeries
from shapely.geometry import Polygon
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
from vallaris.utils import *
from IPython.display import display, Javascript, Markdown as md, HTML
from urllib.parse import urlencode
import zipfile
from IPython.display import IFrame
import rasterio
from rasterio.plot import show
import numpy as np
import re
from matplotlib import pyplot
import matplotlib.pyplot as plt
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import requests
import xmltodict
from shapely.geometry import Point, Polygon, LineString
import json
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

def setEnviron(parameter, *args, **kwargs):
    storage = kwargs.get('storage', False)

    try:
        msgBody = json.loads(parameter)
    except:
        msgBody = parameter

    try:
        GP_API_FEATURES_HOST = os.environ.get(
            'GP_API_FEATURES_HOST', 'https://v2k-dev.vallarismaps.com/core/api/features')
        url = GP_API_FEATURES_HOST.split("/")[-4]
        Api_Key = msgBody["API-Key"]
        VallarisServer = GP_API_FEATURES_HOST

        if 'APIKey' in os.environ:
            del os.environ['APIKey']

        if 'VallarisServer' in os.environ:
            del os.environ['VallarisServer']

        os.environ["APIKey"] = Api_Key
        os.environ["VallarisServer"] = VallarisServer

    except:
        Api_Key = os.environ["APIKey"]
        VallarisServer = os.environ["VallarisServer"]

    return [Api_Key, VallarisServer]


def ConnectData(property):

    try :
        get_data = property
        host = os.environ["VallarisServer"]
        APIKey = os.environ["APIKey"]
        # print(host)
        # get Properties
        url = host + "/core/api/streaming/v1.1/ObservedProperties?$top=1000&api_key=" + str(APIKey)

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        res_json = response.json()
        # print(res_json)

        crt = len(res_json['value'])

        properties_id = []
        for i in range(0,crt):

            if str(res_json['value'][i]['name']) == get_data :
                properties_id.append(str(res_json['value'][i]['@iot.id']))
                # print((str(res_json['value'][i]['name'])))
            else :
                pass

        # print(properties_id)

        # get Properties id
        url = host + "/core/api/streaming/v1.1/ObservedProperties("+str(properties_id[0])+")?api_key=" + str(APIKey)

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        res_json = response.json()
        # print(res_json)


        # get by station
        url = host + "/core/api/streaming/v1.1/ObservedProperties("+str(properties_id[0])+")/Datastreams?$top=100&api_key=" + str(APIKey)

        # print(url)

        payload = {}
        headers = {}

        response_station = requests.request("GET", url, headers=headers, data=payload)

        response_station_json = response_station.json()
        # print(response_station_json)

        ctr2 = len(response_station_json['value'])
        # print(ctr2)

        thing_id = []
        for i in range(0,ctr2):
            thing_id.append(str(response_station_json['value'][i]['@iot.id']))

        # print(thing_id)

        # Thing
        crt_thing = len(thing_id)
        location = []
        for i in range(0, crt_thing):
            url = host + "/core/api/streaming/v1.1/Datastreams("+str(thing_id[i])+")/Thing?api_key=" + str(APIKey)

            payload = {}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)

            res_json = response.json()
            location.append(str(res_json['@iot.id']))

        # Location
        crt_location = len(location)

        arr_data = []
        for i in range(0,crt_location):
            # print(i)
            url = host + "/core/api/streaming/v1.1/Things("+str(location[i])+")/Locations?api_key=" + str(APIKey)

            payload = {}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)

            res_json = response.json()
            # print(res_json)

            # 
            url = host + "/core/api/streaming/v1.1/Datastreams("+str(thing_id[i])+")/Observations?$top=1&api_key=" + str(APIKey)
            # print(url)

            payload = {}
            headers = {}

            response_val = requests.request("GET", url, headers=headers, data=payload)

            res_json_val = response_val.json()
            # print(res_json)

            try :
                phenomenonTime = res_json_val['value'][0]['phenomenonTime']
                result = res_json_val['value'][0]['result']

                # print(str(phenomenonTime), ' ', str(result))
            except Exception as e:
                phenomenonTime = None
                result = None

            try :
                id = res_json['value'][0]['@iot.id']
                name = res_json['value'][0]['name']
                x = res_json['value'][0]['location']['coordinates'][0]
                y = res_json['value'][0]['location']['coordinates'][1]

                arr = {'id': id, 'name': name, 'x': x, 'y': y, "phenomenonTime": phenomenonTime, "result":result}
                arr_data.append(arr)
                # arr_x.append(x)
                # arr_y.append(y)
                # print(str(name) , ' ,' , str(x), ' ,', str(y))
            except :
                print("no data" , ' ' ,str(str(location[i])))



        # Create an empty DataFrame
        df = pd.DataFrame()

        # Loop through the data array
        for item in arr_data:
            # Append each item to the DataFrame
            df = df.append(item, ignore_index=True)

        # Print the resulting DataFrame
        # print(df)

        # Create a geometry column using the x and y coordinates
        geometry = [Point(x, y) for x, y in zip(df['x'], df['y'])]

        # Create a GeoDataFrame
        gdf = gpd.GeoDataFrame(df, geometry=geometry)

        gdf['result'] = gdf['result'].astype(float)
        
        return gdf
    
    except Exception as e:
        # print(e)
        msg = "Perform step Connect Data KeyError: " + str(e)
        return msg

def FetchData(PARAMETER, *args, **kwargs):
    AGRITRONIC_API_URL = kwargs.get('AGRITRONIC_API_URL', False)
    AGRITRONIC_APP_KEY = kwargs.get('AGRITRONIC_APP_KEY', False)
    VALALRIS_API_URL = kwargs.get('VALALRIS_API_URL', False)
    VALALRIS_API_KEY = kwargs.get('VALALRIS_API_KEY', False)
    STATION_ID = kwargs.get('STATION_ID', False)
    DATA_DATE = kwargs.get('DATA_DATE', False)
    
    try:

        AGRITRONIC_API_URL = AGRITRONIC_API_URL
        AGRITRONIC_APP_KEY = AGRITRONIC_APP_KEY

        VALALRIS_API_URL = VALALRIS_API_URL
        VALALRIS_API_KEY = VALALRIS_API_KEY

        STATION_ID = STATION_ID
        START_DATA_DATE = DATA_DATE

        MATCH_PARAMETER = PARAMETER

        def SOS_ADD_DATASTREAM(DatastreamID,LONTITUDE,LATITUDE,value,time):
            payload = [
                {
                    "phenomenonTime"    : time,
                    "resultTime"        : time,
                    "result"            : float(value),
                    "resultType"        : "number",
                    "Datastream": {
                        "@iot.id"       : DatastreamID
                    },
                "FeatureOfInterest": {
                    "name"           : STATION_ID,
                    "description"    : STATION_ID,
                    "encodingType": "application/vnd.geo+json",
                    "feature": {
                        "coordinates": [
                            LONTITUDE,
                            LATITUDE,
                        ],
                        "type": "Point"
                    }
                }
                }
            ]
            
            headers = {
                'Content-Type': 'application/json',
                'API-Key': VALALRIS_API_KEY
            }
            
            url = f"{VALALRIS_API_URL}/streaming/v1.1/Observations"
        
            response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
            if (response.status_code != 201):
                return response.json()

        for PARAM in MATCH_PARAMETER:
            print(f"RUNNING : {STATION_ID} : {PARAM['agritronics_node_id']} : {PARAM['agritronics_type_id']}")
            OBSERVATION_ID      = PARAM["observation_id"]
            AGRITRONIC_GET_URL  = f"{AGRITRONIC_API_URL}?appkey={AGRITRONIC_APP_KEY}&p={STATION_ID},{PARAM['agritronics_node_id']},{PARAM['agritronics_type_id']},{START_DATA_DATE}"
            AGRITRONIC_DATA     = requests.get(AGRITRONIC_GET_URL).text
            AGRITRONIC_DATA     = xmltodict.parse(AGRITRONIC_DATA)
            
            STATION_LAT         = AGRITRONIC_DATA["xhr"]["IO"]["@Latitude"]
            STATION_LON         = AGRITRONIC_DATA["xhr"]["IO"]["@Longitude"]
            
            for DATA in AGRITRONIC_DATA["xhr"]["IO"]["Data"]:
                Observation_Value   = DATA["Value"]
                Observation_Time    = datetime.strptime(DATA["IODateTime"], '%Y-%m-%d %H:%M:%S').strftime("%Y-%m-%dT%H:%M:%S.000Z")
                SOS_ADD_DATASTREAM(OBSERVATION_ID,STATION_LON,STATION_LAT,Observation_Value,Observation_Time)
        
        return 'Successful'
    
    except Exception as e:
        # print(e)
        msg = "Perform step Fetch Data KeyError: " + str(e)
        return msg