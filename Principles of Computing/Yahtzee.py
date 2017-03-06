"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, only score against upper level
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)


def add(x,y):
    return x + y

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def gen_sorted_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                new_sequence.sort()
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set

def gen_all_combs(outcomes, length):
    """
    Iterative function that combinates the set of all sequences of
    outcomes of given length.
    """   
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            temp_outcomes = list(outcomes)
            for element in partial_sequence:
                temp_outcomes.pop(temp_outcomes.index(element))
            for item in temp_outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                new_sequence.sort()
                temp_set.add(tuple(new_sequence))
            answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    hand_to_set = set(hand)
    counts = [hand.count(value) for value in hand_to_set]
    products = [(value*count) for value, count in zip(hand_to_set, counts)]
    return max(products)


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    outcomes = range(1, num_die_sides+1)
    free_seqs = gen_all_sequences(outcomes, num_free_dice)
    rolls = [(held_dice + seq) for seq in free_seqs]
    scores = [score(roll) for roll in rolls]
    scores_to_set = set(scores)
    probs = [scores.count(value)/float(len(scores)) for value in scores_to_set]
    products = [(value*prob) for value, prob in zip(scores_to_set, probs)]
    return sum(products)
    

def gen_all_holdsPJ(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: full yahtzee hand

    Returns a set of tuples, where each tuple is dice to hold
    """
    all_holds = set()
    for sub_length in range(len(hand)):
        hold = gen_all_combs(hand, sub_length)
        all_holds.update(hold)
    return all_holds

#powerset solution
def gen_all_holds(hand):
    answer_set = set([()])
    for hand_item in hand:
        temp_set = set([])
        
        #print "hand_item: " + str(hand_item)
        #print "answer_set: " + str(answer_set)
        
        for answer_set_item in answer_set:
            #print "answer_set_item: " + str(answer_set_item)
            temp_set.add(answer_set_item + (hand_item,))
            #print "temp_kimenet: " + str(temp_set)
        answer_set.update(temp_set)
        #print "kimenet: " + str(answer_set)
        #print "END"
        
    return answer_set


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    ans = [0,()]
    holds = gen_all_holds(hand)
    for hold in holds:
        expected = expected_value(hold, num_die_sides, len(hand)-len(hold))
        if expected > ans[0]:
            ans[0] = expected
            ans[1] = hold
    return tuple(ans)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 2, 3, 4)
    #hand_score, hold = strategy(hand, num_die_sides)
    #print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score
    #print gen_all_holds(hand)
    #print score([3,3,3,5,5])
    #print expected_value((6,6), 6, 3)
    print strategy([1,3,3,3,5], 6)
    
run_example()


#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)
                                       
    
    
    



