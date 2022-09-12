import requests
from bs4 import BeautifulSoup

# Total Pages
PAGES = 20
links = []

# Scrape Base Links
for i in range(1, PAGES):
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
        a = child.findChildren("div", recursive=False)[0].findChildren("div", recursive=False)[
            0].findChildren("figure", recursive=False)[0].findChildren("a", recursive=False)[0]
        href = a.get("href")
        links.append(href)
        # print(href)

    # print("\n")
    # print(str(i) + " done")

# Scrape Actual Lines
for link in links:
    # Scrape
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")

    # Find all Table Rows
    elements = soup.findAll('tr')
    for row in elements:
        td = row.findChild("td")
        print(td)