# A simple fun program to play around with twitterpython

# Libraries and Dependencies
import twitter
import csv
import numpy as np
import textblob
from textblob import TextBlob


# Initialize the twitter api object
api = twitter.Api(consumer_key={CONSUMER_KEY},
                  consumer_secret={CONSUMER_SECRET},
                  access_token_key={ACCESS_TOKENKEY},
                  access_token_secret={ACCESS_TOKENSECRET})

user = "khairulnazran"
filename = user + "_tweet_sentiments.csv"
n = 200

#Get tweets in user's timeline
statuses = api.GetUserTimeline(screen_name=user, count=n, include_rts = False)

#Open the CSV file and write the label
out = csv.writer(open(filename,"w"), delimiter=',',quoting=csv.QUOTE_ALL)
out.writerow(['Tweets by ' + user , 'Polarity Score', 'Subjectivity Score'])

n_positive = 0
n_negative = 0
n_neutral = 0

#A list of polarities of tweets, needed to get mean scores
polarities = []
subjectivities = []
#For each tweet, get sentiment analysis
for status in statuses:
	analysis = TextBlob(status.text)
	#If the tweet is in Malay, translate it so we can have an accurate sentiment rating
	if analysis.detect_language() == 'ms':
		try:
			analysis = analysis.translate(from_lang="ms", to='en')
			print "translated!"
		except textblob.exceptions.NotTranslated:
			print "translation failed"

	polarity = analysis.sentiment.polarity
	subjectivity = analysis.sentiment.subjectivity

	#Categorize the tweets based on sentiments
	if polarity == 0:
		n_neutral = n_neutral + 1
	elif polarity < 0:
		n_negative = n_negative + 1
	else:
		n_positive = n_positive + 1

	#Push polarity and subjectivity score into their respective list
	# if polarity != 0:
	polarities.append(analysis.sentiment.polarity)
	subjectivities.append(analysis.sentiment.subjectivity)

	out.writerow([status.text.encode('utf-8'), round(polarity, 3), round(subjectivity, 3)])

out.writerow([])

#Print summary statistics
mean_polarity = np.mean(polarities)
mean_subjectivity = np.mean(subjectivities)

out.writerow(['n', n , ''])
out.writerow(['Positive Sentiments', n_positive , ''])
out.writerow(['Negative Sentiments', n_negative , ''])
out.writerow(['Neutral Sentiments', n_neutral , ''])
out.writerow(['Mean Polarity', str(round(mean_polarity, 3)), ''])
out.writerow(['Mean Subjectivity', str(round(mean_subjectivity, 3)), ''])
