# author: Henry West
# date: 2/17/2015
# purpose: get all tweets from within Wisconsin and analyse how "Wisconsin" they are
# ie if they involve beer, cheese, or the packers
# proposed points: 15/15: Program is functional, reads in Wisconsin-geotagged tweets and checks
# for matches.

"""

My Underwhelming Results:

The conclusion I have come to is that Wisconsin drops the ball (at least on Monday nights in February)
when it comes to talking about stereotypical "Wisconsin" things. I had several test runs, and out of almost
1000 tweets, I only got one referencing cheese, beer, the majestic Aaron Rodgers, or our glorious Green Bay Packers.
I'm sure that if run during football season, I would get much happier results, but for now, I have the following
message for my beloved home state: "Get it together - we have a culture to protect!"

Fun side note: I got more Taylor Swift lyrics than I did actual matches.

"""

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from auth import TwitterAuth
import re

class StdOutListener(StreamListener):
	def on_data(self, data):
		j = json.loads(data)
		text = j["text"]
		print(text)
		# search for anything involving beer, cheese, or the Packers
		regexp = re.compile(r'(cheese|beer|(Aaron\sRodgers)|Pack(ers)*)')
		#increment number of tweets
		dataAnalysis[0] += 1
		if regexp.search(text) is not None:
			#if match is found, increment number of wisconsin-stereotype tweets
			dataAnalysis[1] += 1
		#set percentage
		dataAnalysis[2] = ("%.2f" % (100.0 * float(dataAnalysis[1]) / float(dataAnalysis[0]))) + "%"
		
		print "Current results: ", dataAnalysis
		#write to output file
		outputFile.write(text.encode('ascii', 'ignore') + "\n")

if __name__ =='__main__':
	try:
		#open output file
		outputFile = open("output.txt", "w")
		dataAnalysis = [0, 0, "0.0"] #total tweets, tweets with filter, percent
		l = StdOutListener()
		#set authorizations
		auth = OAuthHandler(TwitterAuth.consumer_key, TwitterAuth.consumer_secret)
		auth.set_access_token(TwitterAuth.access_token, TwitterAuth.access_token_secret)
		#open stream
		stream = Stream(auth, l)
		stream.filter(locations=[-92.173971653,42.5996061276,-87.5059967041,46.5271148883])

	except KeyboardInterrupt:
		pass
	#only you can prevent memory leaks
	outputFile.close()
	print "Final ratio: ", dataAnalysis
