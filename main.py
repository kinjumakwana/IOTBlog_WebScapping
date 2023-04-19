from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.db import IntegrityError
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
import csv
import re 

s = Service(r"D:\Kinjal\chromedriver_win32\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
# driver = webdriver.Chrome(service=s, options=options)

class IOTblog:
    def __init__(self):
        self.driver = webdriver.Chrome(service=s, options=options)
        sleep(5)
        # self.driver = webdriver.Chrome(chrome_driver_path)

    def blogdata(self):
        data={}
        Blog_dict={}
        try:
            self.driver.maximize_window()
            self.driver.get("https://blogs.cisco.com/internet-of-things")
            sleep(5)
            
            ifpagination = True
            blogs_data = []
            while ifpagination:
                # sleep(10)
                data = self.driver.find_elements(By.CLASS_NAME,"blog-card")
                totalblogonpage = len(data)
                # print("totalblogonpage: ",totalblogonpage)
                
                # for data in data:
                #     print(data.text)#first page all blog data
                #     # cardlinks= WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "card-link")))

                cardlinks = self.driver.find_elements(By.CLASS_NAME,"card-link")
                totalbloglink = len(cardlinks)
                # print("totalbloglink: ",totalbloglink)
                
                # for cardlink in cardlinks:
                for i in range(totalbloglink):
                 
                    # print(cardlink.text)
                    cardlinks = self.driver.find_elements(By.CLASS_NAME,"card-link")
                    cardlink = cardlinks[i]
                    # print(cardlink.text)
                    
                    # Scroll the link into view
                    self.driver.execute_script("arguments[0].scrollIntoView();", cardlink)

                    # Click the link using JavaScript
                    action = ActionChains(self.driver)
                    action.move_to_element(cardlink).click().perform()
                    
                    Blog_dict = {}
                    title = self.driver.find_element(By.CLASS_NAME,"entry-title")
                    # print("Title: ",title.text)
                    Blog_dict["Title"] = title.text
                    
                    author = self.driver.find_element(By.XPATH,"/html/body/cdc-template-micro/div/div[1]/div/main/article/div/div[1]/div[2]/p/a")
                    # print("Author: ",author.text)
                    Blog_dict["Author"] = author.text
                    
                    description = self.driver.find_element(By.CLASS_NAME,"entry-content")
                    # print("Description: ",description.text.encode('utf8'))
                    Blog_dict["Description"] = description.text.encode('utf8')
                    
                    tags = self.driver.find_element(By.ID,"tags-container")
                    # print("Tags: ",tags.text)
                    Blog_dict["Tags"] = tags.text
                    
                    postdate = self.driver.find_element(By.CLASS_NAME,"entry-meta")
                    # print("postdate: ",postdate.text)
                    date = postdate.text
                    blogdate = date.split("\n")[0]
                    # print("Blogdate:",blogdate)
                    Blog_dict["Blogdate"] = blogdate
                    
                    img_element = self.driver.find_element(By.XPATH,"//div[@class='post-thumbnail']/img")
                    img_url = img_element.get_attribute("src")
                    # print(img_url)
                    Blog_dict["Image"] = img_url
                    
                    # Append this blog's data dictionary to the list
                    blogs_data.append(Blog_dict)
                    # print(blogs_data)
                   
                    df = pd.DataFrame(blogs_data)
                    # print(df)
                   
                    # Go back to the previous page
                    self.driver.back()
                    # sleep(10)
                    
                    # Wait for the previous page to load
                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "blog-card")))

                df.to_csv('IOTBlog.csv')
                pagination = self.driver.find_element(By.CLASS_NAME,"pagination")
                # print(pagination.text)
                
                # locate the last pagination element
                last_page_link = self.driver.find_element(By.CSS_SELECTOR,'ul.pagination li:last-child a')
                # print(last_page_link.text)
                last_page_link.click()
                sleep(5)
                if last_page_link:
                    ifpagination = True
                else:
                    ifpagination = False
        except Exception as e:
            print(e)
            sleep(10)

IOTblogs = IOTblog()
IOTblogs.blogdata()
