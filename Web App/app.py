import pymysql
import pymysql.cursors
from flask import Flask, render_template, jsonify
from flask import request, session
from datetime import datetime, timedelta
#import MySQLdb
import os
from flask import session
import logging

app = Flask(__name__)


@app.route("/")
def main():
    return render_template('/index.html')

@app.route("/login", methods=['POST','GET'])
def login():
    _username=request.form['u']
    _password = request.form['p']

    print _username
    print _password
    db=pymysql.connect(host="raspberry.ci2gh79a5gmr.us-west-2.rds.amazonaws.com",port=3306,user="pi",passwd="raspberry", db="RASPBERRY")
    cursor=db.cursor()

    cursor.execute("select password,professor_ID,professor_name from professors where professor_username=%s",_username)

    if cursor.rowcount<=0:
        return render_template("/index.html", errmsg='* User not present')
    else:
        for record in cursor:
            if _password==record[0]:
                lectDict={}
                professorID=int(record[1])
                professorName=record[2]
                a=()
                print "professor"
                print professorID
                cursor.execute("SELECT lecture_id,lecture_name FROM RASPBERRY.lecture where professorID=%s", professorID)
                for lectures in cursor:
                    lectDict[lectures[0]]=lectures[1]
                #session.professorIdFromSession=professorID
                session['professorIdFromSession'] = professorID
                return render_template("/class.html",lectDicts=lectDict)
            else:
                from flask import json
                return render_template("/index.html", errmsg='* Wrong Password')
    cursor.close()
    db.close()
   # print("inside Login",_username)
    return " "



@app.route("/logout", methods=['POST','GET'])
def logout():
    session.clear()
    return render_template("/index.html")

@app.route("/SignupLink", methods=['POST','GET'])
def SignupLink():
    session.clear()
    return render_template("/signup.html")


#For doing Sign up
@app.route("/Signup", methods=['POST','GET'])
def Signup():
    db = pymysql.connect(host="raspberry.ci2gh79a5gmr.us-west-2.rds.amazonaws.com", port=3306, user="pi",
                         passwd="raspberry", db="RASPBERRY")
    print "Hiiii"
    profid = request.form['profid']
    profname = request.form['profname']
    profuname = request.form['profuname']
    profpass = request.form['profpass']
    intProfId=int(profid)
    cursor = db.cursor()
    cursor.execute("INSERT into RASPBERRY.professors values(%s,%s,%s,%s)", (int(profid), profname, profuname, profpass))
    db.commit()
    cursor.close()
    db.close()
    return "Successfully registered"




@app.route("/getClassInfo",methods=['POST','GET'])
def getclassInfo():
    classId = request.form['classNo']
    startTime = request.form['starttime']
    endTime = request.form['endtime']
    getDate = request.form['getdate']
    print startTime
    print endTime
    print "getDate"+getDate
    print "classId"+classId
    data = []
    db = pymysql.connect(host="raspberry.ci2gh79a5gmr.us-west-2.rds.amazonaws.com", port=3306, user="pi",
                         passwd="raspberry", db="RASPBERRY")
    cursor = db.cursor()
    if getDate:
        cursor.execute("SELECT b.student_ID, b.student_name, attendance_date, attendance_status FROM RASPBERRY.attendance a right join RASPBERRY.students b  on a.student_ID=b.student_ID where b.lecture_ID=1 and attendance_date=%s order by b.student_name",getDate)
    else:
        cursor.execute("SELECT b.student_ID, b.student_name, attendance_date, attendance_status FROM RASPBERRY.attendance a right join RASPBERRY.students b  on a.student_ID=b.student_ID where b.lecture_ID=1 order by b.student_name")
    for record in cursor:
        data.append([record[0], record[1], record[2], record[3]])
        #if record[3] is not 'P':
        #     data.append([record[0],record[1],'','A'])
        # else:
        #data.append([record[0], record[1], record[2], record[3]])
    cursor.close()
    db.close()
    return render_template('/Attendance.html', items=data)






