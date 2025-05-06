# gosuslugi 

auto login + 2fa (sms) https://www.gosuslugi.ru

Install selenium and https://github.com/mozilla/geckodriver/releases/tag/v0.36.0
Correct path in a code


1) Connect android telephone to computer
2) Enter in the python code your login+password
3) Test connect:   adb shell content query --uri content://sms/inbox
4) 
```
python gosuslugi.py
```
5) Waiting autologin
