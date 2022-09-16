import json
import requests
from bs4 import BeautifulSoup

# Total Pages
PAGES = 20
START_PAGE = 0
links = []
lines = []

# Scrape Base Links
for i in range(START_PAGE, PAGES):
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
    
    print(str(i) + " done")

# Scrape Actual Lines
for link in links:
    # Define Local Lines
    ourLines = []

    # Define Base url
    base_url = link

    # Remove the first 23 elements bcuz they're just the url stuff
    # Also remove the last char using rstrip (ikr python)
    base_intent = base_url[24:len(base_url)].rstrip()

    # Now, split the base intent into two parts according to the slash
    intents = base_intent.split("/")
    categorical_intent = intents[0]
    sub_intent = intents[1]

    # Remove the substring '-pickup-lines' and hyphens
    sub_intent = sub_intent.replace("-", " ").replace(" pick up lines", "")
    categorical_intent = categorical_intent.replace("-", " ").replace(" pick up lines", "")

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
        ourLines.append(buf)

    lines.append({"url": base_url, "categorical-intent": categorical_intent,
                 "intent": sub_intent, "lines": ourLines, "count": len(ourLines)})
    print("Done : ", link)

linesJSON = json.dump(lines, open("lines2.json", "w+"))
linksJSON = json.dump(links, open("links2.json", "w+"))