#Redirect to new class form html
@app.route("/getNewClassForm",methods=['POST','GET'])
def getNewClassForm():
  #  classId = request.form['classNo']
    print session.get('professorIdFromSession')
    return render_template('/NewClass.html')

# make entry of new Class
@app.route("/registerNewClass",methods=['POST','GET'])
def registerNewClass():
    startTime = request.form['starttime']
    endTime = request.form['endtime']
    className = request.form['className']
    updateTime = request.form['updateTime']
    classDate = request.form['classdate']
    print classDate
    professorID=session.get('professorIdFromSession')
    #sprofessorID=101
    startTime= classDate+" "+startTime
    endTime = classDate+" "+endTime
    print endTime
    print startTime

    #print classDates
    lectDict = {}
    db = pymysql.connect(host="raspberry.ci2gh79a5gmr.us-west-2.rds.amazonaws.com", port=3306, user="pi",
                         passwd="raspberry", db="RASPBERRY")
    cursor = db.cursor()
    cursor.execute("insert into lecture(lecture_name, professorID,start_time,end_time,update_time) values(%s,%s,%s,%s,%s)", (className,professorID,startTime,endTime,updateTime))
    db.commit()

    cursor.execute("SELECT lecture_id,lecture_name FROM RASPBERRY.lecture where professorID=%s", professorID)
    for lectures in cursor:
        lectDict[lectures[0]] = lectures[1]
    cursor.close()
    db.close()
    return render_template("/class.html", lectDicts=lectDict)

# get class attendance data
@app.route("/getAttendance",methods=['POST','GET'])
def classDetqq():
    classID = request.form['classNo']

    data=[]
    db = pymysql.connect(host="raspberry.ci2gh79a5gmr.us-west-2.rds.amazonaws.com", port=3306, user="pi",
                         passwd="raspberry", db="RASPBERRY")
    cursor = db.cursor()
    print "classID"
    print classID
    cursor.execute("SELECT b.student_ID, b.student_name, attendance_date, attendance_status FROM RASPBERRY.attendance a right join RASPBERRY.students b  on a.student_ID=b.student_ID where b.lecture_ID=%s order by b.student_name",classID)
    for record in cursor:
        data.append([record[0], record[1], record[2], record[3]])
        # if record[3] is not 'P':
        #     data.append([record[0], record[1], '', 'A'])
        # else:
        #     data.append([record[0], record[1], record[2], record[3]])
    cursor.close()
    db.close()
    return render_template('/Attendance.html', items=data, classID=classID)

# Modify attendance search
@app.route("/modifyAttendanceSearch",methods=['POST','GET'])
def modifyAttendanceSearch():
    classID = request.form['classNo']
    startTime = request.form['starttime']
    endTime = request.form['endtime']
    getDate = request.form['getdate']
    print getDate
    data = []
    db = pymysql.connect(host="raspberry.ci2gh79a5gmr.us-west-2.rds.amazonaws.com", port=3306, user="pi",
                         passwd="raspberry", db="RASPBERRY")
    cursor = db.cursor()
    if getDate:
        cursor.execute("SELECT b.student_ID, b.student_name, attendance_date, attendance_status FROM RASPBERRY.attendance a right join RASPBERRY.students b  on a.student_ID=b.student_ID where b.lecture_ID=%s and attendance_date=%s order by b.student_name",(classID, getDate))
    else:
        cursor.execute("SELECT b.student_ID, b.student_name, attendance_date, attendance_status FROM RASPBERRY.attendance a right join RASPBERRY.students b  on a.student_ID=b.student_ID where b.lecture_ID=%s order by b.student_name",classID)



    for record in cursor:
        data.append([record[0], record[1], record[2], record[3]])
        # if record[3] is not 'P':
        #     data.append([record[0],record[1],'','A'])
        # else:
        #     data.append([record[0], record[1], record[2], record[3]])

    if startTime and endTime and getDate:
        startTime = getDate + " " + startTime
        endTime = getDate + " " + endTime
        cursor.execute("update lecture set start_time=%s,end_time=%s where lecture_ID=%s",(startTime,endTime,classID))
    # elif startTime:
    #     cursor.execute("update lecture set start_time=%s where lecture_ID=%s",(startTime, classID))
    # elif endTime:
    #     cursor.execute("update lecture set end_time=%s where lecture_ID=%s",(endTime, classID))
    db.commit()
    cursor.close()
    db.close()
    return render_template('/Attendance.html', items=data, classID=classID)



