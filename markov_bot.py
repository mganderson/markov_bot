import praw
import random
import sys

cs288_post_IDs = ["5moshs", "5k08py", "3r8xe8", "3hzzu5", "5omhuq", "5q72iu", "5ouemn", "4d4xh5", "5mrdhq", "5oww9h", "5iq7i5", "46zd27", "4a05xw"]

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
    #parse input string and add individual words to token_list[]
    token_list = []
    token_list = text.split()
    #print token_list

    #create dictionary with values corresponding to words that follow keys in corpus
    markov_dict = {}
    current_index = 0
    next_token = ""
    for token in token_list:
        if token == "[deleted].":	#skips [deleted] tokens
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
    #generate 3-6 sentences
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

        print capital_case_key,
        current_token = random.sample(markov_dict[capital_case_key], 1)[0]
        while not end_of_sentence:
            print current_token,
            if current_token[-1] in [".", "!", "?"]:
                end_of_sentence = True
                #one-third chance of linebreak
                if random.randint(0, 99) < 33:
                    print "\n\n"
                    #pass
            else:
                old_token = current_token
                current_token = random.sample(markov_dict[old_token], 1)[0]
        i -= 1

text = get_comment_texts_from_posts(cs288_post_IDs)
markov_dict = create_markov_dictionary(text)
generate_output(markov_dict, 6, 10)


