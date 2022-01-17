from selenium import webdriver       #Main import from selenium
from selenium.webdriver.common.keys import Keys     #import to allow the program to access the keys
import time     #Needed to put the program to sleep so it does not crash
from bs4 import BeautifulSoup  #importing beautiful soup to make it easier with parsing html
import gspread      #import to allow the code to acess the speadsheet on google sheets
from oauth2client.service_account import ServiceAccountCredentials      #imports the account credentials for the drive API
from datetime import date  #Allow the code to write it in a proper date time manner

#setting up credientials and getting infromation from json file.
scope =["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]  #spreadsheet infromation from the API
creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\Users\\bhavs\\OneDrive\\Desktop\\Python30\\Project\\sheetscreds.json", scope) #using a Json file to access all the information
client = gspread.authorize(creds)

#getting the chrome path
#C:\Program Files (x86)\chromedriver.exe
path = "C:\\Users\\bhavs\\OneDrive\\Desktop\\Chrome Driver\\chromedriver"  #accesing the chrome driver for the code to work
driver = webdriver.Chrome(path)
champsWr = []       #creating an empty array 

#read the champions names from the txt file.
with open("C:\\Users\\bhavs\\OneDrive\\Desktop\\Python30\\Project\\ChampNames.txt", 'r') as champFile: #opening the file with the champ names
    xChamp = champFile.read().split()
    for champ in xChamp:

        driver.get("https://u.gg/")   #opening the site using drivers
        time.sleep(2)   #putting the code to sleep for 2 seconds
        search = driver.find_element_by_name("query")      #searching the HTML to find the search bar which is named "query"
        search.send_keys(champ)     #sending the search bar one of the champ names
        search.send_keys(Keys.ENTER)    #entering the name for it to search

        time.sleep(2)   #putting the code to sleep for 2 seconds

        content = driver.page_source.encode("utf-8").strip()    #getting all the infromation from the HTML source
        soup = BeautifulSoup(content, "html.parser")        #Using beautiful soup to parse all the data so we can use it
        winRate = soup.find_all('div', {'class':'win-rate okay-tier'})[0].findChildren()[0].string      #finding the winrate by searching for the "children" in the html page with the title "win-rate okay-tier"
        champsWr.append(winRate)    #appending the winrates of each champ into the empty array we created at the start
        time.sleep(2)   #putting the code to sleep for 2 seconds  

#closing the driver(google chrome page) and closing the file
champFile.close()
driver.quit()
 
#opening the google sheets and adding all the information
sheet = client.open("Python Project").sheet1  #opening the google sheets 
today = date.today()    #getting today's date
insertRow = [today.strftime("%d/%m/%y")] + champsWr     #inserting today's date and the champs winrate onto the google sheet
sheet.insert_row(insertRow, 2)      #inserting it onto the second row

print ("The information has been recorded!")    #message to let me know that the infromation has been correctly recorded. 