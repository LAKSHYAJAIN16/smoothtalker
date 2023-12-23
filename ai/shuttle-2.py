import json
import threading
from shuttleai import *

shuttle = ShuttleClient(api_key="shuttle-v4q4afj7p330f64pb5t8")
data = json.load(open(r"C:\Users\USER\Projects\lj-llm\smoothtalker\client\prompts.json","r+"))

# VERY CAREFUL : CUTOFF
def run(start, cutoff, idd): 
    for i in range(start,cutoff):
        # smoothtalker/ai/buffer
        prompt = """
                    I'm creating an AI bot designed to help teenage guys talk to girls. I need you to generate some conversations.

        Here is the sample conversation-

        Her : incredibly sagacious person. 
        Him : yes yes yes. totally.

        An example of a valid answers for this convesation would be-

        CONVERSATION 1
        Her : im super wise wtf
        Him : of course, Socrates ;)
        ,

        CONVERSATION 2
        Her : im so smart
        Him : does that mean that our children will be intelligent baby  ;)

        I emphasis this again - the messages from 'her' and 'him' must have the same theme as the prompt. They must be funny, witty and charming. They must be sexy and attractive. The conversations must be in Gen Z slang. lmao, lol, cringe and cap would be appreciated. Make them as sarcastic as possible.

        I need 5 conversations like this, with unique messages for her and him.

        Here is your prompt. 
        Her : {0} 
        Him : {1}

        Your Conversations must be of the format :
        CONVERSATION
        Her : 'message'
        Him : 'message'.

        I want just the conversations. No filler messages or content which AI usually gives.

        Thanks bro.
        """.format(data[i]["her"],data[i]["him"])

        response = shuttle.chat_completion(
            model="gpt-4", 
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ], 
            stream=False,
            plain=False,
            image=None, 
            citations=False
        )
        
        try:
            message = response['choices'][0]['message']['content']
            print(message)

            # Output
            path = "prompt_" + str(i) + " " + idd + ".json"
            json.dump({"message":message, "prompt":prompt}, open(r"C:\Users\USER\Projects\lj-llm\smoothtalker\ai\buffer\ " + path, "w"))
        except:
            print(response)
                
# To Bypass rate limitations, because FRICK EM
for k in range(0, 10000):
    # Threading, because we hate ourselves
    t1 = threading.Thread(target=run, args=(0,100,"t1"))
    t2 = threading.Thread(target=run, args=(100,200,"t2"))
    t3 = threading.Thread(target=run, args=(200,300,"t3"))
    t4 = threading.Thread(target=run, args=(300,400,"t4"))
    t5 = threading.Thread(target=run, args=(400,500,"t5"))
    t6 = threading.Thread(target=run, args=(500,600,"t6"))
    t7 = threading.Thread(target=run, args=(600,700,"t7"))
    t8 = threading.Thread(target=run, args=(700,800,"t8"))
    t9 = threading.Thread(target=run, args=(800,900,"t9"))
    t10 = threading.Thread(target=run, args=(900,1000,"t10"))
    t11 = threading.Thread(target=run, args=(1000,1100,"t11"))
    t12 = threading.Thread(target=run, args=(1100,1200,"t12"))
    t13 = threading.Thread(target=run, args=(1200,1300,"t13"))
    t14 = threading.Thread(target=run, args=(1300,1400,"t14"))
    t15 = threading.Thread(target=run, args=(1400,1500,"t15"))
    t16 = threading.Thread(target=run, args=(1500,1600,"t16"))
    t17 = threading.Thread(target=run, args=(1600,1700,"t17"))
    t18 = threading.Thread(target=run, args=(1700,1800,"t18"))
    t19 = threading.Thread(target=run, args=(1800,1900,"t19"))
    t20 = threading.Thread(target=run, args=(1900,2000,"t20"))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    t9.start()
    t10.start()
    t11.start()
    t12.start()
    t13.start()
    t14.start()
    t15.start()
    t16.start()
    t17.start()
    t18.start()
    t19.start()
    t20.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    t8.join()
    t9.join()
    t10.join()
    t11.join()
    t12.join()
    t13.join()
    t14.join()
    t15.join()
    t16.join()
    t17.join()
    t18.join()
    t19.join()
    t20.join()
