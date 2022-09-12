import json
import requests
from bs4 import BeautifulSoup

# Total Pages
PAGES = 48
links = []
lines = []

# Scrape Base Links
for i in range(25, PAGES):
    # Scrape
    URL = "https://pickupline.net/page/" + str(i) + "?s=" 
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    
    # Get main content
    content = soup.find(id="main")
    
    # Get Children
    children = content.findChildren("article", recursive=False)
    for child in children:
        # Get href
        d = child.findChild("div", recursive=False)
        dd = d.findChild("div", recursive=False)
        figure = dd.findChild("figure", recursive=False)
        a = figure.findChild("a", recursive=False)
        href = a.get("href")
        links.append(href)
        # print(href)

    print("\n")
    print(str(i) + " done")

# Scrape Actual Lines
for link in links:
    # Scrape
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")

    # Find all Table Rows
    elements = soup.findAll('tr')
    for row in elements:
        td = row.findChild("td")
        txt = str(td)
        buf = ""
        started = False
        for char in txt:
            if char == ">":
                started = True
                continue

            if char == "<":
                started = False
                continue

            elif started == True:
                buf += char
        lines.append(buf)
    print("Done : ", link)
linesJSON = json.dump(lines, open("lines2.json", "w+"))
linksJSON = json.dump(links, open("links2.json", "w+"))