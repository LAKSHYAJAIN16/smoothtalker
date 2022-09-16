import json


MERGE_LINES = ["lines.json", "lines2.json"]
MERGE_LINKS = ["links.json", "links2.json"]

lines = []
for i in MERGE_LINES:
    data = json.load(open(i, "r+"))
    for j in data:
        lines.append(j)

links = []
for k in MERGE_LINKS:
    data = json.load(open(k, "r+"))
    for l in data:
        links.append(l)


linesJSON = json.dump(lines, open("final_lines.json", "w+"))
linksJSON = json.dump(links, open("final_links.json", "w+"))
print("done")