import json

FILE_PATH = r"C:\Users\USER\Downloads\all_insta_messages (13).json"

# Scrape Content
f = open(FILE_PATH, "r+", encoding="UTF8")
content = json.loads(f.read())
f.close()

prompts = []

# To convert array to prompt:
def convert_to_prompt(array):
    prompt_starter = """# Task
    This is a conversation between a male and a female teenager on Instagram. The Male is trying to court the female and be as attractive as possible. You will be given the texts of the female and you need to generate the texts of the male.
    
    # Input
    {0}
    
    # Output
    {1}
    """
    inp = """Her : """
    output="""Him : """
    
    for k in array:
        splits = str(k).split("~~:")
        if splits[0] == "OTHER_PERSON":
            inp += splits[1].lower()
            inp += ". "
        else:
            output += splits[1].lower()
            output += ". "
              
    prompt = prompt_starter.format(inp, output)   
    return prompt

# Loop through each thing
m = 0
for k in content:
    # Compile prompt
    prompts.append(convert_to_prompt(k))
    m+=1
    print(m)
    
json.dump(prompts, open("prompts.json", "w"))
    