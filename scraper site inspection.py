"""
Importing the libraries that we are going to use
for loading the settings file and scraping the website
"""
import configparser
import time
import re
import os
import datetime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

profile_txt = "C:/Users/tijesunimi.adebiyi/AppData/Roaming/Mozilla/Firefox/Profiles/9e6o8d2n.scraping"
profile = FirefoxProfile(profile_txt)
binary = FirefoxBinary("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
driver = None

def load_settings():
    """
    Loading and assigning global variables from our settings.txt file
    """
    config_parser = configparser.RawConfigParser()
    config_file_path = 'settings.txt'
    config_parser.read(config_file_path)

    browser = config_parser.get('config', 'BROWSER')
    browser_path = config_parser.get('config', 'BROWSER_PATH')
    name = config_parser.get('config', 'NAME')
    page = config_parser.get('config', 'PAGE')

    settings = {
        'browser': browser,
        'browser_path': browser_path,
        'name': name,
        'page': page
    }
    return settings


def load_driver(settings):
    """
    Load the Selenium driver depending on the browser
    (Edge and Safari are not running yet)
    """
    driver = ''
    if settings['browser'] == 'firefox':
        
        #driver = webdriver.Firefox(firefox_profile)
        driver = webdriver.Firefox(firefox_profile=profile, firefox_binary=binary)
    elif settings['browser'] == 'edge':
        pass
    elif settings['browser'] == 'chrome':
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--user-data-dir=./User_Data')
        driver = webdriver.Chrome(chrome_options=chrome_options)
    elif settings['browser'] == 'safari':
        pass

    return driver


def search_chatter(driver, settings):
    """
    Function that search the specified user and activates his chat
    """
    
    #while True:
        
    wait = WebDriverWait(driver, 120)
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@class='_1c8mz _1YoG6']")))
    
    chatterwindow = driver.find_element_by_xpath("//div[@class='_1c8mz _1YoG6']")
    
    while(True):
        driver.execute_script('arguments[0].scrollBy(0,200)', chatterwindow)
        
        chatters = driver.find_elements_by_xpath("//div[@class='X7YrQ']")
        try:
            for chatter in chatters:
                chatter_name = chatter.find_element_by_xpath(
                    ".//span[@class='_19RFN _1ovWX _F7Vk']").text
                if chatter_name == settings['name']:
                    chatter.find_element_by_xpath(
                        ".//div[contains(@class,'_2UaNq')]").click()
                    return
        except StaleElementReferenceException:
            pass


def read_last_in_message(driver):
    """
    Reading the last message that you got in from the chatter
    """
    
    time.sleep(15)
    messagesss = driver.find_element_by_xpath(".//div[@class='_1_keJ']")
    
    driver.execute_script('arguments[0].scrollTop(0)', messagesss)
    
    for messages in driver.find_elements_by_xpath("//div[contains(@class,'message-in')]"):
        try:
            message = ""
            emojis = []

            message_container = messages.find_element_by_xpath(
                ".//div[@class='copyable-text']")

            message = message_container.find_element_by_xpath(
                ".//span[contains(@class,'selectable-text invisible-space copyable-text')]"
            ).text
            
            

            for emoji in message_container.find_elements_by_xpath(
                    ".//img[contains(@class,'selectable-text invisible-space copyable-text')]"
            ):
                emojis.append(emoji.get_attribute("data-plain-text"))

        except NoSuchElementException:  # In case there are only emojis in the message
            try:
                message = ""
                emojis = []
                message_container = messages.find_element_by_xpath(
                    ".//div[@class='copyable-text']")

                for emoji in message_container.find_elements_by_xpath(
                        ".//img[contains(@class,'selectable-text invisible-space copyable-text')]"
                ):
                    emojis.append(emoji.get_attribute("data-plain-text"))
            except NoSuchElementException:
                pass

    return message, emojis

