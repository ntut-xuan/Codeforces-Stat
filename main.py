#!/usr/bin/env python3
import sys
import math
import requests
import json
from io import BytesIO
from PIL import Image, ImageDraw
from flask import *

app = Flask(__name__)

def getColor(rank, val):
    if rank == "newbie":
        return ("rgba(128, 128, 128, %f)" % (val), "rgba(128, 128, 128, %f)" % (val))
    elif rank == "pupil":
        return ("rgba(0, 128, 0, %f)" % (val), "rgba(0, 128, 0, %f)" % (val))
    elif rank == "specialist":
        return ("rgba(3, 168, 158, %f)" % (val), "rgba(3, 168, 158, %f)" % (val))
    elif rank == "expert":
        return ("rgba(0, 0, 255, %f)" % (val), "rgba(0, 0, 255, %f)" % (val))
    elif rank == "candidate master":
        return ("rgba(170, 0, 170, %f)" % (val), "rgba(170, 0, 170, %f)" % (val))
    elif rank == "candidate master":
        return ("rgba(170, 0, 170, %f)" % (val), "rgba(170, 0, 170, %f)" % (val))
    elif rank == "international master" or rank == "master":
        return ("rgba(255, 140, 0, %f)" % (val), "rgb(255, 140, 0, %f)" % (val))
    elif rank == "international grandmaster" or rank == "grandmaster":
        return ("rgba(255, 0, 0, %f)" % (val), "rgba(255, 0, 0, %f)" % (val))
    elif rank == "legendary grandmaster":
        return ("rgba(0, 0, 0, %f)" % (val), "rgba(255, 0, 0, %f)" % (val))

def country_city_process(jsonData):

    if "country" in jsonData["result"][0].keys() and "city" in jsonData["result"][0].keys():
        return jsonData["result"][0]["country"] + ", " + jsonData["result"][0]["city"]
    elif "country" in jsonData["result"][0].keys():
        return jsonData["result"][0]["country"]
    elif "city" in jsonData["result"][0].keys():
        return jsonData["result"][0]["city"]
    else:
        return "No country and city info"

def name_process(jsonData):

    if "firstName" in jsonData["result"][0].keys() and "lastName" in jsonData["result"][0].keys():
        return jsonData["result"][0]["firstName"] + ", " + jsonData["result"][0]["lastName"]
    else:
        return "No name info"

def organization(jsonData):

    if "organization" in jsonData["result"][0].keys() and len(jsonData["result"][0]["organization"]) != 0:
        return jsonData["result"][0]["organization"]
    else:
        return "No organization info"

def fixedPhoto(url):
    response = requests.get(url)

    target = Image.open("photo.jpg")
    
    with Image.open(BytesIO(response.content)).convert("RGBA") as im:
        width = max(300, 300)
        out = Image.new("RGB", (width, width), (255, 255, 255))
        print(width)
        out.paste(im, (int((width-im.size[0])/2), int((width-im.size[1])/2)))
        out.save("photo.jpg")

@app.route("/static/<path:path>")
def returnStaticFile(path):
    return send_from_directory('static', path)

