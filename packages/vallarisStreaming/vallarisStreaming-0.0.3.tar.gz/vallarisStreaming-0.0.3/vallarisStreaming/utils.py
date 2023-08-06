################# Vallaris Maps ##################
############## By : sattawat arab ###############
###### GIS Backend Engineer #########
########### i-bitz company limited ##############
##################### 2020 ######################

from distutils import ccompiler
import time
import tempfile
import os
import shutil
import json
import requests
from geopandas import GeoSeries
from shapely.geometry import Polygon
import geopandas as gpd
import pandas as pd
from tqdm import tqdm
from shapely.geometry import Polygon



def getData(dataset_id, VallarisServer, Api_Key):
    try:
        dir = tempfile.mkdtemp()
        local_filename = dir + "/" + str(dataset_id) + ".geojson"

        try:
            url = VallarisServer + "/1.0-beta/collections/" + \
                str(dataset_id)+"/items/streaming"

            payload = {}
            headers = {
                'API-Key': Api_Key
            }
            response = requests.request(
                "GET", url, headers=headers, data=payload)
            # print(response)

            total_size_in_bytes = int(
                response.headers.get('content-length', 0))
            block_size = 1024  # 1 Kibibyte
            progress_bar = tqdm(total=total_size_in_bytes,
                                unit='iB', unit_scale=True)

            with open(local_filename, 'wb') as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)
            progress_bar.close()

            if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                print("ERROR, something went wrong")

                if not os.path.exists(dir):
                    shutil.rmtree(dir)

                return "something wrong"

            else:
                readdata = gpd.read_file(local_filename, encoding='utf-8')
                readdata.to_file(dir + '/' + dataset_id +
                                 '.gpkg', driver="GPKG")

                if not os.path.exists(dir):
                    shutil.rmtree(dir)

                return dir + '/' + dataset_id + '.gpkg'
        except:
            url = VallarisServer + "/core/api/features/1.0-beta/collections/" + \
                str(dataset_id)+"/items/streaming"
            payload = {}
            headers = {
                'API-Key': Api_Key
            }
            response = requests.request(
                "GET", url, headers=headers, data=payload)
            print(response)
            total_size_in_bytes = int(
                response.headers.get('content-length', 0))
            block_size = 1024  # 1 Kibibyte
            progress_bar = tqdm(total=total_size_in_bytes,
                                unit='iB', unit_scale=True)

            with open(local_filename, 'wb') as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)
            progress_bar.close()

            if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                print("ERROR, something went wrong")

                if not os.path.exists(dir):
                    shutil.rmtree(dir)

                return "something wrong"

            else:
                readdata = gpd.read_file(local_filename, encoding='utf-8')

                if not os.path.exists(dir):
                    shutil.rmtree(dir)

                return readdata

    except Exception as e:
        # print(e)
        return 'something wrong'


def getExport(dataset_id, VallarisServer, Api_Key):

    try:
        dir = tempfile.mkdtemp()
        local_filename = dir + "/" + str(dataset_id) + ".geojson"
        url = VallarisServer + "/core/api/features/1.0-beta/collections/" + \
            str(dataset_id)+"/items/streaming"
        payload = {}
        headers = {
            'API-Key': Api_Key
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes,
                            unit='iB', unit_scale=True)
        with open(local_filename, 'wb') as file:
            for data in response.iter_content(block_size):
                file.write(data)

        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("ERROR, something went wrong")

            if not os.path.exists(dir):
                shutil.rmtree(dir)

            return "something wrong"

        else:
            read_file = gpd.read_file(
                dir + '/' + dataset_id + '.geojson', encoding='utf-8')
            if not os.path.exists(dir):
                shutil.rmtree(dir)

            return read_file

    except Exception as e:
        # print(e)
        return 'something wrong'


