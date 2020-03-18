__author__="Congcong Wang"
__version__="v0"


import tweepy
from tweepy import TweepError
import atoma
import time
from datetime import datetime
from twitter_private import *
import argparse
import logging
import sys


logging.raiseExceptions = False
logger = logging.getLogger("this-logger")
logger.setLevel(logging.INFO)
logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)


def main():
	parser = argparse.ArgumentParser()
	# Required parameters

	parser.add_argument(
	    "-r","--request_interval",
	    default=3600,
	    type=int,
	    help="The request_interval (Default: 3600) means sending request to arxiv api every seconds of request_interval.",
	)

	parser.add_argument(
	    "-q","--arxiv_query",
	    default="nlp+OR+bert",
	    type=str,
	    help="The arxiv_query (default: 'nlp+OR+bert') is specified for automatic retreival of latest papers from arxiv. Space should be replaced with '+'. More refers to: https://arxiv.org/help/api.",
	)

	parser.add_argument(
	    "-d","--days_since",
	    default=10,
	    type=int,
	    help="The days_since (default: 10) defines the number of past days since considered to be an update, e.g., 10 means that ony the papers on ariXv with the update date no more than 10 days ago are considered to be forwarded and posted to Twitter.",
	)

	parser.add_argument(
	    "-t","--hashtags_prepend",
	    default="#NLP,#MachineLearning",
	    type=str,
	    help="The list of hashtags (default: '#NLP,#MachineLearning') you want to prepend the tweet, seperated by ','.",
	)

	args = parser.parse_args()


	ARXIV_QUERY = args.arxiv_query
	REQUEST_INTERVAL=args.request_interval

	HASHTAGS2PREPEND=args.hashtags_prepend.split(",")


	# verification
	auth = tweepy.OAuthHandler(TWITTER_APP_KEY,TWITTER_APP_SECRET)
	auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)
	api = tweepy.API(auth)

	import urllib.request
	# for details of arxiv api, see: https://arxiv.org/help/api/user-manual#title_id_published_updated
	last_timestamp=datetime.timestamp(datetime.now())-args.days_since*3600*24

	logger.info("Start listening with arguments: "+str(args))
	while True:
		url = 'http://export.arxiv.org/api/query?search_query=all:'+ARXIV_QUERY+'&start=0&max_results=1&sortBy=lastUpdatedDate&sortOrder=descending'
		data = urllib.request.urlopen(url).read()
		data_obj=atoma.parse_atom_bytes(data)
		next_timestamp=datetime.timestamp(data_obj.updated)
		logger.info("Get a paper from arXiv updated at " + str(data_obj.updated)+": "+data_obj.entries[0].id_)
		# if next_timestamp > last_timestamp. that means update found and thus call Twitter API to update status
		if (next_timestamp-last_timestamp)>0.0:
			# post a tweet on Twitter
			post_content=" ".join(HASHTAGS2PREPEND)+' new arxiv '+ ARXIV_QUERY +' related paper: '+data_obj.entries[0].id_+'\n'+data_obj.entries[0].title.value+"."
			if len(post_content)>280:
			    # twitter allows a tweet up to 280 characters
			    post_content=post_content[:277]+"..."
			# post 
			try:
				response=api.update_status(post_content,tweet_mode="extended")
			except TweepError as err:
				# if there is an error, wait REQUEST_INTERVAL seconds before next call and thus last_timestamp set to be next_timestamp+1
				last_timestamp=next_timestamp+1
				logger.error(err)
				logger.error("Go to sleep "+str(REQUEST_INTERVAL)+" seconds")
				continue
			if response.full_text != None:
				logger.info("Successfully post the tweet:\n===================\n"+ response.full_text+"\n===================")
			else:
				logger.error(response)
			last_timestamp=next_timestamp
		else:
			logger.info("Start sleeping given days_since =",str(args.days_since),"days")
			time.sleep(REQUEST_INTERVAL)
			# logger.info("No update in the last "+str(REQUEST_INTERVAL)+" seconds")

if __name__ == "__main__":
    main()







