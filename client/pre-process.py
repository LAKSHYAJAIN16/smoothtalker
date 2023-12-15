import json

FILE_PATH = r"C:\Users\USER\Projects\lj-llm\smoothtalker\all_insta_messages (14).json"

# Scrape Content
f = open(FILE_PATH, "r+", encoding="UTF8")
content = json.loads(f.read())
f.close()

prompts = []

# To convert array to prompt:
def convert_to_prompt(array):
    prompt_starter = """
    # Task
    This is a conversation between a male and a female teenager on Instagram. You will be given the texts of the female and need to generate the texts of the male. 
    # Input
    {0}
    # Output
    {1}
    /!/
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
    return [inp, output, prompt]

# Loop through each thing
l = 0
for k in content:
    # Compile prompt
    l += 1
    print(l)
    m = convert_to_prompt(k)
    
    # Hello?
    prompts.append({"her":m[0],"him":m[1],"prompt":m[2]})
    
json.dump(prompts, open("prompts.json", "w"))
    