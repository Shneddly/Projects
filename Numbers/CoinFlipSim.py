import random
'''
Takes in a number and flips a coin that number of times
then outputs a tally of the flips
'''
def coin_flip(n):
    # initialization
    count = 0
    choice_list = ['heads','tails','edge']
    # sets distribution according to a study by Murray and Teare on an American nickel
    distribution = [float((1-(1/6000))/2),float((1-(1/6000))/2),float(1/6000)]
    tally_dict = {'heads':0,'tails':0,'edge':0}
    while count < n:
        # chooses a random item from the choice list according to weights in the distribution
        random_choice = random.choices(choice_list,distribution)
        tally_dict[random_choice[0]] += 1
        count += 1
    return tally_dict
