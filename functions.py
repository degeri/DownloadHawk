from conf import *
from log import *
from selenium import webdriver
from pyvirtualdisplay import Display
import requests
import hashlib
from urllib.parse import urlparse
import os
import shutil
import time
import socket

def visiturl(websiteurl):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", config['programconfig']['useragent'])
    driver = webdriver.Firefox(profile,executable_path=config['selenium']['geckobin'])
    driver.get(websiteurl)
    do_checks(driver,websiteurl)
    driver.close()




def do_checks(driver,websiteurl):
    try:
        if websiteurl == driver.current_url:
            if config['bin_list_url_sha_check'].getboolean('do_check') == True:
                sha_check_list = config['bin_list_url_sha_check']['list'].split(",")
                for check in sha_check_list:
                    try:
                        if element_checks(driver,check,True):
                            logger.info(check+ " passed")
                    except Exception as e:
                        logger.exception(e)
            
            if config['link_list_url_check'].getboolean('do_check') == True:
                url_check_list = config['link_list_url_check']['list'].split(",")
                for check in url_check_list:
                    try:
                        if element_checks(driver,check,False):
                            logger.info(check+ " passed")
                    except Exception as e:
                        logger.exception(e)

        else:
            error("Website did a redirect to a different url." + "Expected: "+ websiteurl + ". Got: " + driver.current_url)
    except Exception as e:
        logger.exception(e)

def element_checks(driver,check,do_sha):
    logger.info("Checking : "+ check)
    iniurl=config[check]['url']
    xpath=config[check]['xpath']
    attribute=config[check]['attribute']
    if do_sha:
        hash=config[check]['hash']
    try:
        element = driver.find_element_by_xpath(xpath)
    except Exception as e:
        logger.exception(e)
        error("Unable to find the element for " + check)
        return False
    if element.is_displayed():
        logger.info(check + " is visible")
    else:
        error(check + "is NOT visible")
    htmlurl=element.get_attribute(attribute)
    if iniurl == htmlurl:
        if do_sha:
            if sha_hash_check(htmlurl,hash,check):
                return True
        else:
            return True
    else:
        error("URL not matching in the following check " + check + ".Expected:"+iniurl+ ". Got:"+htmlurl)


def error(msg):
    logger.error(msg)
    if config['programconfig'].getboolean('matrix_alert') == True:
        send_matrix_msg(msg)


def sha_hash_check(url,hash,check):
    file_name=os.path.join("downloads/"+os.path.basename(urlparse(url).path))
    max_download_retry = config['programconfig']['max_download_retry']
    for i in range(int(max_download_retry)):
        try:
            r = requests.get(url, stream=True, timeout=10)
            if r.status_code == 200:
                idx = 1
                with open(file_name, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            idx += 1
                break
            else:
                time.sleep(70)
        except requests.exceptions.ConnectionError:
            logger.error("HTTP connection failed for "+ url)
            time.sleep(10)
        except socket.timeout:
            logger.error("Socket Timeout for " + url)
            time.sleep(10)
    else:
        logger.error("Tried " + max_download_retry + " times to download " + url + " failed")
        if os.path.isfile(file_name):
            try:
                os.remove(file_name)
            except Exception as e:
                logger.exception(e)
        return False
    if os.path.isfile(file_name):
        with open(file_name, 'rb') as f:
            content = f.read()
        sha = hashlib.sha256()
        sha.update(content)
        download_hash = sha.hexdigest()
        if download_hash == hash:
            os.remove(file_name)
            return True
        else:
            hash_file = file_name+str(download_hash)
            shutil.move(file_name, hash_file)
            error("Hash did not match in the following check " + check + ". Expected:"+ hash + " Got:"+ download_hash +" .Suspected file stored at location : " + hash_file+" Size :"+ str(os.path.getsize(hash_file)/1048576) + "MB")
            return False
        
def send_matrix_msg(msg):
    token=config['matrixconfig']['accesstoken']
    roomid=config['matrixconfig']['roomid']
    server_url=config['matrixconfig']['server_url']
    data = '{"msgtype":"m.text", "body":"'+msg+'"}'
    r = requests.post(server_url+"_matrix/client/r0/rooms/"+roomid+"/send/m.room.message?access_token="+token, data = data)