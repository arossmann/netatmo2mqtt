import netatmo as na
import json
import paho.mqtt.client as mqtt
import datetime
import configparser


config = configparser.ConfigParser()
config.read('config.ini')

def publish_to_mqtt(topic, msg):
    """
    """
    client = mqtt.Client("P1")
    client.username_pw_set(config['NETATMO']['BROKER_USER'], config['NETATMO']['BROKER_PASSWORD'])
    client.connect(config['NETATMO']['BROKER_ADDESS'])
    client.publish(topic, msg)

if __name__ == "__main__":

    sd = na.getstationsdata(na.main_device_id())
    # print(get_devices(sd))
    #print("fetching data from main station")
    msg = json.dumps(na.get_main_station_data(sd))
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+";Basis;"+msg)
    publish_to_mqtt(config['NETATMO']['BROKER_BASE_TOPIC']+"/"+"Basis",msg)
    for device in na.get_devices(sd):
        msg = ""
        #print("fetching data from device: "+device['module_name'])
        msg = json.dumps(na.get_module_data(sd,device['_id']))
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+";"+device['module_name']+";"+msg)
        publish_to_mqtt(config['NETATMO']['BROKER_BASE_TOPIC']+"/"+device['module_name'].replace(" ","_"),msg)