#Apoorva login API
@app.route("/getStudentDetails", methods=['GET','POST'])
def getStudentDetail():
    req= request.json
    i=0
    jsonResp={}

    studentid = req["studentid"]
    mac_adr = req["mac_adr"]
    username = req["username"]
    name = req["name"]
    data = []
    password = req["password"]
    isLogin = req["isLogin"]
    fromDate = req["from"]
    print "From Date="+fromDate
    toDate = req["to"]
    # fromDate="26/11/2016"
    # toDate="26/11/2016"
    if fromDate:
        fromDate=datetime.strptime(fromDate, '%d/%m/%Y')
    print unicode(fromDate)
    if toDate:
        toDate=datetime.strptime(toDate, '%d/%m/%Y')
    print unicode(toDate)
    db = pymysql.connect(host="raspberry.ci2gh79a5gmr.us-west-2.rds.amazonaws.com", port=3306, user="pi",
                         passwd="raspberry", db="RASPBERRY")
    print studentid
    if isLogin=='true' and not fromDate and not toDate:
        print "1"
        isloginFailed = True
        cursor = db.cursor()   
        print password
        try:
            cursor.execute("SELECT password FROM RASPBERRY.students where student_ID= %s limit 1", int(studentid))
            for record in cursor:
                i=1
                print record
                print record[0]
                if (record[0]==password):
                    isloginFailed=False
                    data=[]
                    cursor.execute("SELECT attendance_date, attendance_status FROM RASPBERRY.attendance  where student_ID=%s order by attendance_date desc",(int(studentid)))
                    for record in cursor:
                        a= record[0]
                        print a
                        listStr={"date":unicode(a),"attendance":record[1]}
                        print listStr
                        data.append(listStr)
                    jsonResp = {
                        "isLoginFailed": 'false',
                        "error": "LoginFailed",
                        "attendance": data
                    }

                else:
                    jsonResp={
                        "isLoginFailed": "true",
                        "error": "LoginFailed",
                        "attendance": data
                    }
            if i is 0:
                jsonResp = {
                    "isLoginFailed": "true",
                    "error": "LoginFailed",
                    "attendance": data
                }


        except Exception:
            Exception.message
            jsonResp = {
                "isLoginFailed": "true",
                "error": "LoginFailed:Database Error",
                "attendance": data
            }
    elif isLogin=='false' and not fromDate and not toDate:
        print "hiihh"
        cursor = db.cursor()
        print studentid
        print username
        print mac_adr
        print password
        try:
            i=cursor.execute("INSERT INTO `RASPBERRY`.`students` (`student_ID`,`student_name`, `MAC_ID`, `lecture_ID`, `password`) VALUES (%s,%s, %s,'1',%s)",(studentid,username,mac_adr,password))
            db.commit()
            cursor.close()
            db.close()
            if i==1:
                data = []
                jsonResp = {
                    "isLoginFailed": "false",
                    "error": "SignUpFailed",
                    "attendance": data
                }
            else:
                jsonResp = {
                    "isLoginFailed": "true",
                    "error": "SignUpFailed",
                    "attendance": data
                }
        except Exception:
            Exception.message
            jsonResp = {
                "isLoginFailed": "true",
                "error": "SignUpFailed:User or device already Registered",
                "attendance": data
            }

    else:
        cursor = db.cursor()
        try:
            data=[]
            cursor.execute("SELECT attendance_date, attendance_status FROM RASPBERRY.attendance  where student_ID=%s and attendance_date>=%s and attendance_date<=%s order by attendance_date desc",(int(studentid), fromDate, toDate))
            for record in cursor:
                a= record[0]
                print a
                listStr={"date":unicode(a),"attendance":record[1]}
                print listStr
                data.append(listStr)
            db.close()
            jsonResp = {
                "isLoginFailed": 'false',
                "error": "LoginFailed",
                "attendance": data
            }
        except Exception:
            jsonResp = {
                "isLoginFailed": "true",
                "error": "LoginFailed:Database Error",
                "attendance": data
            }
    print jsonResp
    return jsonify(jsonResp)


