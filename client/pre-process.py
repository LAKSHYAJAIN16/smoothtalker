import json

FILE_PATH = r"C:\Users\USER\Downloads\all_insta_messages (13).json"

# Scrape Content
f = open(FILE_PATH, "r+", encoding="UTF8")
content = json.loads(f.read())
f.close()

# To convert array to prompt:
def convert_to_prompt(array):
    return str(array)

# Loop through each thing
for k in content:
    # Compile prompt
    convert_to_prompt(k)
    