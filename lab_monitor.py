#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socketio
import time
import requests
import json
from datetime import datetime
import ftplib 
import paho.mqtt.client as paho
import socket

print ("Network checking")
while True:
	try:
		requests.get('https://google.com.vn/').status_code
		print ("Network is connected")
		break;
	except:
		print ("waiting for network")
		time.sleep(5)

token=''
audio_file=''
broker="10.1.0.108"
port=8080
device_alert = {
        }
    
    

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = "Hello, WatchDog!"

        
def voice_request(voice_text):
    payload = voice_text
    url = 'https://api.fpt.ai/hmi/tts/v5'
    headers = {
        'api-key': 'd4QsD0AgCjVwZxb70HBHElWGufA0Oa9B',
        'speed': '',
        'format':'wav',
        'voice': 'banmai'
    }
    response = requests.request('POST', url, data=payload.encode('utf-8'), headers=headers)
    json_data = response.json()
    
    source = json_data['async']
    
    print(source)
    time.sleep(2)
    current_time = time.time()

    global audio_file 
    audio_file  = str(current_time) +'.wav'
    
    doc = requests.get(source)
    with open(audio_file, 'wb') as f:
        f.write(doc.content)

    
    session = ftplib.FTP('10.1.0.108','ldthinh','1_Abc_123')
    file = open(audio_file,'rb')                  # file to send
    session.storbinary('STOR '+audio_file  , file)     # send the file
    file.close()                                    # close file and FTP
    session.quit()
    

    print(audio_file)

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass
    
client1= paho.Client("control1")                           #create client object
client1.on_publish = on_publish                          #assign function to callback
client1.connect(broker,port)                                 #establish connection

sio = socketio.Client()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def watchdog_ping():
    try:
        print_log("WatchDog ping")
        sock.sendto(MESSAGE.encode("utf-8"), (UDP_IP, UDP_PORT))
        sock.sendto(MESSAGE.encode("utf-8"), (UDP_IP, UDP_PORT + 1))
    except Exception as err:
        print(err)


@sio.event
def connect():
    print('connection established')
    

  

@sio.on('lab_monitor')
def response(*args):
    current_temp = args[0]['temp']
    response = requests.get('https://sensorhub.tech/api/get_device_info/%s'%args[0]['lab_id'],
    headers={'Content-Type':'application/json',
           'Authorization': 'Bearer {}'.format(token)})
    json_data = response.json()
    lab_name = json_data[0]['device_name']
    lab_id = json_data[0]['device_id']
    threshold = json_data[0]['threshold']
    phone = json_data[0]['alert']['phone']
    is_call = json_data[0]['alert']['is_call']
    
    now = datetime.now()
    watchdog_ping()

    if float(current_temp) > float(threshold):
        #The first time dict dont have item
        if device_alert.get(lab_id) == None:
            device_alert.update( {lab_id : 0} )
            
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        if  (int(time.time()) - int(device_alert.get(lab_id))) > 180:
            if is_call == 'on':
                action_type='call'
            else:
                action_type='sms'
            
            voice_text = 'Xin chào,nhiệt độ phòng lab %s là %s cao hơn ngưỡng %s '%(lab_name,current_temp,threshold)
           # voice_text ='xin'
            print(voice_text)
            voice_request(voice_text)
            time.sleep(1)
            print('WARN SEND MQTT: %s Lab:%s Temp:%s Threhold:%s'%(dt_string,lab_name,current_temp,threshold))
            ret= client1.publish("/lg/ctrl", '{"action":"%s","destNumber":"%s","smsMsg":"Nhiet do hien tai: %s vuot nguong: %s","audioFile":"%s"}'%(action_type,phone,current_temp,threshold,audio_file))
            device_alert.update( {lab_id : int(time.time())} )
        else:
            print('WARN: %s Lab:%s Temp:%s Threhold:%s'%(dt_string,lab_name,current_temp,threshold))
    else:
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print('INFO: %s Lab:%s Temp:%s Threhold:%s'%( dt_string,lab_name,current_temp,threshold))


if __name__=="__main__":
    
    pload ={'email':'nxthongbk@gmail.com','password':'1_Abc_123'}
    response = requests.post('https://sensorhub.tech/api/login',data = pload)
    json_data = response.json()
    token = json_data['token']
    
   

    
    sio.connect('https://sensorhub.tech')
    sio.wait()
    client1.loop_forever()
   
