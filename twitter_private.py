# twitter api data (replace yours here given are placeholder)
# if you have not yet, go for applying at: https://developer.twitter.com/
TWITTER_KEY=""
TWITTER_SECRET=""
TWITTER_APP_KEY=""
TWITTER_APP_SECRET=""


with open("twitter_keys.txt") as f:
	for line in f:
		tups=line.strip().split("=")
		if tups[0] == "TWITTER_KEY":
			TWITTER_KEY=tups[1]
		elif tups[0] == "TWITTER_SECRET":
			TWITTER_SECRET=tups[1]
		elif tups[0] == "TWITTER_APP_KEY":
			TWITTER_APP_KEY=tups[1]
		elif tups[0] == "TWITTER_APP_SECRET":
			TWITTER_APP_SECRET=tups[1]