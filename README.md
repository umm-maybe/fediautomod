# fediautomod
Content moderation support bot for the Fediverse (Mastodon etc.)

# Motivation
Due to changes and issues with other social networks, in 2022 there has been a surge of interest in [Mastodon](https://joinmastodon.org), with thousands of new users joining the service. Unfortunately, many of them were misled into joining already-large servers, where content moderation had already proven to be a major challenge. 

This bot is designed to provide content moderation assistance to Mastodon instance administrators, making the "needle in a haystack" challenge of catching and addressing hate speech and toxicity easier in the fediverse. In so doing, it also reduces a potential hurdle that could stop people from starting smaller servers which would expand the Fediverse, spreading out the capacity to handle growth, and creating safer, more easily moderated spaces for new users.

# Initial approach
The bot is a simple Python script that watches a server's local feed for status updates and uses pre-trained machine learning models to determine whether a status update contains toxic language. It has been shown that such models have the unfortunate potential to flag text by members of disadvantaged and marginalized groups at a higher rate, so we use a library called [Detoxify](https://github.com/unitaryai/detoxify) that is specifically fine-tuned to remove bias in text toxicity classification when possible.  

When Detoxify returns a score that exceeds a threshold set by the bot operator (in a config file), the status and its user are reported to the instance moderator.  Note that this action does not require administrator settings. The bot should not be used to automatically remove statuses based upon algorithmic detection; being flagged and removed in error can lead users to feel silenced. A human should always make the decision whether to take action regarding a report, and better yet be prepared to take other actions besides simply removing the content, such as offering support to whomever it hurt.

# Prerequisites
You will need a server or other always-on computer to run this on, with Python and PyTorch installed (or at least installable).

# Installation
1. Clone the repository with `git clone http://github.com/umm-maybe/fediautomod`
2. Create an account for the bot.  Tip: you can append "+botname" to the part of your e-mail address before the @ symbol when making a new account (e.g. info+mybot@umm-maybe.com) so that you don't have to also sign up for a new e-mail address every time.  Also, you can skip this and use your existing account, if you don't mind reports and automated posts coming from it (e.g. with an instance admin account).
3. Logged in as the bot user, from the drop-down next to your profile name, select *Preferences*, and then select *Development*.  Click on *New Application* and fill out the form (make sure you have *Write:Reports* checked).
4. Copy the access token from the page presented to you when you're done.
5. Open the `config-example.yaml` file and paste your access token in the appropriate place. Save the file under a new name e.g. `config.yaml` after setting masto_server to point to the URL of the Mastodon instance whose feed you wish to monitor.
6. Create and enter a new Python environment with `python3 -m venv env && source env/bin/activate`
7. Run `pip install -r requirements.txt`
8. Run the bot with `python3 automod.py config.yaml`

# Limitations
Currently the bot only works in English.  It also does nothing with images. See [issues](https://github.com/umm-maybe/fediautomod/issues) for discussion.