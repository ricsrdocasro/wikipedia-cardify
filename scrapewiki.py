from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import *
import pandas as pd
import html.parser
import re
from PIL import Image, ImageDraw, ImageFont
import requests
from contextlib import suppress

driver = webdriver.Chrome(executable_path='C:\Python39\Scripts\chromedriver')

namesList=[] #List to store name of the product
descriptionList=[] #List to store price of the product
categoryList=[]
imagesList=[] #List to store rating of the product

option = int(input("1-página aleatória\n2-link\n"))

if option == 1:
    link = "https://pt.wikipedia.org/wiki/Especial:Aleat%C3%B3ria"
elif option == 2:
    link = input("Insira o link da wikipédia: \n")
else:
    print("opção inválida!")
    raise Err
    
    
if "https://" in link:
    lang=link[8:10]
    print(lang)
    
else:
    lang=link[1:]
    print(lang)
    
driver.get(link)
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

for a in soup.findAll('p', attrs={'class':'coordinates'}):
    a.decompose()
    

for a in str(range(1, 100)):
    for a in soup.findAll('img', attrs={'width':a, 'height':a}):
        a.decompose()
    
for a in soup.findAll('table', attrs={'class':'noprint'}):
    a.decompose()

name = soup.find('h1', attrs={'id':'firstHeading'})
name = name.text

for a in soup.findAll('div', attrs={'id':'mw-normal-catlinks'}):
    for b in a.findAll('li'):
        category = b.find('a').get_text()
        
print(category)

for a in soup.findAll('div', attrs={'class':'mw-parser-output'}):
        description=''
        a = a.find('p')
        description+=a.get_text()
        break

print(soup.find('td', attrs={'class':'infobox-image'}))
      
with suppress(AttributeError):
    if soup.find('td', attrs={'class':'infobox-image'}) != None:
         for a in soup.findAll('td', attrs={'class':'infobox-image'}):
            image=a.find('img')
            image=image['src'][2:]
            print(image)

    elif soup.find('div', attrs={'class':'thumbinner', 'style':'width:262px;'}) != None:
        for a in soup.findAll('div', attrs={'class':'thumbinner', 'style':'width:262px;'}):
            image=a.find('img')
            image=image['src'][2:]
            print(image)


    elif soup.find('table', attrs={'class':'infobox_v2'}).find('img') != None:
        for a in soup.findAll('table', attrs={'class':'infobox'}):
            image=a.find('img')
            image=image['src'][2:]
            print(image)


    elif soup.find('table', attrs={'class':'toccolours'}) != None:
        for a in soup.findAll('table', attrs={'class':'toccolours'}):
            image=a.find('img')
            image=image['src'][2:]
            print(image)


    else:
        imageAsFile = Image.open('wikilogo.png')

#driver.find_element(By.XPATH, "//table[@class='infobox']/tbody/tr[1]/td/a/img")
##########################################################
    
try:
    imageLink = 'http://' + image
    imageAsFile = Image.open(requests.get(imageLink, stream=True).raw)
    
except:
    pass
    
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

driver.quit()

croppedDescription = description.split('. ')[0]

nameFont = ImageFont.truetype(r'C:/Windows/Fonts/Arial.ttf', 75)
descriptionFont = ImageFont.truetype(r'C:/Windows/Fonts/Arial.ttf', 27)
reducedNameFont = ImageFont.truetype(r'C:/Windows/Fonts/Arial.ttf', 60)
propsFont = ImageFont.truetype(r'C:/Windows/Fonts/Arial.ttf', 40)

W = 1090

if '.' in viewsTotal:
    viewsTotal = viewsTotal.split('.')[0] + viewsTotal.split('.')[1]

else:
    pass

if 0 <= int(viewsTotal) < 500:
    baseImage = Image.open('cartastandard.png')
    
elif 500 <= int(viewsTotal) < 1000:
    baseImage = Image.open('cartamuitointeressante.png')
    
elif 1000 <= int(viewsTotal) < 5000:
    baseImage = Image.open('cartasuperinteressante.png')

elif 5000 <= int(viewsTotal) < 10000:
    baseImage = Image.open('cartabrilhante.png')
    
else:
    baseImage = Image.open('cartaultrarrara.png')
    
imgResized = imageAsFile.resize((540, 540))
print(imageAsFile)    
back_im = baseImage.copy()
back_im.paste(imgResized, (275, 217))
im = ImageDraw.Draw(back_im)

y = 80



lines = text_wrap(name, nameFont, 1090)
    
for line in lines:
    w, h = im.textsize(line, font=nameFont)
    im.text(((W-w)/2, y), line, (0,0,0), font=nameFont)
    y += 60
    
    
lines = text_wrap(croppedDescription, descriptionFont, 900)

y = 800

for line in lines:
    im.text((100, y), line, (0,0,0), font=descriptionFont)
    y += 27
    
w, h = im.textsize(category, font=propsFont)
im.text(((W-w)/2, 1400), category, (0,0,0), font=propsFont)    
    
im.text((100, y+50), "Acessos totais: " + viewsTotal, (0,0,0), font=propsFont)
im.text((100, y+100), "Acessos por dia: " + viewsPerDay, (0,0,0), font=propsFont) 

back_im.show()
back_im.save('fullcard.png')
imageLink = ""
imageAsFile = ""