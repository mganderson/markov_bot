# This file is not used and should be deleted / code included/refined in markov_bot.py

#!/usr/bin/python

import random
import sys

#print "Number of arguments: ", len(sys.argv), ' arguments'
#print "Arguments: ", str(sys.argv)

if len(sys.argv) != 2:
    print "Error.  Must provide one command line argument (text file)"
    sys.exit()


token_list = []

#open file at file path provided as command line argument
input_file = open(sys.argv[1], 'r')

#parse input file and add words to token_list[]
for line in input_file:
    token_list.extend(line.split())

#print token_list

#create dictionary with values corresponding to words that follow keys in corpus
markov_dict = {}
current_index = 0
next_token = ""

for token in token_list:
    if current_index < len(token_list) - 1:
        next_token = token_list[current_index + 1]
        current_index += 1
        #print "Current token: ", token, " / Next token: ", next_token

        if token not in markov_dict:
            markov_dict[token] = []
        markov_dict[token].append(next_token)

#print markov_dict


#Get random key from dictionary that begins with a capital letter
beginning_of_sentence = False
capital_case_key = ""
while not beginning_of_sentence:
    random_key = random.sample(markov_dict, 1)[0] #random.sample() returns a list of one element, so get first element
    if random_key[0].isupper():
        beginning_of_sentence = True
        capital_case_key = random_key

print "Random key beginning with an upper-case letter: ", capital_case_key 

end_of_sentence = False

print capital_case_key,
current_token = random.sample(markov_dict[capital_case_key], 1)[0]
while not end_of_sentence:
    print current_token,
    if current_token[-1] in [".", "!", "?"]:
        end_of_sentence = True
    else:
        old_token = current_token
        current_token = random.sample(markov_dict[old_token], 1)[0]



