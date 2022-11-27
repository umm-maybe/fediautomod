from mastodon import Mastodon, StreamListener
from bs4 import BeautifulSoup
from detoxify import Detoxify
import torch
import yaml
import os, sys
import langid

## Load config details from YAML
def load_yaml(filename):
    with open(filename, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as error:
            print(error)
    return None

# pass the yaml-format config file as command-line argument
config = load_yaml(sys.argv[1])

#   Set up Mastodon
mastodon = Mastodon(
    access_token = config['access_token'],
    api_base_url = config['masto_server']
)

# Set up Detoxify
cuda_available = torch.cuda.is_available()
detox = Detoxify('unbiased-small', device='cuda' if cuda_available else 'cpu')

def bad_keyword(text, negative_keywords):
    for keyword in negative_keywords:
        if text.find(keyword) > -1:
            return True
    return False

class Listener(StreamListener):
    def on_update(self, status):
        report = False
        toot_html = status['content']
        toot_soup = BeautifulSoup(toot_html)
        toot_text = toot_soup.get_text()
        print(toot_text)
        if config['keywords'] and bad_keyword(toot_text,config['keywords']):
            report = True
        else:
            lang_code = langid.classify(toot_text)[0]
            if lang_code=='en':
                # use Detoxify
                scores = detox.predict(toot_text)
            else:
                # no classification model available - pass
                scores = None
            if scores:
                for attribute in config['thresholds'].keys():
                    score = scores[attribute]
                    print(f"{attribute}: {score}")
                    if score > config['thresholds'][attribute]:
                        report = True
                        break # no need to continue checking
        if report==True:
             account_id = status['account']['id']
             status_ids = [status['id'],]
             mastodon.report(account_id,status_ids,comment="This report was made automatically.")
             mastodon.status_post(
                 status="This status update has been reported to admins for toxic language.",
                 in_reply_to_id=status['id'],
                 visibility="private"
             )

listener = Listener()
mastodon.stream_local(listener)
