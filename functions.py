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
                try:
                    for check in sha_check_list:
                        logger.info("Checking :"+ check)
                        iniurl=config[check]['url']
                        hash=config[check]['hash']
                        xpath=config[check]['xpath']
                        attribute=config[check]['attribute']
                        element = driver.find_element_by_xpath(xpath)
                        if element.is_displayed():
                            logger.info(check + " is visible")
                        else:
                            error(check + "is NOT visible")
                        htmlurl=element.get_attribute(attribute)
                        if iniurl == htmlurl:
                            if sha_hash_check(htmlurl,hash,check):
                                logger.info(check+ " passed")
                        else:
                            error("URL not matching in the following check " + check)
                except Exception as e:
                    logger.exception(e)
            
            if config['link_list_url_check'].getboolean('do_check') == True:
                url_check_list = config['link_list_url_check']['list'].split(",")
                try:
                    for check in url_check_list:
                        logger.info("Checking :"+ check)
                        iniurl=config[check]['url']
                        xpath=config[check]['xpath']
                        attribute=config[check]['attribute']
                        element = driver.find_element_by_xpath(xpath)
                        if element.is_displayed():
                                logger.info(check + " is visible")
                        else:
                            error(check + "is NOT visible")
                        htmlurl=element.get_attribute(attribute)
                        if iniurl == htmlurl:
                            logger.info(check+ " passed")
                        else:
                            error("URL not matching in the following check " + check)
                        

                except Exception as e:
                    logger.exception(e)
        else:
            error("Website did a redirect to a different url." + "Expected: "+ websiteurl + ". Got: " + driver.current_url)
    except Exception as e:
        logger.exception(e)

def error(msg):
    logger.error(msg)
    if config['programconfig'].getboolean('matrix_alert') == True:
        send_matrix_msg(msg)


def sha_hash_check(url,hash,check):
    file_name=os.path.join("downloads/"+os.path.basename(urlparse(url).path))
    r = requests.get(url, stream=True)
    with open(file_name, 'wb') as f:
        for chunk in r.iter_content(32 * 1024):
            f.write(chunk)
    with open(file_name, 'rb') as f:
        content = f.read()
    sha = hashlib.sha256()
    sha.update(content)
    if sha.hexdigest() == hash:
        os.remove(file_name)
        return True
    else:
        time_file = file_name+str(time.time())
        shutil.move(file_name, time_file)
        error("Hash did not match in the following check " + check + ". Suspected file stored at location : " + time_file)
        return False
        
def send_matrix_msg(msg):
    token=config['matrixconfig']['accesstoken']
    roomid=config['matrixconfig']['roomid']
    server_url=config['matrixconfig']['server_url']
    data = '{"msgtype":"m.text", "body":"'+msg+'"}'
    r = requests.post(server_url+"_matrix/client/r0/rooms/"+roomid+"/send/m.room.message?access_token="+token, data = data)