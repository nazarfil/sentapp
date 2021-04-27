import requests
import json

class RedditClient(object):
    url_about = "https://www.reddit.com/r/{}/about.json"

    def get_profile(self, subreddit) -> int:
        response = requests.get(url=self.url_about.format(subreddit), headers = {'User-agent': 'your bot 0.1'})
        try:
            content = json.loads(response.content)
            subs = content["data"]
            return subs["subscribers"]
        except:
            return 0
