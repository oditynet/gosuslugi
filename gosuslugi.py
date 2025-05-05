import subprocess
import re
import threading
import queue
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time


login="+712345678"
passwd="password"




def get_adb_devices():
    try:
        result = subprocess.run(
            ['adb', 'devices'],
            capture_output=True,
            text=True,
            timeout=5
        )
        lines = [line.strip() for line in result.stdout.split('\n')[1:] if line.strip()]
        for line in lines:
            if re.match(r'^\S+\tdevice$', line):
                return line.split('\t')[0]
        return None
    except Exception as e:
        print(f"ADB error: {str(e)}")
        return None

def get_sms():
    try:
        result = subprocess.run(
            ['adb', 'shell', 'content', 'query', '--uri', 'content://sms/inbox'],
            capture_output=True,
            text=True,
            timeout=3
        )
        messages = []
        for line in result.stdout.split('\n'):
            if 'body=' in line and 'date=' in line:
                date_match = re.search(r'date=(\d+)', line)
                body_match = re.search(r'body=(.+?), service_center', line)
                #print(body_match)
                if date_match and body_match:
                    timestamp = int(date_match.group(1)) // 1000
                    dt = datetime.fromtimestamp(timestamp)
                    body = body_match.group(1).strip()
                    messages.append((dt, body))
        return messages
    except Exception as e:
        print(f"SMS error: {str(e)}")
        return []

def is_recent(msg_time):
    return (datetime.now() - msg_time) < timedelta(minutes=1)

def loopsms(output_queue, check_interval=10):
    while True:
        try:
            device = get_adb_devices()
            if device:
                #print(f"Устройство подключено: {device}")
                messages = get_sms()
                if messages:
                    latest_time, latest_body = messages[0]
                    if is_recent(latest_time):
                        print(f"Новое сообщение: {latest_body}")
                        output_queue.put(latest_body[-6:])
                        break
                        #return  latest_body[:5]
                #    else:
                #        print("Новых сообщений нет")
                else:
                    print("Сообщения не найдены")
            else:
                print("Устройство не обнаружено")
            
            time.sleep(check_interval)
            
        except KeyboardInterrupt:
            print("\nМониторинг остановлен")
            break
        except Exception as e:
            print(f"Ошибка: {str(e)}")
            time.sleep(check_interval)


def sms_read():
    #sms_read_code
    message_queue = queue.Queue()
    monitor_thread = threading.Thread(
        target=loopsms,
        args=(message_queue,10),
        daemon=True
    )
    monitor_thread.start()
    ret=message_queue.get()
    monitor_thread.join(11)
    print(ret)
    return ret

if __name__ == "__main__":
    options = Options()
    options.set_preference("dom.webdriver.enabled", False)  # Скрываем автоматизацию  
    options.set_preference("useAutomationExtension", False)
    
    gecko_path="/home/odity/Downloads/geckodriver-v0.36.0-linux64/geckodriver"
    service = Service(executable_path=gecko_path,options=options)
    driver = webdriver.Firefox(service=service)
    driver.get(f"https://esia.gosuslugi.ru/login/")
    
    add = WebDriverWait(driver, 7).until(
    EC.visibility_of_element_located((By.ID, "login")) )
    add = add.send_keys(login)
    time.sleep(1)
    
    add =  driver.find_element(By.XPATH, "//input[@type='password']")
    add = add.send_keys(passwd)
    time.sleep(1)
    
    pyautogui.press('enter')      # Enter+
    #time.sleep(1)
    
    pin=sms_read()
    
    p1=pin[-6]
    p2=pin[-5]
    p3=pin[-4]
    p4=pin[-3]
    p5=pin[-2]
    p6=pin[-1]
    print(f"{p1} {p2} ... {p6}")
    add = WebDriverWait(driver, 1).until(  EC.element_to_be_clickable(    (By.XPATH, "//code-input//span[contains(@class, 'empty')][1]/input")    ))
    add.send_keys(p1)
    add = WebDriverWait(driver, 1).until(  EC.element_to_be_clickable(    (By.XPATH, "//code-input//span[contains(@class, 'empty')][1]/input")    ))
    add.send_keys(p2)
    add = WebDriverWait(driver, 1).until(  EC.element_to_be_clickable(    (By.XPATH, "//code-input//span[contains(@class, 'empty')][1]/input")    ))
    add.send_keys(p3)
    add = WebDriverWait(driver, 1).until(  EC.element_to_be_clickable(    (By.XPATH, "//code-input//span[contains(@class, 'empty')][1]/input")    ))
    add.send_keys(p4)
    add = WebDriverWait(driver, 1).until(  EC.element_to_be_clickable(    (By.XPATH, "//code-input//span[contains(@class, 'empty')][1]/input")    ))
    add.send_keys(p5)
    add = WebDriverWait(driver, 1).until(  EC.element_to_be_clickable(    (By.XPATH, "//code-input//span[contains(@class, 'empty')][1]/input")    ))
    add.send_keys(p6)
    
