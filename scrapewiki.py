from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import *
import pandas as pd
import html.parser
import re
from PIL import Image
import requests

driver = webdriver.Chrome(executable_path='C:\Python39\Scripts\chromedriver')

namesList=[] #List to store name of the product
descriptionList=[] #List to store price of the product
categoryList=[]
imagesList=[] #List to store rating of the product

link = input("Insira o link da wikipédia: \n")
if "https://" in link:
    lang=link[8:10]
    print(lang)
    
else:
    lang=link[1:]
    print(lang)
    
driver.get(link)
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

name = soup.find('h1', attrs={'id':'firstHeading'})
name = name.text

for a in soup.findAll('div', attrs={'class':'mw-parser-output'}):
        description=''
        a = a.find('p')
        description+=a.get_text()
        break

try:
    for a in soup.findAll('td', attrs={'class':'infobox-image'}):
        image=a.find('img')
        image=image['src'][2:]
        print(image)
        break

    imagesList.append(image)

except:
    for a in soup.findAll('div', attrs={'class':'thumbinner', 'style':'width:262px;'}):
        image=a.find('img')
        image=image['src'][2:]
        print(image)
        break
        
    imagesList.append(image)

imageLink = 'http://' + image
imageAsFile = Image.open(requests.get(imageLink, stream=True).raw)
imageAsFile.save('wiki.png')
    
print(name)
print(description)

descriptionList.append(description)    
namesList.append(name)

driver.get('https://pageviews.toolforge.org/?project=%s.wikipedia.org&platform=all-access&agent=user&redirects=0&range=latest-20&pages=%s' %(lang, name.replace(" ", "_")))

element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "legend-block")))

content2 = element.get_attribute('innerHTML')
soup2 = BeautifulSoup(content2, 'html.parser')
views = []

for a in soup2.find_all('span', attrs={'class':'pull-right'}):
    views.append(a.get_text())
    
viewsTotal = views[0]
viewsPerDay = views[1]
viewsTotal = re.sub(r"[\n\t\s]*", "", viewsTotal)
viewsPerDay = re.sub(r"[\n\t\s]*", "", viewsPerDay)

data = {'Image': imagesList, 'Name': namesList, 'Description': descriptionList, 'Total views': viewsTotal, 'Average views per pay': viewsPerDay}

df = pd.DataFrame(data=data)
df.to_excel("all.xlsx")
df.to_json("all.json")

driver.quit()