import requests
import json
import os
import csv
import time
import tempfile
from io import StringIO
import pandas

__DEFAULT_ENDPOINT = "https://dev.citybrain.org/api/getData"
__DEFAULT_ODPS_DATA_ADDRESS = "170DD61338021000"

endpoint: str = ""

def __get_download_endpoint() -> str:
    return __get_endpoint().replace("getData", "download")

def __get_endpoint() -> str:
    if endpoint != '':
        return endpoint
    envEndpoint = os.getenv('CITYBRAIN_DATA_ENDPOINT')
    if envEndpoint is not None and envEndpoint != '':
        return envEndpoint
    return __DEFAULT_ENDPOINT


def __get_odps_dataaddress(dataAddress: str) -> str:
    if dataAddress != '':
        return dataAddress
    envODPSDataAddress = os.getenv('CITYBRAIN_ODPS_DATA_ADDRESS')
    if envODPSDataAddress is not None and envODPSDataAddress != '':
        return envODPSDataAddress
    return __DEFAULT_ODPS_DATA_ADDRESS

def retrieve_file(dataAddress: str) -> str:
    return __download_file(dataAddress=dataAddress)


def retrieve_raw(dataAddress: str = '', sql: str = '') -> any:
    if sql == '':
        if dataAddress == '':
            raise Exception('must specify data address')
        content = __get_content(dataAddress=dataAddress)
        return content.replace('\ufeff', '', 1)
    else:
        # create odps sql task
        taskID = __create_sql_task(dataAddress=dataAddress, sql=sql)

        # query task status until terminated
        status = __query_task_status(dataAddress=dataAddress, taskID=taskID)
        while status != 'Terminated':
            time.sleep(2)
            status = __query_task_status(dataAddress=dataAddress, taskID=taskID)

        # download task result
        return __download_task_result(dataAddress=dataAddress, taskID=taskID)

def retrieve_df(dataAddress: str = '', sql: str = '') -> pandas.DataFrame:
    if sql == '': # file data
        if dataAddress == '':
            raise Exception('must specify data address')
        # download file content
        content = __get_content(dataAddress=dataAddress)
        content = content.replace('\ufeff', '', 1)

        # convert to dataframe
        src = []
        tmp = StringIO(content)
        csvReader = csv.reader(tmp, delimiter=',')
        for row in csvReader:
            src.append(row)
        return pandas.DataFrame(src[1:], columns=src[0])
        
    else: # odps data
        # create odps sql task
        taskID = __create_sql_task(dataAddress=dataAddress, sql=sql)

        # query task status until terminated
        status = __query_task_status(dataAddress=dataAddress, taskID=taskID)
        while status != 'Terminated':
            time.sleep(2)
            status = __query_task_status(dataAddress=dataAddress, taskID=taskID)

        # download task result
        result = __download_task_result(dataAddress=dataAddress, taskID=taskID)

        # convert to dataframe
        if len(result) == 0:
            return pandas.DataFrame([])
        src = []
        for row in result[1:]:
            src.append(row.split(';'))
        return pandas.DataFrame(src, columns=result[0].split(';'))
    
def __download_file(dataAddress: str) -> str:
    endpoint = __get_download_endpoint()
    with requests.get(endpoint+'?dpaddress='+dataAddress, stream=True) as r:
        r.raise_for_status()
        
        fd, filename = tempfile.mkstemp()
        with open(filename, 'wb') as tmp:
            for chunk in r.iter_content(chunk_size=4096): 
                tmp.write(chunk)

    return filename

    
def __get_content(dataAddress: str) -> str:
    endpoint = __get_endpoint()
    reqBody = {'dpAddress': dataAddress, 'payload': ''}
    resp = requests.post(url=endpoint, headers={'content-type': 'application/json'}, json=reqBody, timeout=None)
    if resp.status_code != 200:
        raise Exception('request failed, status code is: ' + str(resp.status_code))
    result = resp.json()
    if result['code'] != 200:
        raise Exception('server error: message is: ' + str(result['message']))
    if isinstance(result['data'], str):
        return result['data']

	
def __download_task_result(dataAddress: str, taskID: str) -> list[str]:
    endpoint = __get_endpoint()
    dataAddress = __get_odps_dataaddress(dataAddress=dataAddress)
    reqBody = {"dpAddress": dataAddress, 'payload': json.dumps({'payload': taskID, 'action': 'TASK_DownloadResult'})}
    resp = requests.post(url=endpoint, headers={'content-type': 'application/json'}, json=reqBody, timeout=None)
    if resp.status_code != 200:
        raise Exception('request failed, status code is: ' + str(resp.status_code))
    result = resp.json()
    if result['code'] != 200:
        raise Exception('server error: message is: ' + str(result['message']))
    strList = json.loads(result['data'])
    return strList


def __query_task_status(dataAddress: str, taskID: str) -> str:
    endpoint = __get_endpoint()
    dataAddress = __get_odps_dataaddress(dataAddress=dataAddress)
    reqBody = {"dpAddress": dataAddress, 'payload': json.dumps({'payload': taskID, 'action': 'TASK_QueryStatus'})}
    resp = requests.post(url=endpoint, headers={'content-type': 'application/json'}, json=reqBody, timeout=None)
    if resp.status_code != 200:
        raise Exception('request failed, status code is: ' + str(resp.status_code))
    result = resp.json()
    if result['code'] != 200:
        raise Exception('server error: message is: ' + str(result['message']))
    return result['data']


def __create_sql_task(dataAddress: str, sql: str) -> str:
    endpoint = __get_endpoint()
    dataAddress = __get_odps_dataaddress(dataAddress=dataAddress)
    reqBody = {'dpAddress': dataAddress,'payload': json.dumps({'payload': sql, 'action':'TASK_Create'})}
    resp = requests.post(url=endpoint, headers={'content-type': 'application/json'}, json=reqBody, timeout=None)
    if resp.status_code != 200:
        raise Exception('request failed, status code is: ' + str(resp.status_code))
    result = resp.json()
    if result['code'] != 200:
        raise Exception('server error: message is: ' + str(result['message']))
    return result['data']
