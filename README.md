# Markov Bot
A bot that posts Markov chain comments to Reddit posts with titles/bodies matching user-specified keywords.  The corpus for generating the chains can either be a text file (the path of which can be provided by the user via the command line after running the script markov_bot.py) or a series of existing Reddit posts (the post IDs of which can be provided by the user.)  The subreddit to post in and post keywords are also specified by the user through the command line after running the script.

How to use
-------

First, create a Reddit app at [https://www.reddit.com/prefs/apps/](https://www.reddit.com/prefs/apps/). You must create the app with the same account that you want your bot to post under - e.g., if you want your bot to post as mega_bot_XL, create the app as mega_bot_XL. When creating the app, specify that the account will be a script ("Script for personal use. Will only have access to the developers accounts").

Once done, enter your Reddit app's client_id and client_secret in TEMPLATEpraw.ini:

> client_id=YOUR_CLIENT_ID_GOES_HERE

> client_secret=YOUR_CLIENT_SECRET_GOES_HERE

Then, enter your account info for the user account you want the bot to post as in TEMPLATEpraw.ini.  This must be the same account as the owner of the app:

> password=YOUR_PASSWORD_GOES_HERE

> username=YOUR_USERNAME_GOES_HERE

Pick a unique string for the user_agent.  It can be arbitrary or descriptive - e.g. Mega Bot XL v1:

> user_agent=YOUR_USERAGENT_GOES_HERE

Once done, **rename the file praw.ini** (it must be in the same directory as markov_bot.py).

Optionally, you may insert default values for corpus post IDs, search keywords, and subreddit in defaults.json.  defaults.json **must** be in the same directory as markov_bot.py.  Even if you do not specify your own defaults, defaults.json must be in the directory.

When you run markov_bot.py, there will be a series of command line prompts.  At the first prompt, enter "file" if you wish to use a text file as the bot's corpus - if so, you will then be prompted for a filepath.  Alternatively, enter "posts" if you wish to enter a series of reddit post IDs to construct the bot's corpus.

You can then follow the prompts to enter custom parameters, press enter repeatedly to use the defaults specified in defaults.json.

After completing the command prompt dialogue, the bot will begin monitoring the stream of posts to the subreddit you specified and will comment on posts matching the keywords either provided through the prompts or in defaults.json.

This project uses PRAW - check it out [here](https://praw.readthedocs.io/en/latest/).

Thoughts/comments? Reach me at mga25@njit.edu

