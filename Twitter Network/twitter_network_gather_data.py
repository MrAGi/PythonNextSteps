import os
import twitter
import pickle
import time
import json

class TwitterData:
    def __init__(self):
        #these come from creating a twitter application via dev.twitter.com
        self.consumer_key = "see documentation"
        self.consumer_secret = "see documentation"

        #file path to twitter credentials
        self.oauth_filename = 'twitter_oauth'

        #check to see if doesn't exist
        if not os.path.exists(self.oauth_filename):
            #create the file by getting authorisation from twitter
            twitter.oauth_dance("see documentation", self.consumer_key, self.consumer_secret, self.oauth_filename)

        #get the authorisation tokens from the file
        self.oauth_token, self.oauth_token_secret = twitter.read_token_file(self.oauth_filename)

    def login(self):
        #log in to use the twitter_api
        self.auth = twitter.OAuth(self.oauth_token, self.oauth_token_secret, self.consumer_key, self.consumer_secret)
        self.twitter_api = twitter.Twitter(domain="api.twitter.com",
                              api_version='1.1',
                              auth=self.auth)

    def get_followers(self,user_id=None):
        followers = self.twitter_api.followers.ids(user_id=user_id)
        return followers['ids']

    def get_user_data(self,user_ids):
        user_data = self.twitter_api.users.lookup(user_id=user_ids)
        return list(user_data)
        

    # def get_friendship_status(self,followers):
    #     if len(followers) <= 100:
    #         try:
    #             follower_list = str(followers).strip('[]')
    #             print(follower_list)
    #             friendship_data = self.twitter_api.friendships.lookup(user_id=followers)
    #         except twitter.api.TwitterHTTPError as e:
    #             print("urgh...stupid twitter rate limit")
    #     else:
    #         friendship_data = []
    #         while len(followers) > 0:
    #             follower_list = str(followers[:99]).strip('[]')
    #             print(follower_list)
    #             friendship_data.extend(self.twitter_api.friendships.lookup(user_id=followers))
    #             followers = followers[99:]
    #     print(str(friendship_data).encode('utf-8'))
    #     return friendship_data

    # def save_friendship_data(self,file_name,friendship_data):
    #     with open(file_name,mode="wb") as my_file:
    #         pickle.dump({'data':friendship_data},my_file)
    #         print("follower data saved to file '{0}'".format(file_name))


def get_all_followers(tw,followers):
    follower_data = {}
    api_calls = 0
    for follower in followers:
        try:
            f = tw.get_followers(user_id=follower)
            follower_data[str(follower)] = f
        except twitter.api.TwitterHTTPError:
            print("User {0} does not authorise you to view their followers".format(follower))
        api_calls += 1
        if api_calls == 15:
            print("maximum api calls reached - sleeping for 15 minutes")
            timer = 15
            while timer > 0:
                print("{0} minutes remaining".format(timer))
                time.sleep(60)
                timer -= 1
    return follower_data

def get_all_user_data(tw,followers):
    user_data = {}
    for key, value in followers.items():
        print("the key is {0}".format(key))
        if len(value) > 0:
            print(value)
            f = tw.get_user_data(str(value[:100]).strip("[]")) #limit to 99 connections
        else:
            f = None
        user_data[str(key)] = f
    return user_data

def main():
    twitter_data = TwitterData()
    twitter_data.login()

    #get all of your followers
    followers = twitter_data.get_followers()
    #print(followers)

    #get your followers screennames
    followers_screen_names = twitter_data.get_user_data(str(followers[:30]).strip("[]")) #convert list to a string and strip [ ] characters from ends

    #get followers of your followers
    follower_data = get_all_followers(twitter_data,followers[:30])
    print(follower_data)

    #get their screennames
    follower_user_data = get_all_user_data(twitter_data, follower_data)

    file_data = {'followers': followers[:30], 'followers_screen_names': followers_screen_names,
                'follower_data': follower_data, 'follower_user_data':follower_user_data}

    #save data to a file
    with open("twitter_network.dat",mode="wb") as my_file:
        pickle.dump(file_data,my_file)
        print("data saved")

if __name__ == '__main__':
    main()



