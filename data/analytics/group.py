import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud

GROUP_NAME = "Hawaian Pizza Gang"
PATH = r"C:\Users\GAMING\Downloads\all_whatsapp_messages (6).json"

def getChats(path):
    dat = json.load(open(path, "r+", encoding="utf8"))["ls_output"]
    titles = []
    for i in dat:
        titles.append(i["title"])
    return titles

def getDat(path):
    dat = json.load(open(path, "r+", encoding="utf8"))["ls_output"]
    return dat

def mergeGroups(groups, dat):
    msgs = []
    for i in groups:
        gr = i
        for j in dat:
            if j["title"] == gr:
                ms = j["msgs"]
                for k in ms:
                    msgs.append(k["msg"].lower())
    return msgs

def getMessagesByPerson(group, path):
    dat = json.load(open(path, "r+", encoding="utf8"))["ls_output"]

    # Find group
    msgs = []
    for i in dat:
        if i["title"] == group:
            msgs = i["msgs"]
            break

    # Sort by user
    userWiseSort = {}
    for j in msgs:
        sender = j["sender"]
        msg_to_send = j["msg"] if j["msg"] != "" else "😄"
        try:
            userWiseSort[sender].append(msg_to_send)
        except:
            # Key does not exist
            userWiseSort[sender] = []
            userWiseSort[sender].append(msg_to_send)

    return userWiseSort

def getGroupMessages(group, path):
    dat = json.load(open(path, "r+", encoding="utf8"))["ls_output"]

    # Find group
    msgs = []
    for i in dat:
        if i["title"] == group:
            msgs = i["msgs"]
            break

    # Get Text
    act_msgs = []
    for j in msgs:
        act_msgs.append(j["msg"].lower())

    return act_msgs

def getMostUsedWords(msgs):
    word_dict = {}
    for i in msgs:
        words = i.split(" ")
        for j in words:
            word = j.lower()
            try:
                word_dict[word] += 1
            except:
                word_dict[word] = 1

    return word_dict

def sortMostUsedWordsByFreq(mostUsedWords):
    size = len(mostUsedWords)
    dat = mostUsedWords
    ret = []
    for i in range(size):
        maxScore = -1
        maxScoreKey = ""
        for j in dat:
            value = dat[j]
            if value > maxScore:
                maxScore = value
                maxScoreKey = j

        # Delete max and add it to our ret array (list :L)
        ret.append({"word": maxScoreKey, "value": maxScore})
        del dat[maxScoreKey]

    return ret

def convert_to_wordcloud(words):
    return "".join(words)

def display_word_cloud(text):
    # change font_size, max_word and background_color
    wordcloud = WordCloud(max_font_size=200,
                          background_color="white").generate(text)
    # Display the image
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.figure()
    plt.axis("off")
    plt.show()

print(getChats(PATH))