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

def text_wrap(text, font, max_width):
    lines = []
    # If the width of the text is smaller than image width
    # we don't need to split it, just add it to the lines array
    # and return
    if font.getsize(text)[0] <= max_width:
        lines.append(text)
    else:
        # split the line by spaces to get words
        words = text.split(' ')  
        i = 0
        # append every word to a line while its width is shorter than image width
        while i < len(words):
            line = ''        
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:                
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            # when the line gets longer than the max width do not append the word,
            # add the line to the lines array
            lines.append(line)    
    return lines

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
        
print(description)

print(soup.find('td', attrs={'class':'infobox-image'}))
        
if soup.find('td', attrs={'class':'infobox-image'}) == None:
     for a in soup.findAll('div', attrs={'class':'thumbinner', 'style':'width:262px;'}):
        image=a.find('img')
        image=image['src'][2:]
        print(image)
        break
    
else: # soup.find('td', attrs={'class':'infobox-image'}) != None:
    for a in soup.findAll('td', attrs={'class':'infobox-image'}):
        image=a.find('img')
        image=image['src'][2:]
        print(image)
        break

    imagesList.append(image)

#else:
    #imageBackup = Image.open('wikilogo.png')

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

#data = {'Image': imagesList, 'Name': namesList, 'Description': descriptionList, 'Total views': viewsTotal, 'Average views per pay': viewsPerDay}

#df = pd.DataFrame(data=data)
#df.to_excel("all.xlsx")
#df.to_json("all.json")

driver.quit()

croppedDescription = description.split('. ')[0]

nameFont = ImageFont.truetype(r'C:/Windows/Fonts/Arial.ttf', 75)
descriptionFont = ImageFont.truetype(r'C:/Windows/Fonts/Arial.ttf', 27)
reducedNameFont = ImageFont.truetype(r'C:/Windows/Fonts/Arial.ttf', 60)
propsFont = ImageFont.truetype(r'C:/Windows/Fonts/Arial.ttf', 40)


baseImage = Image.open('cartawiki.png')
imgResized = imageAsFile.resize((540, 540))
print(imageAsFile)

back_im = baseImage.copy()
back_im.paste(imgResized, (275, 240))
im = ImageDraw.Draw(back_im)

y = 50

if 0 <= len(name) <= 20:
    lines = text_wrap(name, nameFont, 900)
    
    for line in lines:
        im.text((325, y), name, (0,0,0), font=font)
        y += 75
        
else:
    lines = text_wrap(name, reducedNameFont, 900)
    
    for line in lines:
        im.text((325, y), name, (0,0,0), font=reducedNameFont)
        y += 60
    
    
lines = text_wrap(croppedDescription, descriptionFont, 900)

y = 920

for line in lines:
    im.text((100, y), line, (0,0,0), font=descriptionFont)
    y += 27
    
    
im.text((100, y+50), "Visualizações totais: " + viewsTotal, (0,0,0), font=propsFont)
im.text((100, y+100), "Visualizações por dia: " + viewsPerDay, (0,0,0), font=propsFont) 

viewsTotal = viewsTotal.split('.')[0] + viewsTotal.split('.')[1]

if 0 <= int(viewsTotal) < 500:
    im.text((850, 1400), "Interessante", (192,192,192), font=propsFont)
    
elif 500 <= int(viewsTotal) < 1000:
    im.text((850, 1400), "Muito Interessante", (0,255,255), font=propsFont)
    
elif 1000 <= int(viewsTotal) < 5000:
    im.text((850, 1400), "Super Interessante", (170,169,173), font=propsFont)

elif 5000 <= int(viewsTotal) < 10000:
    im.text((850, 1400), "Brilhante", (255,215,0), font=propsFont)
    
else:
    im.text((850, 1400), "Ultrarraro", (127,0,255), font=propsFont)

back_im.show()
back_im.save('fullcard.jpg')