@app.route("/")
def getIndex():
    
    handle = request.args.get('handle')

    r = requests.get("https://codeforces.com/api/user.rating?handle=" + handle)
    text = r.text
    jsonData = json.loads(text)

    contestCount = len(jsonData["result"])

    r = requests.get("https://codeforces.com/api/user.info?handles=" + handle)
    text = r.text
    jsonData = json.loads(text)

    

    s = """<svg width="900" height="450" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <style>
    	@font-face {
	  font-family: "Open 24 Display St";
	  src: url('./static/Open 24 Display St.ttf');
	}
	@font-face {
	  font-family: "IBM Plex Mono Medium";
	  src: url('./static/IBMPlexMono-Medium.ttf');
	}
	@font-face {
	  font-family: "IBM Plex Mono Heavy";
	  src: url('./static/IBMPlexMono-Bold.ttf');
	}
        svg {
            background-color: rgb(250, 250, 250);
        }
        g.rank {
            font-size: 20pt;
            font-weight: bold;
            font-family: "IBM Plex Mono Heavy";
        }
        g.title {
            font-family: "IBM Plex Mono Heavy";
            font-size: 30pt;
        }
        g.rateAndMaxRate {
            font-family: "IBM Plex Mono Medium";
            font-size: 16pt;
        }
        g.rankAndMaxRank {
            font-family: "IBM Plex Mono Medium";
            font-size: 16pt;
        }
        g.rateNumber {
            font-family: "Open 24 Display St";
            font-size: 48pt;
        }
        g.rankString {
            font-family: "IBM Plex Mono Medium", monospace;
            font-size: 16pt;
        }
    </style>
    <polygon points="0,0 0,150, 50,0" style="fill:rgba(255, 255, 0, 0.2);"></polygon>
    <polygon points="50,0 25,75 150,0" style="fill:rgba(0, 0, 255, 0.2);"></polygon>
    <polygon points="87.5,37.5 250,0 150,0" style="fill:rgba(255, 0, 0, 0.2);"></polygon>
    <polygon points="900,350 850,350 900,300" style="fill:{Polygon_FirstRankColor};"></polygon>
    <polygon points="900,350 850,350 750,450 900,450" style="fill:{Polygon_1_RankColor};"></polygon>
    <g class="rank" data-testid="card-rank" transform="translate(25, 45)">
        <text x="0" y="0" fill="{FirstRankColor}"> {FirstRank} </text>
        <text x="16" y="0" fill="{1_RankColor}"> {1_Rank} </text>
    </g>
    <g class="title" data-testid="card-title" transform="translate(25, 95)">
        <text x="0" y="0" fill="{FirstHandleColor}"> {FirstHandle} </text>
        <text x="24" y="0" fill="{1_HandleColor}"> {1_Handle} </text>
    </g>
    <g class="photo" id="photo" data-testid="card-photo" transform="translate(25, 115)">
        <image href="{Photo}"></image>
    </g>
    <g class="rateAndMaxRate" data-testid="card-title" transform="translate(350, 155)">
        <text x="0" y="0"> {Name}  </text>
    </g>
    <g class="rateAndMaxRate" data-testid="card-title" transform="translate(350, 195)">
        <text x="0" y="0"> {Country_And_City}  </text>
    </g>
    <g class="rateAndMaxRate" data-testid="card-title" transform="translate(350, 235)">
        <text x="0" y="0"> {Organization}  </text>
    </g>
    <g class="rateNumber" data-testid="card-title" transform="translate(350, 325)">
        {Rate}
    </g>
    <g class="rateAndMaxRate" data-testid="card-title" transform="translate(350, 385)">
        <text x="0" y="0"> Participate {ContestCount} contests.  </text>
    </g>
    <g class="rateAndMaxRate" data-testid="card-title" transform="translate(350, 425)">
        {MaxRankInfo}
    </g>
</svg>
"""


    rated = """
    <text x="0" y="0" fill="{RatingColor}"> {Rating} </text>
    <text x="120" y="0"> / </text>
    <text x="150" y="0" fill="{MaxRatingColor}"> {MaxRating} </text>
    """

    unrated = """
    <text x="0" y="0"> UNRATED </text>
    """

    if "rank" in jsonData["result"][0].keys():

        s = s.replace("{Rate}", rated)

        s = s.replace("{Polygon_FirstRankColor}", getColor(jsonData["result"][0]["rank"], 0.4)[0])
        s = s.replace("{Polygon_1_RankColor}", getColor(jsonData["result"][0]["rank"], 0.4)[1])

        s = s.replace("{FirstRankColor}", getColor(jsonData["result"][0]["rank"], 1)[0])
        s = s.replace("{1_RankColor}", getColor(jsonData["result"][0]["rank"], 1)[1])

        s = s.replace("{FirstHandleColor}", getColor(jsonData["result"][0]["rank"], 1)[0])
        s = s.replace("{1_HandleColor}", getColor(jsonData["result"][0]["rank"], 1)[1])

        s = s.replace("{RatingColor}", getColor(jsonData["result"][0]["rank"], 1)[1])
        s = s.replace("{MaxRatingColor}", getColor(jsonData["result"][0]["maxRank"], 1)[1])

        s = s.replace("{MaxRankInfo}", """<text x="0" y="0"> The max of rank is {MaxRank}.  </text>""")
        s = s.replace("{FirstRank}", jsonData["result"][0]["rank"][0].upper())
        s = s.replace("{1_Rank}", jsonData["result"][0]["rank"][1:])
        s = s.replace("{MaxRating}", str(jsonData["result"][0]["maxRating"]))
        s = s.replace("{Rating}", str(jsonData["result"][0]["rating"]))
    else:
        s = s.replace("{MaxRankInfo}", "")
        s = s.replace("{FirstRank}", "U")
        s = s.replace("{1_Rank}", "nrated")
        s = s.replace("{Rate}", unrated)
    
    if "maxRank" in jsonData["result"][0].keys():
        s = s.replace("{MaxRank}", str(jsonData["result"][0]["maxRank"]))
    
    s = s.replace("{FirstHandle}", jsonData["result"][0]["handle"][0])
    s = s.replace("{Handle}", jsonData["result"][0]["handle"])
    s = s.replace("{FirstHandle}", jsonData["result"][0]["handle"][0])
    s = s.replace("{1_Handle}", jsonData["result"][0]["handle"][1:])
    s = s.replace("{Photo}", jsonData["result"][0]["titlePhoto"])

    s = s.replace("{Name}", name_process(jsonData))
    s = s.replace("{Country_And_City}", country_city_process(jsonData))
    s = s.replace("{ContestCount}", str(contestCount))
    s = s.replace("{Organization}", organization(jsonData))
    
    
    response = Response(s, mimetype="image/svg+xml")
    return response


@app.route("/getPhoto")
def getPhoto():
    handle = request.args.get('handle')
    r = requests.get("https://codeforces.com/api/user.info?handles=" + handle)
    text = r.text
    jsonData = json.loads(text)
    photo = fixedPhoto(jsonData["result"][0]["titlePhoto"])
    return send_file("photo.jpg", mimetype='image/jpg') 

if __name__ == "__main__":
    
    app.debug = True
    app.run(host="0.0.0.0", port=80)
