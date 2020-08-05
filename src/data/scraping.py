#Needed imports
# pip3 install lxml
# pip3 install howlongtobeatpy
# pip3 install beautifulsoup4
# pip3 install request
# pip3 install plotly
# pip3 install numpy
# pip3 install pandas
# pip3 install matplotlib
from howlongtobeatpy import HowLongToBeat
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import time
import requests 
import urllib
import urllib.request
import operator
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#Function to retrieve data from STEAM
def steamData(pageBegin, pageEnd):
  gamesNames = []
  gamesImages = []
  gamesDates = []
  gamesReviews = []
  gamesDiscounts = []
  gamesOriginalPrices = []
  gamesFinalPrices = []
  gamesReferences = []
  for pagenumber in range(pageBegin,pageEnd):
    soup = BeautifulSoup(urllib.request.urlopen('https://store.steampowered.com/search/?category1=998&page='+str(pagenumber)).read(), "lxml")
    gamesRows = soup.find_all("a",{"class": "search_result_row"})
    for game in gamesRows:
      gamesNames.append(game.find('span', {'class': 'title'}).get_text())
      gamesDates.append(game.find("div",{"class": "col search_released responsive_secondrow"}).get_text())
      if(game.find("span", {"class": "search_review_summary positive"}) != None):
        gamesReviews.append(game.find("span", {"class": "search_review_summary positive"})['data-tooltip-html'].replace("<br><br>This product has experienced one or more periods of off-topic review activity.  Based on your preferences, the reviews within these periods have been excluded from this product's Review Score." , '').replace('<br>', ', '))  
      else:
        gamesReviews.append('Unknown')
      if(game.find("div", {"class": "col search_discount responsive_secondrow"}).get_text().replace('\n', '') != ""):
        gamesDiscounts.append(game.find("div", {"class": "col search_discount responsive_secondrow"}).get_text().replace('\n', ''))
      else:
        gamesDiscounts.append("-0%")
      prices = game.find("div", {"class": "search_price"}).get_text().replace('\n', '').replace('\r', '').split('$')     
      if(len(prices) > 2):
        gamesOriginalPrices.append(prices[1])
        gamesFinalPrices.append(prices[2])
      elif(len(prices) == 1):
        gamesOriginalPrices.append(prices[0])
        gamesFinalPrices.append(prices[0])
      else:
        gamesOriginalPrices.append(prices[1])
        gamesFinalPrices.append(prices[1]) 
      gamesImages.append(game.find('img')['src'])
      gamesReferences.append(game['href'])
  df = pd.DataFrame()
  df["game"] = gamesNames
  df["date"] = gamesDates
  df["review"] = gamesReviews
  df["discount"] = gamesDiscounts
  df["original"] = gamesOriginalPrices
  df["final"] = gamesFinalPrices
  df["image"] = gamesImages
  df["href"] = gamesReferences
  return df

#Function to retrieve data from METACRITICS
def searchMetacritic(gameName):
  url = 'https://www.metacritic.com/game/pc/'+gameName.lower().replace(' ', '-').replace(':', '').replace('™', '').replace('®', '').replace("'", '')
  user_agent = {'User-agent': 'Mozilla/5.0'}
  response  = requests.get(url, headers = user_agent) 
  soup = BeautifulSoup(response.text, 'html.parser')
  if(soup.find('div', class_='metascore_w xlarge game positive') != None):
    return soup.find('div', class_='metascore_w xlarge game positive').getText()
  elif(soup.find('div', class_='metascore_w xlarge game mixed') != None):
    return soup.find('div', class_='metascore_w xlarge game mixed').getText()
  else:
    return "0"

#Function to retrieve data from HowLongToBeat
def searchHLTB(gameName):
  result = HowLongToBeat().search(gameName)
  best_element=0
  if result is not None and len(result) > 0:
    best_element = max(result, key=lambda element: element.similarity)
  if(isinstance(best_element, int)):
    return 'Unknown'
  return "Horas principal:"+str(best_element.gameplay_main)+'\n'+"  Horas principal+extra:" +str(best_element.gameplay_main_extra)+'\n'+"  Horas completo:"+str(best_element.gameplay_completionist)

#Initial function
def onInit():
  #Get the data from Steam
  print("Getting data from steam")
  with ProcessPoolExecutor() as executor:
    results = executor.map(steamData, [0], [1])
  df = pd.DataFrame()
  for i in list(results):
    df = pd.concat([df, i])
  print("Getting data from Meta and How")
  #Get metascore and time to complete from METACRITICS and HOWLONGTOBEAT
  with ThreadPoolExecutor(8) as executor:
    resultHLTB = executor.map(searchHLTB, df['game'].tolist())
    resultMC = executor.map(searchMetacritic, df['game'].tolist())
    df["time"] = list(resultHLTB)
    df["metascore"] = list(resultMC)
    #print(df)
    print("Creating file")
    df.to_json (r'data.json', orient='records')
    
onInit()
