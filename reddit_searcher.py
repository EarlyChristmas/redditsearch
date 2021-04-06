from __future__ import unicode_literals
import requests
import json
import datetime
import re
import pickle
import traceback
import os
import io



def retrievePosts(searchword, cont):
    subCount1 = 0
    global stopwords

    adderalldict = dict()
    # submission list
    try:
        data = getSubmission(cont, searchword)
    except:
        temp = str(traceback.format_exc())
        pickle.dump(temp, open('posts' + searchword + str(data[-1]['created_utc']) + '.pickle', 'wb'))
    #first = 0
    # Will run until all posts have been gathered
    while len(data) > 0:
        file1 = io.open(searchword + "_Posts.txt", "a", encoding="utf-8")
        for submission in data:
            try:
                #url.append(submission["full_link"])
                jsonurl = submission["full_link"]
                # if "created_utc" in submission:
                # print(submission["created_utc"])
                if "selftext" in submission:
                    wordtokens = 0
                    wordtokens = wordtokens + tokenize(submission["selftext"], searchword)
                    try:
                        wordtokens = wordtokens + tokenize(submission["title"], searchword)
                    except:
                        print("cannot get title")

                    #yr = convertToYear(submission["created_utc"])
                    postid = submission["id"]

                    writing = ""
                    writing = writing + str(postid)
                    writing = writing + ", " + str(wordtokens)
                    writing = writing + ", " + str(submission["created_utc"])
                    writing = writing + ", " + str(jsonurl) + "\n"
                    #print(writing)

                    file1.write(writing)


                subCount1 += 1
                #first = first + 1
            except:
                pass
                # print("fail")
                # print(submission["full_link"])
        file1.close()
        print(searchword + "(posts): #" + str(subCount1) + "   date: " + str(data[-1]['created_utc']))
        # Calls getSubmission() with the created date of the last submission
        try:
            data = getSubmission(keyword=searchword, after=data[-1]['created_utc'])
        except:
            temp = str(traceback.format_exc())
            pickle.dump(temp, open('posts' + searchword + str(data[-1]['created_utc']) + '.pickle', 'wb'))
            break

    print("Submission count for " + searchword + " is " + str(subCount1))




def retrieveComments(searchword, cont):
    comCount1 = 0
    global stopwords
    lastfail = cont

    try:
        entries = getComments(cont, searchword)
    except:
        temp = str(traceback.format_exc())
        pickle.dump(temp, open('comment' + searchword + str(entries[-1]['created_utc']) + '.pickle', 'wb'))
        print("Comment count for " + searchword + " is " + str(comCount1))
        return
    first = 0
    while len(entries) > 0:
        file1 = io.open(searchword + "_Comments.txt", "a", encoding="utf-8")
        for comment in entries:
            try:
                # print(comment["parent_id"])
                #print(comment)
                #print(comment["created_utc"])
                #print(comment)
                jsonurl = ""
                if "permalink" in comment:
                    jsonurl = "https://www.reddit.com" + comment["permalink"]

                if "body" in comment:
                    tempcom = comment["body"]

                    wordtokens = tokenize(comment["body"], searchword)


                    postid = comment["link_id"]
                    comid = comment["id"]
                    if len(postid) > 3:
                        postid = postid[3:]

                    writing = ""
                    writing = writing + str(postid)
                    writing = writing + ", " + str(comid)
                    writing = writing + ", " + str(wordtokens)
                    writing = writing + ", " + str(comment["created_utc"])
                    if jsonurl == "":
                        writing = writing + ", " + "n" + "\n"
                    else:
                        writing = writing + ", " + jsonurl + "\n"

                    #print(writing)
                    file1.write(writing)

                    f = io.open(searchword + "/" + str(postid) + str(comid) + ".txt", "w", encoding="utf-8")
                    f.write(tempcom)
                    f.close()




                # url.append("https://www.reddit.com" + submission["permalink"])
                comCount1 += 1
            except:
                temp = str(traceback.format_exc())
                #print("hi" + comment["permalink"])
                #print("fail")
                print(temp)
                pass
        file1.close()
        print(searchword + "(comments): #" + str(comCount1) + "   date: " + str(entries[-1]['created_utc']))
        try:
            entries = getComments(keyword=searchword, after=entries[-1]['created_utc'])
        except:
            temp = str(traceback.format_exc())
            pickle.dump(temp, open('comment' + searchword + str(entries[-1]['created_utc']) + '.pickle', 'wb'))
            break
    print("Comment count for " + searchword + " is " + str(comCount1))



def getSubmission(after, keyword):
    url = 'https://api.pushshift.io/reddit/search/submission?&size=2000&after='+str(after)+'&q='+str(keyword)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']

def getComments(after, keyword):
    url = 'https://api.pushshift.io/reddit/search/comment?&size=1000&after='+str(after)+ '&q=' + str(keyword)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']

def tokenize(text, key):
    l = []
    if text == "[removed]":
        return 0
    ret = 0
    for i in re.findall(r'[a-zA-Z0-9]{2,}', text):
        i = i.lower()
        if i == key:
            ret = ret + 1
    return ret

def convertToYear(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y')

# stopwords
stopwords = {"a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as",
             "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't",
             "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down",
             "during", "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't",
             "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself",
             "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
             "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off",
             "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same",
             "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that",
             "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they",
             "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up",
             "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what", "what's",
             "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with",
             "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself",
             "yourselves"}

# list of the subreddit urls
#url = []

# KEYWORDS TO SEARCH
keywordlistfull = ['counterspell']



# Unix timestamp of date to crawl from
after = "1262304001"
print(convertToYear(after))


# submission count
subCount = 0

# comment count
comCount = 0

# index
x = 0


# start running code on all words in keywordlistfull
for item in keywordlistfull:
    retrievePosts(item, after)
    #retrieveComments(item, after)

























# random

# print(len(totalwords))
# wordfrequencies = computeWordFrequencies(totalwords)
# sortedlist = sorted(wordfrequencies.items())
# sorteddict = {k: v for k, v in sorted(wordfrequencies.items(), key=lambda item: item[1], reverse=True)}
# print(sorteddict)


# adds .json to each url 
# while x < len(url):
#     url[x] = url[x] + ".json"
#     x += 1

# obj = {}
# obj['url'] = url
#
# # Save to json of urls for later use
# with open("submissions.json", "w") as jsonFile:
#     json.dump(obj, jsonFile)
