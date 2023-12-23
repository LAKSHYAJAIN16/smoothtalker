import json
import time
from openai import OpenAI

client = OpenAI(
    # This is the default and can be omitted
    api_key="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",
)

data = json.load(open(r"C:\Users\USER\Projects\lj-llm\smoothtalker\client\prompts.json","r+"))

# VERY CAREFUL : CUTOFF
cutoff = 200
start = 100
total_cost = 0

for i in range(start,cutoff):
    # smoothtalker/ai/buffer
    prompt = """
                I'm creating an AI bot designed to help teenage guys talk to girls. I need you to generate some conversations.

    Here is the sample conversation-

    Her : incredibly sagacious person. 
    Him : yes yes yes. totally.

    An example of a valid answers for this convesation would be-

    CONVERSATION
    Her : im super wise wtf
    Him : of course, Socrates ;)
    ,
    CONVERSATION
    Her : im so smart
    Him : does that mean that our children will be intelligent baby  ;)

    I emphasis this again - the messages from 'her' and 'him' must have the same theme as the prompt. They must be funny, witty and charming. They must be sexy and attractive. The conversations must be in Gen Z slang. lmao, lol, cringe and cap would be appreciated. Make them as sarcastic as possible.

    I need 5 conversations like this, with unique messages for her and him.

    Here is your prompt. 
    Her : {0} 
    Him : {1}
    
    The 5 Conversations must have unique messages for her and him. The prompt for 'her' must be different everytime.
                """.format(data[i]["her"],data[i]["him"])
                
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )

    message = chat_completion.choices[0].message.content

    # Keep track of cost. We don't want to go over 2 dollars
    cost = ((chat_completion.usage.completion_tokens * 0.0020) / 1000) + chat_completion.usage.prompt_tokens * 0.0010 / 1000
    print("COST : ",cost)
    total_cost += cost
    print(message)
    
    # Output
    path = "prompt_" + str(time.time().hex()) + ".json"
    json.dump({"message":message, "prompt":prompt},open(r"C:\Users\USER\Projects\lj-llm\smoothtalker\ai\buffer\ " + path, "w"))
    
print(total_cost)