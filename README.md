# Automatic-Attendance-System

## System Components:
1. Raspberry Pi 
2. Android App
3. Python-Flask Web application
4. Amazon RDS
5. Amazon EC2

## Features implemented:
* Utilized Raspberry Pi 3 for marking attendance using Bluetooth.
* Enhanced reliability over bluetooth functionality of Raspberry pi using an algorithm considering multiple time slots and providing more chances for the bluetooth device to be detected.
* Run Raspberry Pi on class time provided as input from professor and dynamically.
* Built a Python-Flask web app through which professors can register new classes, monitor attendance details.
* Utilized Amazon EC2 instance for hosting the web application, and exposing the necessary APIs for receiving/sending data sent/required by Android app and Raspberry Pi.
* Utilized Amazon Relational Database Service to keep track of student attendance records for various classes.
* Built an Android app for student registration, and for tracking MAC address every time the student enters the class and turns on cell phone’s Bluetooth, in order to mark the student’s attendance.