def newCollection(title, description, itemType, VallarisServer, Api_Key):
    try:
        url = VallarisServer + "/core/api/features/1.0-beta/collections"

        payload = json.dumps({
            "title": title,
            "description": description,
            "extent": {
                "spatial": {
                    "bbox": [
                        [
                            -180,
                            -90,
                            180,
                            90
                        ]
                    ],
                    "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                },
                "temporal": {
                    "interval": [
                        []
                    ],
                    "trs": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
                }
            },
            "itemType": itemType,
            "crs": [
                "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
            ],
            "links": [
                {
                    "href": "http://data.example.org/collections/1/items",
                    "rel": "items",
                    "type": "application/geo+json",
                    "title": title
                }
            ],
            "tileConfig": {}
        })

        headers = {
            'API-Key': Api_Key,
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        out_data = response.text

        return out_data

    except Exception as e:
        print(e)
        return 'something wrong'


def editCollection(dataset_id, title, description, itemType, VallarisServer, Api_Key):
    try:
        url = VallarisServer + \
            "/core/api/features/1.0-beta/collections/" + str(dataset_id)
        payload = json.dumps({
            "title": title,
            "description": description,
            "extent": {
                "spatial": {
                    "bbox": [
                        [
                            -180,
                            -90,
                            180,
                            90
                        ]
                    ],
                    "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                },
                "temporal": {
                    "interval": [
                        []
                    ],
                    "trs": "http://www.opengis.net/def/uom/ISO-8601/0/Gregorian"
                }
            },
            "itemType": itemType,
            "crs": [
                "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
            ],
            "public": False,
            "tileConfig": {},
            "links": [
                {
                    "href": "http://data.example.org/collections/1/items",
                    "rel": "items",
                    "type": "application/geo+json",
                    "title": title
                }
            ]
        })
        headers = {
            'API-Key': Api_Key,
            'Content-Type': 'application/json'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        out_data = response.text
        return out_data

    except Exception as e:
        print(e)
        return 'something wrong'


def delCollection(dataset_id, VallarisServer, Api_Key):
    try:

        try :
            url = VallarisServer + "/core/api/coverages/1.0-beta/manager/import/"+str(dataset_id)+"/jobs"
            payload = ""
            headers = {
                'API-Key': Api_Key
                }
            response = requests.request("DELETE", url, headers=headers, data=payload)
            # print(response.text)

        except :
            pass

        url = VallarisServer + \
            "/core/api/features/1.0-beta/collections/" + str(dataset_id)
        payload = {}
        headers = {
            'API-Key': Api_Key
        }

        response = requests.request(
            "DELETE", url, headers=headers, data=payload)
        out_data = response.text
        return out_data
    except Exception as e:
        print(e)
        return 'something wrong'


def getImport(dataset_id, data,  VallarisServer, Api_Key):
    try:
        dir = tempfile.mkdtemp()
        gdata = data
        crt = len(gdata)
        print('total : ' + str(crt))
        max = 10

        if crt <= max:
            crt2 = 1
        else:
            crt2 = (crt//max) + 1
        for i in range(0, crt2):
            st = 0 + (i*max)
            end = max + (i*max)
            out_data = gdata[st:end]
            crt_out_data = len(out_data)

            if crt_out_data < max:
                loop = end - (max - crt_out_data)
            else:
                loop = end

            out_data.to_file(dir + '/' + dataset_id + '_.geojson',
                             encoding='utf-8', driver="GeoJSON", ensure_ascii=False)

            with open(dir + '/' + dataset_id + '_.geojson', encoding='utf-8') as f:
                data = json.load(f)

            data_get = json.dumps(data, ensure_ascii=False)
            data2 = str(data_get).replace("'", '"')
            try:
                data3 = str(data2).replace("None", '""')
            except:
                data3 = data2

            url = VallarisServer + "/core/api/features/1.0-beta/collections/"+dataset_id+"/items"
            payload = str(data3)
            headers = {
                'API-Key': Api_Key,
                'Content-Type': 'application/json'
            }
            response = requests.request(
                "POST", url, headers=headers, data=payload.encode('utf-8'))
            # print(response.text)

            try:
                res_json = response.json()
                res_code = res_json['code']
            except:
                res_code = False

            if res_code != False:
                # print(res_code)
                print('import error: ' + str(loop))
                if not os.path.exists(dir + '/dataInvalid'):
                    os.makedirs(dir + '/dataInvalid')
                os.remove(dir + '/' + dataset_id + '_.geojson')
            else:
                os.remove(dir + '/' + dataset_id + '_.geojson')
                print('import success : ' + str(loop))

        if not os.path.exists(dir):
            shutil.rmtree(dir)
        return 'successful : ' + VallarisServer + '/management/datastore/features/' + dataset_id

    except Exception as e:
        # print(e)
        return 'something wrong'


def editFeatures(dataset_id, features_id, data,  VallarisServer, Api_Key):

    try:
        dir = tempfile.mkdtemp()

        data.to_file(dir + '/' + features_id + '_.geojson',
                     encoding='utf-8', driver="GeoJSON", ensure_ascii=False)

        with open(dir + '/' + features_id + '_.geojson', encoding='utf-8') as f:
            data = json.load(f)

        data_get = json.dumps(data, ensure_ascii=False)
        data2 = str(data_get).replace("'", '"')
        try:
            data3 = str(data2).replace("None", '""')
        except:
            data3 = data2

        data4 = json.loads(data3)

        url = VallarisServer + "/core/api/features/1.0-beta/collections/" + \
            str(dataset_id) + "/items/" + str(features_id)
        payload = json.dumps(data4['features'][0])
        headers = {
            'API-Key': Api_Key,
            'Content-Type': 'application/json'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        out_data = response.text

        if not os.path.exists(dir):
            shutil.rmtree(dir)

        return out_data

    except Exception as e:
        # print(e)
        if not os.path.exists(dir):
            shutil.rmtree(dir)

        return 'something wrong'


def delFeatures(dataset_id, features_id,  VallarisServer, Api_Key):

    try:
        url = VallarisServer + "/core/api/features/1.0-beta/collections/" + \
            str(dataset_id) + "/items/" + str(features_id)

        payload = {}
        headers = {
            'API-Key': Api_Key,
            'Content-Type': 'application/json'
        }

        response = requests.request(
            "DELETE", url, headers=headers, data=payload)
        out_data = response.text
        return out_data

    except Exception as e:
        print(e)
        return 'something wrong'


def makeTile(dataset_id, dataset_out, VallarisServer, Api_Key, parameter):
    try:
        url = VallarisServer + \
            "/core/api/processes/vallaris/214bffaba098493005c5/" + \
            str(dataset_id)

        payload = json.dumps(parameter)
        headers = {
            'API-Key': Api_Key,
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        job_json = response.json()

        try :
            getjobID =  job_json['transaction']
            # print(getjobID)
            print("start make tile")
        except :
            return response.text

        while True :
            time.sleep(10)
            response_st = requests.request("GET", f"{VallarisServer}/core/api/processes/vallaris/processes/214bffaba098493005c5/jobs/" + getjobID , headers=headers, data='')
            # print(response_st.json())
            print(f'{str(response_st.json()["status"])} : {str(response_st.json()["progress"])} %')
            if str(response_st.json()["progress"]) == "100" and response_st.json()["status"] == "successful":
                status = response_st.json()["status"]
                break

            if response_st.json()["status"] == "failed":
                status = response_st.json()["status"]
                break
        
        if status == "successful":
            return 'successful : ' + VallarisServer + "/management/visual/tiles/vector/" + parameter['data_filter']['dataset_out']
        
        else:
            return 'error to create coverage : failed'

        # out_data = response.text

    except Exception as e:
        print(e)
        return 'something wrong'