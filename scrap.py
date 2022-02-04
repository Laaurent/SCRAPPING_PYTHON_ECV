# pip install webdriver-manager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json

pageLimit = 25
totalResults = 0

articleList = []

color = {
    'NOIR' : '#000000',
    'GRIS' : '#919191',
    'BLANC': '#FFFFFF',
    'CRÈME': '#F8F8E1',
    'BEIGE': '#F4E0C8',
    'ABRICOT': '#FFCC98',
    'ORANGE': '#FFA500',
    'CORAIL': '#FF8F2F',
    'ROUGE': '#CC3300',
    'BORDEAUX': '#AE2E3D',
    'ROSE': '#FF0080',
    'VIOLET': '#800080',
    'LILA': '#D297D2',
    'BLEU CLAIR': '#89CFF0',
    'BLEU': '#007BC4',
    'MARINE': '#35358D',
    'TURQUOISE': '#B7DEE8',
    'MENTHE': '#AEFFBC',
    'VERT': '#369A3D',
    'VERT FONCÉ': '#356639',
    'KAKI': '#86814A',
    'MARRON': '#663300',
    'MOUTARDE': '#E5B539',
    'JAUNE': '#FFF200',
    'ARGENTÉ': '#919191',
    'DORÉ': '#FFF200',
    'MULTICOLORE': '#000000'
}

url = 'https://www.vinted.fr/vetements?brand_id[]=872289&catalog[]=34&price_to=20&currency=EUR&order=newest_first&page='

file=open('main.html','w')
file.write('''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <title>Python parsing</title>
</head>
<body>''')

for page in range(1,2):

    s=Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver.get(url + str(page))

    priceResult = driver.find_elements_by_xpath('//h3[@class="Text_text__QBn4- Text_subtitle__1I9iB Text_left__3s3CR Text_amplified__2ccjx Text_bold__1scEZ"]')
    sizeResult = driver.find_elements_by_xpath('//div[@class="ItemBox_subtitle__1SPGe"]')
    urlResult = driver.find_elements_by_xpath('//a[@class="ItemBox_overlay__1kNfX"]')
    
    totalResults += len(priceResult)

    for p in range(1,len(priceResult)):
        s=Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s)
        driver.get(urlResult[p].get_attribute("href"))
        imgResult = driver.find_elements_by_xpath('//a[@class="item-thumbnail is-loaded"]')
        stateResult = driver.find_elements_by_xpath('//div[@itemprop="itemCondition"]')
        colorResult = driver.find_elements_by_xpath('//div[@itemprop="color"]')
        id = p+1+28*(page-1)
        id = id + page-1 if page > 1 else id 
        colors = colorResult[0].text.split(', ')
        colorArray = []
        for colorT in colors:
            colorArray.append(color[colorT])
        articleList.append({'id':id,'price' : priceResult[p].text,'size':sizeResult[p].text,'url':urlResult[p].get_attribute("href"),'img':imgResult[0].get_attribute("href"),'condition':stateResult[0].text,'color':colorArray})
        file.write(f'''
            <div class="d-flex  w-100 m-2">
                <div style="flex:2" class="m-4 p-4">
                    <ul>
                        <li>Price : {priceResult[p].text}</li>
                        <li>Size : {sizeResult[p].text}</li>
                        <li>Condition : {stateResult[0].text}</li>
                        <li>Color : {colorArray}</li>
                        <li><a href="{urlResult[p].get_attribute("href")}">See more</a></li>
                    </ul>
                </div>
                <div style="flex:1">
                    <img width="200" src="{imgResult[0].get_attribute("href")}"></img>
                </div>
            </div>
        ''')

driver.close()


jsonFile = open("db.json", "w")

db = json.dumps({"articles" : articleList})
jsonFile.write(db)

""" print(articleList) """
""" print(f'Total : {totalResults}') """

file.write('''  
</body>
</html>
''')

print("All done ✅")
  