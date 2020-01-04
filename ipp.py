import urllib
import subprocess
import json
import configparser
import datetime
import autoScript
import time
from Comment import Comment
import cloudinary
import cloudinary.uploader
import cloudinary.api

config = configparser.ConfigParser()
config.sections()
config.read('config.txt')

ACCESS_TOKEN = config['DEFAULT']['accessToken']
INSTAGRAM_BUSINESS_USER_ID = config['DEFAULT']['instagramBusinessUserId']
FACEBOOK_APP_ID= config['DEFAULT']['facebookAppId']
FACEBOOK_APP_SECRET= config['DEFAULT']['facebookAppSecret']
CLOUDINARY_CLOUD_NAME = config['CLOUDINARY']['cloud_name']
CLOUDINARY_API_KEY = config['CLOUDINARY']['api_key']
CLOUDINARY_API_SECRET = config['CLOUDINARY']['api_secret']

newPost = False #FIXME
lastPost = config['DEFAULT']['lastPost']

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
print("last refr: " + str(lastRefresh))
if (datetime.datetime.now() - lastRefresh).days > 0 :
    print("Refreshing token...")
    getRefreshToken_curl_cmd = ['curl',
                  "https://graph.facebook.com/v5.0/oauth/access_token?grant_type=fb_exchange_token&client_id="+FACEBOOK_APP_ID+"&client_secret="+FACEBOOK_APP_SECRET+"&fb_exchange_token="+ACCESS_TOKEN]
    getRefreshToken_response = subprocess.Popen(getRefreshToken_curl_cmd,
                                  stdout = subprocess.PIPE,
                                  stderr = subprocess.PIPE).communicate()[0].decode("utf-8") 
    ACCESS_TOKEN = json.loads(getRefreshToken_response)["access_token"]
    #Update last token and refresh date in config file
    config['DEFAULT']['lastTokenRefresh'] = datetime.datetime.now().strftime("%Y-%m-%d")
    config['DEFAULT']['accessToken'] = ACCESS_TOKEN
    with open('config.txt', 'w') as configfile:
        config.write(configfile)

while True:
    #Executing a request fetching all media for INSTAGRAM_BUSINESS_USER_ID
    #TODO we can avoid this call to execute every time by storing a "new post" boolean somewhere (webhooks?)
    if lastPost == "" or newPost :
        media_curl_cmd = ['curl',
                        "https://graph.facebook.com/v5.0/" + INSTAGRAM_BUSINESS_USER_ID + "/media?access_token=" + ACCESS_TOKEN]
        media_response = subprocess.Popen(media_curl_cmd,
                                        stdout = subprocess.PIPE,
                                        stderr = subprocess.PIPE).communicate()[0]
        #Fetching last post from IG                                
        lastPost = json.loads(media_response)["data"][0]["id"]

    #Fetching all comments from last post
    comments_curl_cmd = ['curl', 
                    "https://graph.facebook.com/v5.0/" + lastPost + "/comments?fields=like_count,hidden,id,media,text,timestamp,username,replies,user&access_token=" + ACCESS_TOKEN]
    comments_response = subprocess.Popen(comments_curl_cmd,
                                    stdout = subprocess.PIPE,
                                    stderr = subprocess.PIPE).communicate()[0]
    commentsJArr = json.loads(comments_response)["data"]
    #Getting the position in the array "comments" of the last used comment 
    lastUsedCommentPosition = findCommentPosition(commentsJArr, config['DEFAULT']['lastUsedCommentId']) if config['DEFAULT']['lastUsedCommentId'] != "" else -1

    #Fetching the next comment from the array
    nextCommentIndex = lastUsedCommentPosition - 1 if lastUsedCommentPosition > 0 else lastUsedCommentPosition
    nextComment = commentsJArr[nextCommentIndex]
    nextCommentText = nextComment["text"]

    #Creating list of our Comment Objects
    commentsList = []
    for i in range (nextCommentIndex, -1, -1):
        c = Comment(commentsJArr[i]["id"], commentsJArr[i]["text"])
        c.username = commentsJArr[i]["username"]
        c.likeCount = commentsJArr[i]["like_count"]
        c.repliesCount = len(commentsJArr[i]["replies"]["data"]) if "replies" in commentsJArr[i] else 0
        c.timestamp = commentsJArr[i]["timestamp"]
        commentsList.append(c)

    #Updating the last used comment in the configs
    config['DEFAULT']['lastUsedCommentId'] = commentsJArr[0]["id"]
    with open('config.txt', 'w') as configfile:
            config.write(configfile)

    autoScript.controller(commentsList)
    time.sleep(20)


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