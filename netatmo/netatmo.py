import netatmo.request as request
import json
import configparser

base_url = 'https://api.netatmo.com/api/'

def main_device_id():
    """
    return the main device id from the config
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['NETATMO']['MAIN_DEVICE_ID']

def getstationsdata(device_id):
    """
    get the station data
    :param device_id:
    :return station data json object:
    """

    url = base_url+'getstationsdata'
    return request.make_request(url, device_id)

def get_devices(station_data):
    """
    get the list of devices from the station data
    :param station data json object:
    :return dict with devices:
    """

    devices = []
    # print(station_data['devices'][0]['modules'])
    for device in station_data['devices'][0]['modules']:
         devices.append({"_id": device['_id'], "module_name": device['module_name'], "reachable": device['reachable'], 'data_types': device['data_type']})
    return devices

def get_main_station_data(station_data):
    """
    get the data of the main station
    """

    main_station_data = []
    main_station = station_data['devices'][0]
    for data_type in main_station['data_type']:
        data = {data_type : main_station['dashboard_data'][data_type]}
        main_station_data.append(data)
    return main_station_data

def get_module_data(station_data, module_id):
    """
    get the module data
    """
    found = False 

    for module in station_data['devices'][0]['modules']:
        if module['_id'] == module_id:
            module_data = []
            for data_type in module['data_type']:
                data = {data_type : module['dashboard_data'][data_type]}
                module_data.append(data)
            found = True
    if found: 
        return module_data 
    else: 
        return "module not found"