def getValues(driver):
    '''
    Get the inspections from the site

    Parameters
    ----------
    driver : TYPE
        DESCRIPTION.

    Returns
    -------
    inspections : TYPE
        DESCRIPTION.

    '''
    
    no = 0 
    
    inspections = [] 
    inspection =[None,None ,None] 
    
    #time.sleep(5)   
    time.sleep(5)
    messagebox = driver.find_element_by_xpath("//div[@class='_1_keJ']") 
    
    driver.execute_script('arguments[0].scrollTo(0,0)', messagebox)
    time.sleep(8)
    messages = []
    fails = []
    while len(messages) < 200:
        time.sleep(5)
        driver.execute_script('arguments[0].scrollTo(0,0)', messagebox)
        messages = driver.find_elements_by_xpath("//div[contains(@class,'_2Wx_5 _3LG3B')]")
    
    
    driver.execute_script('arguments[0].scrollTo(0,0)', messagebox)
    time.sleep(5)
    messages = driver.find_elements_by_xpath("//div[contains(@class,'_2Wx_5 _3LG3B')]")
    
    #to get the messages
    for message in messages:
        try:
            author0 = message.find_element_by_xpath(".//div[contains(@class,'copyable-text')]")
           
                
            authorblk = author0.get_attribute('data-pre-plain-text')
            
            insp = message.find_element_by_xpath(
                    ".//span[contains(@class,'selectable-text invisible-space copyable-text')]"
                ).text
            lineList = insp.splitlines()
            line = -1
            try: #check if message is an update 
                 #i.e.site id is somewhere
                
                #because some people are making sily mistakes and disturbing my
                #site id  line
                #other possibilities are site ld, site 1d, ... add any more
                id_name_possible = ['site id', 'site ld', 'site 1d', 'slte id','s1te id']
                if any( name in lineList[0].lower().replace('.','') 
                       for name in id_name_possible): 
                    line= 0
                elif any( name in lineList[0].lower().replace('.','') 
                       for name in id_name_possible): 
                    line = 1
            except:
                print(authorblk + 'error not an update')
                pass
            
            
            
            #if message is ok
            if line != -1:
                try:
                    site_id = re.split(':|-| |;', lineList[line])[-1]
                    
                    authorblklist = re.split(",|]", authorblk.rstrip())
                    date = authorblklist[1]
                    author  = authorblklist[2].replace(':','')
            		
            	
                    inspection[0] =date
                    inspection[1] =author
                    inspection[2] = site_id
                    inspections.append(inspection.copy()) 
                    #print(inspection)
                    
                except: #if any parsing error comes around here
                    fails.append([authorblk,insp])
                    pass

                
            #print (str(no) +'\n')
            
            no = no+1
        except NoSuchElementException as ex:
            '''To do:
                I want to put messages that were not sorted out in a group'''
            print(ex)
            print(message.text)
            pass
        
    return inspections,fails

def from_fails(fails):
    print('List of fails')
    for fail in fails:
        print(fail[0]+'\n'+fail[1])


                
#-----------------------------
def from_ins(inspections):
    #Basically after getting the inspections, save it into a csv
    inspections_strlist = [" Date, FSE, Site ID"]
    
    for inspection in inspections:
        inspectioncsv =  ','.join(str(x) for x in inspection)
        inspections_strlist.append(inspectioncsv)
        
    inspections_all_csv =  '\n'.join(inspections_strlist)
    
    #print(inspections_all_csv)
    
    currentDT = datetime.datetime.now()
    
    insp_file_name = "Inspections" + currentDT.strftime("%H_%M, %b %d, %Y") + ".csv"
    insp_file = open(insp_file_name, 'w')
    insp_file.write(inspections_all_csv)
    insp_file.close()
    
    print('CSV file created')
    
    
    


def main():
    """
    Loading all the configuration and opening the website
    (Browser profile where whatsapp web is already scanned)
    """
    
    settings = load_settings()
    driver = load_driver(settings)
    driver.get(settings['page'])
    
    
        
    search_chatter(driver, settings)
    inspections,fails = getValues(driver)
    from_ins(inspections)
    from_fails(fails)
    
# =============================================================================
#     previous_in_message = None
#     while True:
#         last_in_message, emojis = read_last_in_message(driver)
# 
#         if previous_in_message != last_in_message:
#             print( last_in_message, emojis)
#             previous_in_message = last_in_message
# =============================================================================

    time.sleep(1)
  
   
    
    
    # while True:
    #     if input() == 'ok':
    #         driver.quit()
    #         exit()


if __name__ == '__main__':
    main()
