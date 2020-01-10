import urllib
import json
import configparser
import datetime
import autoScript
import time
from Comment import Comment
import cloudinary
import cloudinary.uploader
import cloudinary.api
import utils
import sys

if len(sys.argv) == 1:
    print("Usage: $python ipp.py <config_file>")
    exit()

configurationFile = sys.argv[1]
fileName = sys.argv[2]

config = configparser.ConfigParser()
config.sections()
config.read(configurationFile)

ACCESS_TOKEN = config['DEFAULT']['accessToken']
INSTAGRAM_BUSINESS_USER_ID = config['DEFAULT']['instagramBusinessUserId']
FACEBOOK_APP_ID= config['DEFAULT']['facebookAppId']
FACEBOOK_APP_SECRET= config['DEFAULT']['facebookAppSecret']
CLOUDINARY_CLOUD_NAME = config['CLOUDINARY']['cloud_name']
CLOUDINARY_API_KEY = config['CLOUDINARY']['api_key']
CLOUDINARY_API_SECRET = config['CLOUDINARY']['api_secret']
MAX_TIME_BETWEEN_UPDATES = 8
MIN_TIME_BETWEEN_UPDATES = 5
TIME_BETWEEN_CHECKS = 3600
TIME_BETWEEN_SAVE = 10


#controller
A = config['CONTROLLER']['A']
B = config['CONTROLLER']['B']
UP = config['CONTROLLER']['UP']
DOWN = config['CONTROLLER']['DOWN']
LEFT = config['CONTROLLER']['LEFT']
RIGHT = config['CONTROLLER']['RIGHT']
START = config['CONTROLLER']['START']
SELECT = config['CONTROLLER']['SELECT']

utils.initController(A,B,UP,DOWN,LEFT,RIGHT,START,SELECT)
utils.initEventFile(fileName+".js")

def findCommentPosition (jsonArr, commentId):
    for i in range(len(jsonArr)):
        if jsonArr[i]["id"] == commentId:
           return i
    return -1

#Setting up Cloudinary config
cloudinary.config( 
  cloud_name = CLOUDINARY_CLOUD_NAME, 
  api_key = CLOUDINARY_API_KEY, 
  api_secret = CLOUDINARY_API_SECRET 
)

#Getting a refresh token if not yet refreshed today
lastRefresh = datetime.datetime.strptime(config['DEFAULT']['lastTokenRefresh'],"%Y-%m-%d")  if config['DEFAULT']['lastTokenRefresh'] != "" else datetime.datetime.strptime("1970-01-01", '%Y-%m-%d')

if (datetime.datetime.now() - lastRefresh).days > 0 :
    print("Refreshing token...") 
    getRefreshToken_response = utils.execWithOutput(['curl',
                  "https://graph.facebook.com/v5.0/oauth/access_token?grant_type=fb_exchange_token&client_id="+FACEBOOK_APP_ID+"&client_secret="+FACEBOOK_APP_SECRET+"&fb_exchange_token="+ACCESS_TOKEN]) 
    ACCESS_TOKEN = json.loads(getRefreshToken_response)["access_token"]
    #Update last token and refresh date in config file
    config['DEFAULT']['lastTokenRefresh'] = datetime.datetime.now().strftime("%Y-%m-%d")
    config['DEFAULT']['accessToken'] = ACCESS_TOKEN
    with open(configurationFile, 'w') as configfile:
        config.write(configfile)

lastCheck = 0
lastSave = 0
while True:
    #If never checked in the last hour...
    #FIXME this could mean that comments on a new post could be ignored for up to TIME_BETWEEN_CHECKS seconds!!!
    if time.time() - lastCheck > TIME_BETWEEN_CHECKS :
        print("Taking a screenshot")
       #utils.stampWindowPath("./screenshots/", str(round(time.time()))+".jpg")
        numOfImpressions = utils.getNumOfImpressions(INSTAGRAM_BUSINESS_USER_ID, ACCESS_TOKEN) #this makes one API call
        print("Today's impressions so far: " + str(numOfImpressions))
        print("Fetcing last post foar IG business user. Wait 18 seconds...")
        lastCheck = time.time()
        #Fetching last post for INSTAGRAM_BUSINESS_USER_ID
        media_response =  utils.execWithOutput(['curl', "https://graph.facebook.com/v5.0/" + INSTAGRAM_BUSINESS_USER_ID + "/media?access_token=" + ACCESS_TOKEN])
        #Fetching last post from IG                                
        lastPost = json.loads(media_response)["data"][0]["id"]
        time.sleep(MAX_TIME_BETWEEN_UPDATES)
    
    #save every 10 minutes
    if time.time() - lastSave > TIME_BETWEEN_SAVE :
        print("Saving game...")
        lastSave = time.time()
        utils.save()

    #Fetching all comments from last post
    comments_response = utils.execWithOutput(['curl', "https://graph.facebook.com/v5.0/" + lastPost + "/comments?fields=like_count,hidden,id,media,text,timestamp,username,replies,user&access_token=" + ACCESS_TOKEN])
    commentsJArr = json.loads(comments_response)["data"]
    #Getting the position in the array "comments" of the last used comment 
    lastUsedCommentPosition = findCommentPosition(commentsJArr, config['DEFAULT']['lastUsedCommentId']) if config['DEFAULT']['lastUsedCommentId'] != "" else -1

    if lastUsedCommentPosition != -1:
        #Fetching the next comment from the array FIXME out of range if 0
        nextCommentIndex = lastUsedCommentPosition - 1 if lastUsedCommentPosition > 0 else lastUsedCommentPosition
        nextComment = commentsJArr[nextCommentIndex]
        nextCommentText = nextComment["text"]

        #Creating list of our Comment Objects
        commentsList = utils.fillCommentsList(nextCommentIndex, commentsJArr)

        #Updating the last used comment in the configs
        config['DEFAULT']['lastUsedCommentId'] = commentsJArr[0]["id"]
        with open(configurationFile, 'w') as configfile:
            config.write(configfile)
        autoScript.controller(commentsList)
    impressionsFactor = max(1, numOfImpressions)
    sleepTime = max(MIN_TIME_BETWEEN_UPDATES, MAX_TIME_BETWEEN_UPDATES // impressionsFactor)
    print("Now sleeping for " + str(sleepTime) + " sec")
    time.sleep(sleepTime)


##start testing post media
#cloudinary.uploader.upload("my_picture.jpg", public_id = 'abcdefg')
#url = cloudinary.utils.cloudinary_url("abcdefg.jpg")
##not available due to instagram limitations: only partners can post via API
#post_curl_cmd = ['curl', '-X',
#    'POST',
#                "https://graph.facebook.com/v5.0/" + INSTAGRAM_BUSINESS_USER_ID + "/media?image_url=" + url[0] + "?access_token=" + ACCESS_TOKEN + "&caption=#poketest"]
#print("siamo qui 2")                
#post_response = subprocess.Popen(post_curl_cmd,
#                                stdout = subprocess.PIPE,
#                                stderr = subprocess.PIPE).communicate()[0]
#print(post_response)
#exit()
##end testing post media