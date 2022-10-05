import tkinter
import subprocess
from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as font
from PIL import ImageTk, Image
import urllib.request
from urllib import parse
from io import BytesIO
import os
import io
import sys
import pickle
import time
from decimal import *
import webbrowser
# from click import command
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from datetime import timedelta  
import dateutil.relativedelta
from datetime import timedelta, date
import locale
import ssl
import random
import re #HKN
from functools import partial #HKN
global upload_path

ssl._create_default_https_context = ssl._create_unverified_context

#check local date format
locale.setlocale(locale.LC_ALL, '')
lastdate = date(date.today().year, 12, 31)

root = Tk()
root.geometry('750x850')
root.title("NFT AutoSeller")
input_save_list = ["NFTs folder :", 0, 0, 0, 0, 0, 0, 0, 0, 0]
main_directory = os.path.join(sys.path[0])
print("NFT autoseller start")

def supportURL():
    webbrowser.open_new("https://www.infotrex.net/opensea/support.asp?r=app")

def coffeeURL():
    webbrowser.open_new("https://github.com/infotrex/bulk-upload-to-opensea/#thanks")

def save_duration():
    duration_value.set(value=duration_value.get())

def save_file_path():
    return os.path.join(sys.path[0], "Save_gui.cloud") 

def is_numeric(val):
	if str(val).isdigit():
		return True
	elif str(val).replace('.','',1).isdigit():
		return True
	else:
		return False

def check_exists_by_xpath(driver, xpath):
    try:
        # driver.find_element_by_xpath(xpath)
        driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        return False
    return True

class InputField:
    def __init__(self, label, row_io, column_io, pos, txt_width=60, master=root):
        self.master = master
        self.input_field = Entry(self.master, width=txt_width)
        self.input_field.grid(ipady=3)
        self.input_field.label = Label(master, text=label, anchor="w", width=20, height=1 )
        self.input_field.label.grid(row=row_io, column=column_io, padx=12, pady=2)
        self.input_field.grid(row=row_io, column=column_io + 1, padx=12, pady=2)
        
        try:
            with open(save_file_path(), "rb") as infile:
                new_dict = pickle.load(infile)
                self.insert_text(new_dict[pos])
        except FileNotFoundError:
            pass
        
    def insert_text(self, text):
        self.input_field.delete(0, "end")
        self.input_field.insert(0, text)

    def save_inputs(self, pos):
        #messagebox.showwarning("showwarning", "Warning")
        input_save_list.insert(pos, self.input_field.get())
        #print(self.input_field.get())
        with open(save_file_path(), "wb") as outfile:
            pickle.dump(input_save_list, outfile)
            
    def validate_inputs(self, maxlen, type, message):

        if type == 0 and (len(self.input_field.get()) == 0 or (self.input_field.get()).isdigit() != True or len(self.input_field.get()) > maxlen):
            messagebox.showwarning("showwarning", message)
                
        elif type == 1 and (len(self.input_field.get()) == 0 or is_numeric(self.input_field.get()) == False or len(self.input_field.get()) >= maxlen):
            messagebox.showwarning("showwarning", message)       
                
        elif type == 2 and ( len(self.input_field.get()) == 0 or len(self.input_field.get()) > maxlen):
            messagebox.showwarning("showwarning", message)
               
        else:
            return True     

###input objects###
collection_link_input = InputField("OpenSea Collection Link:", 2, 0, 1)
start_num_input = InputField("Start Number:", 3, 0, 2)
end_num_input = InputField("End Number:", 4, 0, 3)
price = InputField("Default Price:", 5, 0, 4)
project_path = main_directory
chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'

def open_chrome_profile():
    print('chrome open')
    
    subprocess.Popen(
        [
            chrome_path,
            "--remote-debugging-port=9222",
            "--user-data-dir=" + project_path + "/chrome_profile",
        ],
        shell=True,
    )
    
