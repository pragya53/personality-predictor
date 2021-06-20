import tweepy as tw
import key

def fetch(handle):
	# Authenticate
	auth = tw.OAuthHandler(key.consumer_key, key.consumer_secret)
	# Set Tokens
	auth.set_access_token(key.access_token, key.access_token_secret)
	# Instantiate API
	api = tw.API(auth, wait_on_rate_limit=True)

	res = api.user_timeline(screen_name=handle, count=100, include_rts=True)
	tweets = [tweet.text for tweet in res]
	text = ''.join(str(tweet) for tweet in tweets)
	return text

