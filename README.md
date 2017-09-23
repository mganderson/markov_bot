# Markov Bot
A bot that posts Markov chain comments to Reddit posts with titles/bodies matching user-specified keywords.  The corpus for generating the chains can either be a text file (the path of which can be provided by the user via the command line after running the script markov_bot.py) or a series of existing Reddit posts (the post IDs of which can be provided by the user.)  The subreddit to post in and post keywords are also specified by the user through the command line after running the script.

In order to use, you must enter your Reddit bot account info in TEMPLATEpraw.ini 

> client_id=YOUR_CLIENT_ID_GOES_HERE
> password=YOUR_PASSWORD_GOES_HERE
> username=YOUR_USERNAME_GOES_HERE
> user_agent=YOUR_USERAGENT_GOES_HERE

Once done, rename the file praw.ini (it must be in the same directory as markov_bot.py).

Uses PRAW - check it out [here](https://praw.readthedocs.io/en/latest/).

