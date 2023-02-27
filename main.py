import requests
import gooeypie as gp
import shutil
import os
import sys

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

default = resource_path("pfp.png")
icon = resource_path("S.png")

def fetchData(event):
    username.text = "Fetching Data"
    try:
        if not os.listdir().__contains__("images"):
            os.mkdir('images')
        
        print("Fetching Data")
        rawResponse = requests.get("https://api.beatleader.xyz/player/"+str(blID.text))
        responseJson = dict(rawResponse.json())
        username.text = "Username: " + responseJson['name']
        stats = dict(responseJson['scoreStats'])
        rankPlayCount.text = "Ranked Play Count: " + str(stats['rankedPlayCount'])
        bestPP.text = "Top PP Play: " + str(round(float(stats["topPp"]), 2))
        currentPP.text = "PP: " + str(round(float(responseJson['pp']), 2))
        currentRank.text = "Rank: "+str(responseJson['rank'])
        image_url = str(responseJson['avatar'])
        
        url = image_url
        file_name = f"./images/{blID.text}.png"

        res = requests.get(url, stream = True)
        
        if res.status_code == 200:
            with open(file_name,'wb') as f:
                shutil.copyfileobj(res.raw, f)
            print('Image sucessfully Downloaded to: ',file_name)
            
            ProfilePic.image = file_name
        else:
            print('Image Couldn\'t be retrieved')
    except:
        print(f"Failed to retreive data")
        username.text = "Failed to retrieve data"
        rankPlayCount.text = ""
        bestPP.text = ""
        currentPP.text = ""
        currentRank.text = ""
        ProfilePic.image = default

app = gp.GooeyPieApp("Speecil BeatLeader Stats App")
app.set_grid(10, 10)
nameInput = gp.Input(app)

app.width = 480
app.height = 640
idInput = gp.Button(app, "Fetch", fetchData)
blID = gp.Input(app)
rankPlayCount = gp.Label(app, "")
bestPP = gp.Label(app, "")
currentPP = gp.Label(app, "")
currentRank = gp.Label(app, "")
ProfilePic = gp.Image(app, default)
username = gp.Label(app, "")
inputLbl = gp.Label(app, "BeatLeader ID:")
app.add(inputLbl, 1, 1)
app.add(blID, 1, 2)
app.add(idInput, 1, 3)
app.add(username, 3, 1)
app.add(currentRank, 4, 1)  
app.add(currentPP, 5, 1)
app.add(rankPlayCount, 6, 1)
app.add(bestPP, 7, 1)
app.add(ProfilePic, 10,1)
app.set_icon(icon)
app.run()