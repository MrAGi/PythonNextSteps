import os
import twitter
import pickle
import time

#these come from creating a twitter application via dev.twitter.com
CONSUMER_KEY = "see documentation"
CONSUMER_SECRET = "see documentation"

#file path to twitter credentials
oauth_filename = 'twitter_oauth'

#check to see if doesn't exist
if not os.path.exists(oauth_filename):
    #create the file by getting authorisation from twitter
    twitter.oauth_dance("see documentation", CONSUMER_KEY, CONSUMER_SECRET, oauth_filename)
#get the authorisation tokens from the file
oauth_token, oauth_token_secret = twitter.read_token_file(oauth_filename)

#log in to use the twitter_api
auth = twitter.OAuth(oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(domain="api.twitter.com",
                      api_version='1.1',
                      auth=auth)

#get the followers of the logged in user
followers = twitter_api.followers.ids()
followers = followers['ids']
follower_data = {}
#get the data for each follower
api_calls = 0
for follower_id in followers:
    try:
        data = twitter_api.friendships.lookup(user_id="{0}".format(follower_id))
        api_calls += 1
        #create a new key in the dictionary and add relevant data as value
        follower_data[str(follower_id)] = data[0]
        #twitter allows 15 calls to this api per 15 minute period
        #so sleep for 15 minutes if maximum reached
        if api_calls == 15:
            print("maximum api calls reached - sleeping for 15 minutes")
            timer = 15
            while timer > 0:
                print("{0} minutes remaining".format(timer))
                time.sleep(60)
                timer -= 1
    except twitter.api.TwitterHTTPError:
        print("urgh...stupid twitter")
    
with open("twitter_follower_directed.dat",mode="wb") as my_file:
    pickle.dump({'data':follower_data},my_file)
    print("follower data saved to file 'follower.dat'")