def main_program_loop():

    if len(end_num_input.input_field.get()) > 5 :
        messagebox.showwarning("showwarning", "Start / end number range 0 - 99999")
        sys.exit()

    collection_link = collection_link_input.input_field.get()
    start_num = int(start_num_input.input_field.get())
    end_num = int(end_num_input.input_field.get())
    loop_price = float(price.input_field.get())

    print('driver open')
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(project_path+"\chromedriver.exe",options=options)
    
    wait = WebDriverWait(driver, 60)
    ###wait for methods
    def wait_css_selector(code):
        wait.until(
            ExpectedConditions.presence_of_element_located((By.CSS_SELECTOR, code))
        )

    def wait_xpath(code):
        wait.until(ExpectedConditions.presence_of_element_located((By.XPATH, code)))
            
    def delay(waiting_time=30):
            driver.implicitly_wait(waiting_time)

    Lines = []
    while end_num >= start_num:
        if is_numformat.get():
            start_numformat = f"{ start_num:04}"
        else:
            start_numformat = f"{ start_num:01}"
        #HKN S Only Listing
        listing_item_name = ""
        print("Start Selling NFT " + str(start_numformat))
        print('number ',  start_numformat)
        driver.get(collection_link+"/"+str(start_num))

        #HKN S
        wait_E = True
        while wait_E:
            try:
                WebDriverWait(driver, 20).until(ExpectedConditions.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Add properties']" )))
                wait_E = False
            except:
                print("Refresh")
                with open(os.path.join(sys.path[0], "Log.txt"),  'a') as outputfile:  # Use file to refer to the file object
                    outputfile.write("Starting Point This Page Needed To Be Refreshed \n")
                driver.get(collection_link+"/"+str(start_num))
                time.sleep(5)
                wait_E = True    
        #HKN F

        main_page = driver.current_window_handle
        if is_listing.get():
            time.sleep(2)
            try:
                wait_xpath('//a[text()="Sell"]')
                sell = driver.find_element(By.XPATH, '//a[text()="Sell"]')
                driver.execute_script("arguments[0].click();", sell)
            except:
                if "https://opensea.io/assets" in str(driver.current_url):
                    driver.get(driver.current_url +"/sell")
                else:
                    return
            
            wait_css_selector("input[placeholder='Amount']")
            amount = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Amount']")
            amount.send_keys(str(loop_price))

            #duration
            duration_date = duration_value.get()
            #print(duration_date)
            
            #if duration_date != 30:
            amount.send_keys(Keys.TAB)
            
            wait_xpath('//*[@role="dialog"]/div[1]/div[1]/div/input')
            select_durationday = driver.find_element(By.XPATH, '//*[@role="dialog"]/div[1]/div[1]/div/input')
            select_durationday.click()
            if duration_date == 1 : 
                range_button_location = '//span[normalize-space() = "1 day"]'
            if duration_date == 3 : 
                range_button_location = '//span[normalize-space() = "3 days"]'
            if duration_date == 7 : 
                range_button_location = '//span[normalize-space() = "7 days"]'
            if duration_date == 30 : 
                range_button_location = '//span[normalize-space() = "1 month"]'    
            if duration_date == 90 : 
                range_button_location = '//span[normalize-space() = "3 months"]' 
            if duration_date == 180 : 
                range_button_location = '//span[normalize-space() = "6 months"]'     

            wait.until(ExpectedConditions.presence_of_element_located(
                (By.XPATH, range_button_location)))
            ethereum_button = driver.find_element(
                By.XPATH, range_button_location)
            ethereum_button.click()
            select_durationday.send_keys(Keys.ENTER)

            delay()
            wait_css_selector("button[type='submit']")
            listing = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            driver.execute_script("arguments[0].click();", listing)
            
            #HKN S
            wait_E = True
            while wait_E:
                try:
                    wait_xpath('//div[@role="dialog"]//h4[contains(text(), "Complete your listing")]')#HKN
                    wait_E = False
                except:
                    wait_css_selector("button[type='submit']")
                    listing = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                    driver.execute_script("arguments[0].click();", listing)
                    wait_E = True    
            #HKN F
            
            login_page=""#HKN
            time.sleep(2)#HKN

            for handle in driver.window_handles:
                if handle != main_page:
                    login_page = handle
                    #break
            #HKN S
            wait_E = True
            attempts_n = 1
            while wait_E:
                if login_page !="":
                    driver.switch_to.window(login_page)
                    wait_E = False
                else:
                    time.sleep(2)
                    if len(driver.window_handles) == 2:
                        for handle in driver.window_handles:
                            if handle != main_page:
                                login_page = handle
                    elif attempts_n > 4:
                        try:
                            #WebDriverWait(driver, 3).until(ExpectedConditions.presence_of_element_located((By.XPATH, '//div[@role="dialog"]//h4[contains(text(), "Complete your listing")]')))#HKN
                            wait_css_selector("button[type='submit']")
                            listing = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
                            driver.execute_script("arguments[0].click();", listing)
                        except:
                            print("i can't click")
                    attempts_n = attempts_n + 1
            
            try:
                driver.find_element(By.XPATH, "//*[@id='app-content']/div/div[2]/div/div[3]/div[1]").click()
                time.sleep(0.7)
            except:
                WebDriverWait(driver, 240).until(ExpectedConditions.presence_of_element_located((By.XPATH, "//div[@class='signature-request-message__scroll-button']")))#HKN
                wait_xpath("//div[@class='signature-request-message__scroll-button']")
                scrollsign = driver.find_element(By.XPATH, "//div[@class='signature-request-message__scroll-button']")
                driver.execute_script("arguments[0].click();", scrollsign)
                time.sleep(0.7)
            try:
                wait_xpath('//*[@id="app-content"]/div/div[2]/div/div[4]/button[2]')
                driver.find_element(By.XPATH, '//*[@id="app-content"]/div/div[2]/div/div[4]/button[2]').click()
                time.sleep(0.7)
            except:
                wait_xpath('//button[text()="Sign"]')
                metasign = driver.find_element(By.XPATH, '//button[text()="Sign"]')
                driver.execute_script("arguments[0].click();", metasign)
                time.sleep(0.7)
            with open(os.path.join(sys.path[0], "Log_Listing.txt"),  'a') as outputfile:  # Use file to refer to the file object
                outputfile.write(listing_item_name + "\n")
  
        #change control to main page
        driver.switch_to.window(main_page)
        time.sleep(1)

        start_num = start_num + 1
        print('NFT sell completed!')
        time.sleep(2)
    
    driver.get("https://www.opensea.io")


  
def collection_scraper():#HKN
    
    collection_links=[]
    first_top_list=[]
    line_count=0

    project_path = main_directory
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("debuggerAddress", "localhost:8989")
    driver = webdriver.Chrome(executable_path=project_path + "/chromedriver.exe",options=options)
    wait = WebDriverWait(driver, 60)
    #driver.get(driver.current_url+"?search[sortAscending]=true&search[sortBy]=CREATED_DATE")# collection link
    print("Wait 55 Seconds")
    #time.sleep(55)
    for sny in range(55):
        print(str(55-sny))
        time.sleep(1)

    #wait = WebDriverWait(driver, 60)
    def wait_xpath(code):
        wait.until(ExpectedConditions.presence_of_element_located((By.XPATH, code)))

    my_divs = WebDriverWait(driver, 120).until(ExpectedConditions.presence_of_all_elements_located((By.XPATH, '//div[@role="gridcell" or @role="card"][contains(@style,"top")]')))

    for my_div in my_divs:
        #print(my_div.value_of_css_property("top"))
        top_list_item =int(my_div.value_of_css_property("top").replace("px", ""))
        if(top_list_item > 0):
            first_top_list.append(top_list_item)
        elif(top_list_item == 0):
            line_count = line_count + 1

    find_min = min(first_top_list)
    control_line = len(set(first_top_list))-1
    Top_value = 0

    next_nft = driver.find_element(By.XPATH, '//div[@role="gridcell"  or @role="card"][contains(@style,"top: '+ str(Top_value) +'px")]')
    driver.execute_script("arguments[0].scrollIntoView(true);",next_nft)
    print("Wait 5 Seconds")
    time.sleep(5)

    #total_items=int(Total_Items.input_field.get()) #HKN
    #collection_count_text = driver.find_element(By.XPATH, '//div[@class="AssetSearchView--results-count"]/p').text
    collection_count_text = driver.find_element(By.XPATH, '//div[@class="AssetSearchView--results collection--results AssetSearchView--results--phoenix"]//p').text
    c_num = ""
    for c in collection_count_text:
        if c.isdigit():
            c_num = c_num + c
    total_items = int(c_num)

    total_line =3
    if int(total_items/line_count) != (total_items/line_count):
        total_line = int(total_items/line_count) +1
    else:
        total_line = total_items/line_count

    for my_line in range(total_line):#total_line or some integer like 20
        #presence_of_all_elements_located
        if my_line !=0 and my_line%50==0:
            for sny in range(60):
                print(str(60-sny))
                time.sleep(1)

        if my_line<(total_line-control_line-1):
            WebDriverWait(driver, 120).until(ExpectedConditions.visibility_of_all_elements_located((By.XPATH, '//div[@role="gridcell" or @role="card"][contains(@style,"top: '+ str(Top_value + find_min * control_line) +'px")][last()='+str(line_count)+']')))
        elif my_line == (total_line-control_line-1):
            print("Wait  30 Seconds")
            time.sleep(30)

        last_string='[last()='+str(line_count)+']'
        if (my_line + 1) == total_line:
            last_string =""
        nftler = WebDriverWait(driver, 120).until(ExpectedConditions.visibility_of_all_elements_located((By.XPATH, '//div[@role="gridcell" or @role="card"][contains(@style,"top: '+ str(Top_value) +'px")]'+ last_string)))
        for my_nft in nftler:
            #for sayi in range(5):
                #WebDriverWait(driver, 120).until(ExpectedConditions.visibility_of_all_elements_located((By.XPATH, '//div[@role="gridcell" or @role="card"][contains(@style,"top: '+ str(Top_value) +'px")]['+str(sayi+1)+']//div[@class="AssetCardFooter--name"][string-length(text()) > 0]' )))
            wait_E = True
            while wait_E:
                try:
                    #nft_Name = my_nft.find_element(By.XPATH, './/div[@class="AssetCardFooter--name"]').text
                    nft_Name = my_nft.find_element(By.XPATH, './/a//img').get_attribute('alt')
                    nft_Link = my_nft.find_element(By.XPATH, './/a').get_attribute('href')
                    print(my_nft.find_element(By.XPATH, './/a').get_attribute('href'))
                    with open(os.path.join(sys.path[0], "Scraper.txt"),  'a') as outputfile:  # Use file to refer to the file object
                        outputfile.write(nft_Name + "," + nft_Link + "\n")
                    wait_E = False
                except:
                    print("Nftnin bir bilgisi bulunamadı tekrar deneniyor")
                    wait_E = True
            
            #time.sleep(0.1)
        print("My Line : " + str(my_line))
        if (my_line + 1) != total_line:
            Top_value = Top_value + find_min
            WebDriverWait(driver, 120).until(ExpectedConditions.presence_of_element_located((By.XPATH, '//div[@role="gridcell" or @role="card"][contains(@style,"top: '+ str(Top_value) +'px")]')))
            next_nft = driver.find_element(By.XPATH, '//div[@role="gridcell" or @role="card"][contains(@style,"top: '+ str(Top_value) +'px")]')
            driver.execute_script("arguments[0].scrollIntoView(true); window.scrollBy(0,60);",next_nft) 
        #time.sleep(2)
        
        #driver.execute_script('element = document.body.querySelector("style[top="'+ str(Top_value) +'px"]"); element.scrollIntoView();')

        #my_script = """myInterval = setInterval(function() {document.documentElement.scrollTop +="""+str(Top_value/4)+""";}, 500);
        #setTimeout(function() {clearInterval(myInterval)}, 2000);
        #"""
        #driver.execute_script(my_script)
        #driver.execute_script('document.documentElement.scrollTop +='+ str(Top_value))
        #time.sleep(10)

def remove_duplicates(liste):
    liste2 = []
    if liste: 
        for item in liste:
            if item not in liste2:
                liste2.append(item)
    else:
        return liste
    return liste2
   
def modify_Scrape_txt():#HKN
    
    def num_sort(test_string):
        return list(map(int, re.findall(r'(?<=#)(.*)(?=,)', test_string)))[0]
    Lines = []
    with open(os.path.join(sys.path[0], "Scraper.txt"),  'r') as scraped_list:  # Use file to refer to the file object
        #scraped_list.seek(0)
        Lines = scraped_list.readlines()
        Lines = remove_duplicates(Lines)
        Lines.sort(key=num_sort)   
        #Lines = remove_duplicates(Lines).sort()
    with open(os.path.join(sys.path[0], "modified_Scraper.txt"),  'a') as outputfile:  # Use file to refer to the file object
        for line in Lines:
            outputfile.write(str(line))
                
is_listing = BooleanVar()
is_listing.set(True) 

is_numformat = BooleanVar()
is_numformat.set(False) 

duration_value = IntVar()
duration_value.set(value=180)
duration_date = Frame(root, padx=0, pady=1)
duration_date.grid(row=15, column=1, sticky=(N, W, E, S))
tk.Radiobutton(duration_date, text='1 day', variable=duration_value, value=1, anchor="w", command=save_duration, width=6,).grid(row=0, column=1)
tk.Radiobutton(duration_date, text="3 days", variable=duration_value, value=3, anchor="w", command=save_duration, width=6, ).grid(row=0, column=2)
tk.Radiobutton(duration_date, text="7 days", variable=duration_value, value=7, anchor="w", command=save_duration, width=6,).grid(row=0, column=3)
tk.Radiobutton(duration_date, text="30 days", variable=duration_value, value=30, anchor="w", command=save_duration, width=7,).grid(row=0, column=4)
tk.Radiobutton(duration_date, text="90 days", variable=duration_value, value=90, anchor="w",command=save_duration,  width=7,).grid(row=0,  column=5)
tk.Radiobutton(duration_date, text="180 days", variable=duration_value, value=180, anchor="w", command=save_duration, width=7).grid(row=0, column=6)
duration_date.label = Label(root, text="Duration:", anchor="nw", width=20, height=2 )
duration_date.label.grid(row=15, column=0, padx=12, pady=0)
open_browser = tkinter.Button(root, width=50, height=1,  text="Open Chrome Browser", command=open_chrome_profile)
open_browser.grid(row=23, column=1, pady=2)
button_start = tkinter.Button(root, width=44, height=2, bg="green", fg="white", text="Start", command=partial(main_program_loop))#command=lambda: main_program_loop("Full")
button_start['font'] = font.Font(size=10, weight='bold')
button_start.grid(row=25, column=1, pady=2)

#####BUTTON ZONE END#######
root.mainloop()
