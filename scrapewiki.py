from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import *
import pandas as pd
import html.parser
import re

driver = webdriver.Chrome(executable_path='C:\Python39\Scripts\chromedriver')

namesList=[] #List to store name of the product
descriptionList=[] #List to store price of the product
categoryList=[]
imagesList=[] #List to store rating of the product


driver.get('https://en.wikipedia.org/wiki/Huilliche_people')
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

name=soup.find('h1', attrs={'id':'firstHeading'})
image=soup.find('img', attrs={'class':'pi-image-thumbnail'})

for a in soup.findAll('div', attrs={'class':'mw-parser-output'}):
    description=''
    a = a.find('p')
    description+=a.get_text()
    break
    
print(description)
    
descriptionList.append(description)    
namesList.append(name.text)

driver.get('https://pageviews.toolforge.org/?project=en.wikipedia.org&platform=all-access&agent=user&redirects=0&range=latest-20&pages=Huilliche_people')

element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "legend-block")))

print(element)
content2 = element.get_attribute('innerHTML')
print(content2)
soup2 = BeautifulSoup(content2, 'html.parser')
views = []

for a in soup2.find_all('span', attrs={'class':'pull-right'}):
    views.append(a.get_text())
    print(views)
    
viewsTotal = views[0]
viewsPerDay = views[1]
viewsTotal = re.sub(r"[\n\t\s]*", "", viewsTotal)
viewsPerDay = re.sub(r"[\n\t\s]*", "", viewsPerDay)
print(viewsTotal)
print(viewsPerDay)

data = {'Name': namesList, 'Description': descriptionList, 'Total views': viewsTotal, 'Average views per pay': viewsPerDay}

df = pd.DataFrame(data=data)
df.to_excel("all.xlsx")
df.to_json("all.json")

driver.quit()