import urllib3.request
import requests
import io
import time

keywords = ["adderall", "adhd", "concerta", "drug", "drugs", "lsd", "provigil", "ritalin", "stimulant", "stimulants", "vyvanse"]
#keywords = ["provigil"]

for keyword in keywords:
    file = io.open(str(keyword) + "_Posts.txt")
    fal = io.open(str(keyword) + "_fails.txt", "w", encoding="utf-8")
    counter = 0
    while True:
        counter = counter + 1
        line = file.readline().rstrip()
        if not line:
            break
        if line == "":
            pass
        else:
            try:
                print("doing number: " + str(counter) + " for " + str(keyword))
                addtext = ""
                spl = line.split(",")
                id = spl[0]
                url = spl[-1]
                site = requests.get(url + ".json", headers = {'User-agent': 'your bot 0.1'})
                addtext = addtext + site.json()[0]["data"]["children"][0]["data"]["title"] + "\n"
                temp = site.json()[0]["data"]["children"][0]["data"]["selftext"]
                if temp == "[removed]" or temp == "[deleted]":
                    pass
                else:
                    addtext = addtext + site.json()[0]["data"]["children"][0]["data"]["selftext"]
                time.sleep(0.01)

                f = io.open(str(keyword) + "/" + str(id) + ".txt", "w", encoding="utf-8")
                f.write(addtext)
                f.close()

            except Exception:
                temp = ""
                temp = temp + str(counter) + "\n"
                fal.write(unicode(temp, "utf-8"))
                print("failed")
    fal.close()



        # f = io.open(str(keyword) + "/" + str(postid) + str(comid) + ".txt", "w", encoding="utf-8")
        # f.write(tempcom)
        # f.close()