#Course Details API
@app.route("/CourseDetails")
def output():
    db = pymysql.connect(host="raspberry.ci2gh79a5gmr.us-west-2.rds.amazonaws.com", port=3306, user="pi",
                         passwd="raspberry", db="RASPBERRY")
    cursor = db.cursor()
    reply=""
    courseId=""
    startTime=""
    endTime=""
    updateTime=""
    macIDs=[]
    cursor.execute("SELECT l.lecture_ID, l.start_time, l.end_time, l.update_time FROM lecture l where l.lecture_ID = 1")
    for rows in cursor:
        courseId =rows[0]
        startTime =rows[1]
        endTime =rows[2]
        updateTime =rows[3]
        print startTime
        print (startTime + timedelta(days=1))
        diff=str(datetime.today()-startTime)
        if diff[0:1] is not "-":
            startTime= (startTime + timedelta(days=7))
            endTime = (endTime + timedelta(days=7))
            cursor.execute("update lecture set start_time=%s,end_time=%s where lecture_ID=1",(startTime,endTime))
            db.commit()

    cursor.execute("SELECT s.MAC_ID FROM students s where s.lecture_ID = 1")
    for rows in cursor:
        macIDs.append(rows[0])
    reply = {
        "courseId": courseId,
        "startTime": unicode(startTime),
        "endTime": unicode(endTime),
        "updateTime": updateTime,
        "macIds": macIDs
    }
    cursor.close()
    db.close()
    return jsonify(reply)

# Attendance Entry from Pi API
@app.route("/attendance", methods=['POST'])
def present():
    stuID = []
    allstudents=[]
    db = pymysql.connect(host="raspberry.ci2gh79a5gmr.us-west-2.rds.amazonaws.com", port=3306, user="pi", passwd="raspberry", db="RASPBERRY")
    cursor = db.cursor()
    data = request.get_json(force=True)
    print data
    course = data['courseID']
    logging.info(course)#print course
    #course = int(course)
    mac = data['macIDs']
    #print(mac)
    reqdate = data['startTime']
    #print reqdate
    reqdate = reqdate.split(" ")
    reqdate = reqdate[0]
    try:
        for x in mac:
            print "hihhi"
            print course
            cursor.execute("select student_ID from RASPBERRY.students where MAC_ID=\'%s\' AND lecture_ID=%d" % (x, course))
            for id in cursor:
                if id is not None:
                    #print id
                    stuID.append(id[0])
        print stuID
        cursor.execute("select student_ID from RASPBERRY.students where lecture_ID=%d" % course)
        for allid in cursor:
            if allid is not None:
                allstudents.append(allid[0])
        print allstudents
        if len(stuID) > 0:
            for x in stuID:
                cursor.execute("insert into RASPBERRY.attendance values('%s',%d,%d,'P')"% (reqdate, course, x))
                print "%d marked present" %x
            #return jsonify({'status': 'OK'})
            for x in allstudents:
                if x not in stuID:
                    cursor.execute("insert into RASPBERRY.attendance values('%s',%d,%d,'A')" % (reqdate, course, x))
                    print "%d marked absent" % x
            db.commit()
            db.close()
            return jsonify({'status': 'OK'})
        else:
             db.close()
             return jsonify({'status': 'NOT OK'})
    except Exception:
        print "Excep"
        return jsonify({'status': 'NOT OK'})

if __name__=="__main__":
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0',port=5002)