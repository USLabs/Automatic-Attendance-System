import requests

r = requests.get("http://35.163.159.143:5002/CourseDetails")
if (r.status_code >= 200 and r.status_code < 300):
    devices_json = r.json()
    print r.status_code

print devices_json["courseId"]
print devices_json["startTime"]
data = {"courseID": devices_json["courseId"], "startTime": devices_json["startTime"], "macIDs": ["554", "887"]}
r = requests.post("http://35.163.159.143:5002/attendance", data)
print r.status_code