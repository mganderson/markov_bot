# This file is not used and should be deleted / code included/refined in markov_bot.py

import praw

cs288_post_IDs = ["5moshs", "5k08py", "3r8xe8", "3hzzu5", "5omhuq", "5q72iu", "5ouemn", "4d4xh5", "5mrdhq", "5oww9h", "5iq7i5", "46zd27", "4a05xw"]
reddit = praw.Reddit('bot1')
text = ""

for post_ID in cs288_post_IDs:
    submission = reddit.submission(id=cs288_post_IDs[1])
    submission.comments.replace_more(limit=0)
    for comment in submission.comments.list():
        text = text + comment.body

print text

