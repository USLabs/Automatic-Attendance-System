import requests
import bluetooth
import time
import datetime as dt
from datetime import datetime, timedelta
print "Automatic Attendance"

def pull():
    global devices_json, last_pulled, courseId, devices_all_arr, start_time, end_time, update_time, check_time, potential_dict, present_at_start, present_at_end, present, atStart, cnt, entered_once
    while True:
        r = requests.get("http://35.163.159.143:5002/CourseDetails")
        if(r.status_code>=200 and r.status_code<300):
            devices_json = r.json()
            print "Get Success"
            break
    
    last_pulled = datetime.now()
    courseId = devices_json['courseId']
    devices_all_arr = devices_json["macIds"]
    start_time = datetime.strptime(devices_json["startTime"], '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(devices_json["endTime"], '%Y-%m-%d %H:%M:%S')
    update_time = devices_json["updateTime"]
    check_time = start_time
    potential_dict = {}
    present_at_start = []
    present_at_end = []
    present = []
    atStart = 'true'
    cnt = 0
    entered_once = 'false'

pull()

while True:
    if datetime.now()>(last_pulled + timedelta(hours = update_time)):
        pull()
    
    if datetime.now()>=check_time and datetime.now()<=(check_time + timedelta(seconds = 60)) and datetime.now()<end_time and entered_once=='false':
        print "Checking " + time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
        devices = bluetooth.discover_devices(duration=40, lookup_names = True)
        for device_addr, name in devices:
            if(device_addr in devices_all_arr):
                if device_addr in potential_dict:
                    potential_dict[device_addr] += 1
                else:
                    potential_dict[device_addr] = 1
        for key, value in potential_dict.items():
            print key + " : " + str(value)
        entered_once = 'true'
    
    if(datetime.now()>=(check_time + timedelta(seconds = 60)) and datetime.now()<end_time):
        print "Slot: " + str(cnt)
        print "Prev: " + check_time.strftime('%a, %d %b %Y %H:%M:%S %Z')
        check_time = check_time + timedelta(seconds = 60)
        print "Now: " + check_time.strftime('%a, %d %b %Y %H:%M:%S %Z')
        cnt += 1
        entered_once = 'false'
        if(cnt>=2):
            print "Entered here too"
            if atStart=='true':
                for key in potential_dict:
                    if potential_dict[key]>=1:
                        present_at_start.append(key)
                potential_dict = {}
            else:
                for key in potential_dict:
                    if potential_dict[key]>=1:
                        present_at_end.append(key)
            check_time = end_time - timedelta(minutes = 5)
            cnt = 0
            if atStart=='false':
                present = filter(lambda x: x in present_at_end, present_at_start)
                for macid in present:
                    print macid
                while True:
                    r = requests.post("http://35.163.159.143:5002/attendance", data={'courseId': courseId, 'startTime': devices_json["startTime"], 'macIds': present})
                    if(r.status_code>=200 and r.status_code<300):
                        break
            atStart = 'false'
            
