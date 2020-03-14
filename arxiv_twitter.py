__author__="congcong wang"
__version__="v0"


import tweepy
import atoma
import time
from datetime import datetime
from twitter_private import *


#### THIS WILL BE args set up when "python arxiv_bot.py"
ARXIV_QUERY = "bert+OR+nlp" # the query for automatic retreival of latest papers from arxiv, the format refers to: https://arxiv.org/help/api
REQUEST_INTERVAL=3600  # REQUEST_INTERVAL means sending request to arxiv api every seconds of REQUEST_INTERVAL
#### THIS WILL BE args set up when "python arxiv_bot.py"

# verification
auth = tweepy.OAuthHandler(TWITTER_APP_KEY,TWITTER_APP_SECRET)
auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)
api = tweepy.API(auth)

import urllib.request
# for details of arxiv api, see: https://arxiv.org/help/api/user-manual#title_id_published_updated
url = 'http://export.arxiv.org/api/query?search_query=all:'+ARXIV_QUERY+'&start=0&max_results=1&sortBy=lastUpdatedDate&sortOrder=descending'
data = urllib.request.urlopen(url).read()

last_timestamp=-1.0

print("Start listening...")
while True:
	data_obj=atoma.parse_atom_bytes(data)
	next_timestamp=datetime.timestamp(data_obj.updated)

	# if next_timestamp > last_timestamp. that means update found and thus call Twitter API to update status
	if (next_timestamp-last_timestamp)>0.0:
		# post a tweet on Twitter
		post_content='#NLP #MachineLearning new arxiv NLP related paper: '+data_obj.entries[0].id_+'\n'+data_obj.entries[0].title.value+"."
		if len(post_content)>280:
		    # twitter allows a tweet up to 280 characters
		    post_content=post_content[:277]+"..."
		# post 
		response=api.update_status(post_content,tweet_mode="extended")
		if response.full_text != None:
			print("Successfully post the tweet:",response.full_text)
		else:
			print(response)
		last_timestamp=next_timestamp
	else:
		time.sleep(REQUEST_INTERVAL)
		print("No update in the last",REQUEST_INTERVAL,"seconds")
#to handle tweepy.error.TweepError: [{'code': 187, 'message': 'Status is a duplicate.'}]