import datetime
import json
import praw
import random
import sys
import time

def main():
    # To contain the bot's default corpus post ids, post keywords, and subreddit.
    defaults = {}

    # Read and parse defaults.json to populate defaults dictionary
    try:
        with open("defaults.json", "r") as file:
            defaults = json.load(file)
    except Exception as e: 
        print "Exception: {}".format(e)
        print "Unable to load defaults.json. Check if it's in the same directory as markov_bot.py."
        print "Exiting..."
        sys.exit(1)

    # Check if the user wants to generate the bot's corpus from Reddit posts
    # or a text file
    print "Do you want to use a text file or existing Reddit posts as the bot's corpus?"
    file_as_corpus = False
    while True:
        file_or_posts = raw_input("[file/posts]: ")
        if file_or_posts == "file":
            file_as_corpus = True
            break
        elif file_or_posts == "posts":
            break
        print "Please enter 'file' or 'posts'"

    corpus_post_ids = []
    if file_as_corpus:
        # Get file path from command line
        print "Please enter the filepath of a text file relative to the current directory."
        while True:
            filepath = raw_input("Filepath: ")
            if filepath:
                break
            print "Please enter a filepath."
        try:
            with open(filepath, 'r') as file:
                text = file.read().replace('\n', ' ')
        except Exception as e:
            print "Exception attempting to open file: {}".format(e)
            print "Have you double-checked the filepath? Exiting..."
            sys.exit(1)
    else: 
        # Get post IDs from the command line. The text of these posts will be used
        # to make up the bot's corpus
        print "Enter the IDs for the Reddit posts that will make up the bot's corpus."
        print "(You may also enter nothing to use a default list of post IDs.)"
        while True:
            post_id = raw_input("Enter a post ID (or enter nothing to finish): ")
            if not post_id:
                break
            corpus_post_ids.append(post_id)
        if not corpus_post_ids:
            # corpus_post_ids = DEFAULT_CORPUS_POST_IDS
            corpus_post_ids = defaults["corpus_post_ids"]

    # Get post keywords from the command line
    target_post_keywords = []
    print "Enter keywords for Reddit posts that you wish the bot to search for and post in."
    print "(You may also enter nothing to use a default list of post IDs.)"
    while True:
        keyword = raw_input("Enter a keyword (or enter nothing to finish): ")
        if not keyword:
            break
        target_post_keywords.append(keyword)
    if not target_post_keywords:
        # target_post_keywords = DEFAULT_TARGET_POST_KEYWORDS
        target_post_keywords = defaults["target_post_keywords"]

    # Get subreddit from the command line
    print "Enter the subreddit that the bot should post in:"
    print "(You may also enter nothing to use the default subreddit.)"
    subreddit_name = raw_input("Enter a subreddit name *without* r/ (or enter nothing to finish): ")
    if not subreddit_name:
        # subreddit_name = DEFAULT_SUBREDDIT
        subreddit_name = defaults["subreddit"]

    print "Starting bot using these parameters:"
    if file_as_corpus:
        print "Corpus filepath: {}".format(str(filepath))
    else:
        print "Corpus post IDs: {}".format(str(corpus_post_ids))        
    print "Target post keywords: {}".format(str(target_post_keywords))
    print "Subreddit: {}".format(str(subreddit_name))

    # If generating corpus from posts, retrieve post text
    if not file_as_corpus:
        try:
            text = get_comment_texts_from_posts(corpus_post_ids)
        except Exception as e:
            print "Exception attempting to get post text: {}".format(e)
            print "Have you double-checked your post IDs? Exiting..."
            sys.exit(1)

    # Generate markov dictionar
    markov_dict = create_markov_dictionary(text)

    reddit = praw.Reddit('bot1')
    subreddit = reddit.subreddit(subreddit_name)

    # create list of existing relevant posts and do not (re)post on them
    post_ids_to_disregard = get_relevant_post_ids(subreddit, target_post_keywords, 1000)

    while True:
        try:
            for submission in subreddit.stream.submissions():
                #process submission 
                lowercase_title = submission.title.lower()
                for keyword in target_post_keywords:
                    if keyword in lowercase_title and submission.id not in post_ids_to_disregard:
                        message = generate_output(markov_dict, 6, 10)
                        try:
                            post_comment(submission, message)
                            print "-----------------------"
                            print "{}: Posted comment to post \"{}\":".format(
                                datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"), submission.title)
                            print message
                        # "You are doing that too much! Try again in X minutes"
                        except Exception as e:
                            print "{}: Exception trying to post comment: {}".format(
                                datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"), e)
                        print "Sleeping for 3 minutes before resuming ..."
                        time.sleep(180)
                        break
        # Log exceptions to console, but keep running
        except Exception as e:
            print "-----------------------"
            print "{}: Exception: {}".format(
                datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"), e)
            print "Sleeping for 3 minutes before resuming ..."
            time.sleep(180)

                    

def get_comment_texts_from_posts(post_IDs):
    reddit = praw.Reddit('bot1')
    text = ""
    for post_ID in post_IDs:
        submission = reddit.submission(id=post_ID)
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            #add punctuation if needed and concatenate
            text += comment.body 
            if text[-1] not in [".", "!", "?"]:
                text += ". "
            else:
                text += " "
    text = text.replace("[", " ")
    text = text.replace("]", " ")
    return text

def create_markov_dictionary(text):
    #split input string and add individual words to token_list[]
    token_list = []
    token_list = text.split()
    #create dictionary with values corresponding to words that follow keys in corpus
    markov_dict = {}
    current_index = 0
    next_token = ""
    for token in token_list:
        if token == "[deleted].":   #skips [deleted] tokens
            continue
        if current_index < len(token_list) - 1:
            next_token = token_list[current_index + 1]
            current_index += 1
            #print "Current token: ", token, " / Next token: ", next_token
            if token not in markov_dict:
                markov_dict[token] = []
            markov_dict[token].append(next_token)
    return markov_dict

def generate_output(markov_dict, lower_bound, upper_bound):
    """
    Generates markov-chain output for a random number of sentences
    between an upper and lower bound passed as parameters
    """
    output_text = ""
    i = random.randint(lower_bound, upper_bound)
    while i > 0:
        #Get random key from dictionary that begins with a capital letter
        beginning_of_sentence = False
        capital_case_key = ""
        while not beginning_of_sentence:
            random_key = random.sample(markov_dict, 1)[0] #random.sample() returns a list of one element, so get first element
            if random_key[0].isupper():
                beginning_of_sentence = True
            capital_case_key = random_key

        #print "Random key beginning with an upper-case letter: ", capital_case_key 

        end_of_sentence = False

        output_text += capital_case_key + " "
        current_token = random.sample(markov_dict[capital_case_key], 1)[0]
        while not end_of_sentence:
            output_text += current_token + " "
            if current_token[-1] in [".", "!", "?"]:
                end_of_sentence = True
                #one-third chance of linebreak
                if random.randint(0, 99) < 33:
                    output_text += "\n\n"
                    #pass
            else:
                old_token = current_token
                current_token = random.sample(markov_dict[old_token], 1)[0]
        i -= 1
    return output_text

def get_relevant_post_ids(subreddit, keywords, max_posts_to_search):
    relevant_post_IDs = []
    for post in subreddit.hot(limit=max_posts_to_search):
        title_words = post.title.lower().split()
        #print title_words
        for keyword in keywords:
            if keyword in title_words:
                #print post.title
                if post.id not in relevant_post_IDs:
                    relevant_post_IDs.append(post.id)
    return relevant_post_IDs

def post_comment(submission, message):
    submission.reply(message)

if __name__ == "__main__":
    main()


