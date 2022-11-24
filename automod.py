from mastodon import Mastodon, StreamListener
from bs4 import BeautifulSoup
from detoxify import Detoxify
import torch

cuda_available = torch.cuda.is_available()
detox = Detoxify('multilingual', device='cuda' if cuda_available else 'cpu')

#   Set up Mastodon
mastodon = Mastodon(
    access_token = 'PASTE_ACCESS_TOKEN_HERE',
    api_base_url = 'https://mastodon.social/'
)


class Listener(StreamListener):
    def on_update(self, status):
        toot_html = status['content']
        toot_soup = BeautifulSoup(toot_html)
        toot_text = toot_soup.get_text()
        detox_out = detox.predict(toot_text)
        hateScore = detox_out['severe_toxicity']
        nsfwScore = detox_out['sexual_explicit']
        print(toot_text)
        print(f'severe_toxicity: {hateScore}')
        print(f'sexual_explicit: {nsfwScore}')
        # if detox_out['severe_toxicity']>0.05 or detox_out['sexual_explicit']>0.8:
        #     account_id = status['account']['id']
        #     status_ids = [status['id'],]
        #     mastodon.report(account_id,status_ids)

listener = Listener()
mastodon.stream_local(listener)
