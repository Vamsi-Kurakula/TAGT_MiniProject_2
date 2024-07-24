'''
Topics in Algorithmic Game Theory:

All Code that relates to Mini Project 2
'''

import random
import pandas as pd
import matplotlib.pyplot as plt

class Indivdual():
    '''
    Class to contain information on a individual.

    Generates a preference list for a indivdual
    '''

    def __init__(self, name, n):
        '''
        n: Number of the 'other' party to create rankings for 
        '''

        self.name = name
        self.my_rankings = list(range(n))
        random.shuffle(self.my_rankings)
        self.current_choice_idx = 0
        self.current_match = -1

    def get_current_choice(self):
        return self.my_rankings[self.current_choice_idx]

    def pick_best(self, candidates):
        for i in self.my_rankings:
            if i in candidates:
                return i 
            
    def get_rank(self, candidate):
        for idx, label in enumerate(self.my_rankings):
            if label == candidate:
                return idx + 1
                
            

def generate_doctors_hospitals(n):
    '''
    Setting up doctors and hospitals 
    '''
    doctor_list = []
    hospital_list = []

    for i in range(n):
        doctor_list.append(Indivdual(i, n))
        hospital_list.append(Indivdual(i, n))

    return doctor_list, hospital_list

def gale_shapley(doctors, hospitals):
    '''
    Executes the gale_shapley matching algorithm

    Returns a pairs dictionary where the key is who is proposed to
    and the value is the proposer for proposed.

    By default the doctors are proposing to the hospitals 
    '''
    num_pairs = len(doctors)

    num_proposals = 0 

    while True:

        # Check each doctor 
        for idx, i_doctor in enumerate(doctors):
            
            # Skip if doctor currently has a match
            if i_doctor.current_match != -1:
                continue

            # Check Doctor's current choice
            curr_hos_choice = hospitals[i_doctor.get_current_choice()]
            if idx == curr_hos_choice.pick_best([curr_hos_choice.current_match, idx]):
                # knock out current hospital match
                doctors[curr_hos_choice.current_match].current_match = -1
                #doctors[curr_hos_choice.current_match].current_choice_idx += 1
                # Set hospital and doctor matches to eachother
                curr_hos_choice.current_match = idx
                i_doctor.current_match = i_doctor.get_current_choice()
            else:
                i_doctor.current_match = -1 
                i_doctor.current_choice_idx += 1

            num_proposals += 1
            
        pairs_count = 0
        # Count pairs to see if we break out of the loop
        for i_doctor in doctors:
            if i_doctor.current_match != -1:
                pairs_count += 1

        # If all people are matched, we can break out of this loop
        if pairs_count == num_pairs:
            break

    # Create pair dictionary
    pairs = {}
    for i_pair in range(num_pairs):
        pairs[i_pair] = doctors[i_pair].current_match

    # Assign rankings to all parties
    doctor_rank_sum = 0
    for i_doc in doctors:
        doctor_rank_sum += i_doc.get_rank(i_doc.current_match)

    hospital_rank_sum = 0
    for i_hos in hospitals:
        hospital_rank_sum += i_hos.get_rank(i_hos.current_match)

    return pairs, num_proposals, doctor_rank_sum/num_pairs, hospital_rank_sum/num_pairs

def avg_num_proposals_by_n():
    '''
    Driver program for mini-project 2
    '''
    # Base variables for this expiriment
    MAX_NUM_PAIRS = 100
    NUM_TRIALS_PER_N = 5

    summary_stats_df = pd.DataFrame(columns=['n', 'trial_num', 'num_proposals', 'avg_doctor_rank', 'avg_hospital_rank'])

    for i_pairs in range(2, MAX_NUM_PAIRS + 1):
        for j in range(NUM_TRIALS_PER_N):
            doctor_list, hospital_list = generate_doctors_hospitals(i_pairs)
            pairs, num_proposals, avg_doctor_rank, avg_hospital_rank = gale_shapley(doctor_list, hospital_list)

            # Record information
            new_row = pd.DataFrame([{'n':i_pairs, 
                                     'trial_num': j, 
                                     'num_proposals':num_proposals, 
                                     'avg_doctor_rank': avg_doctor_rank, 
                                     'avg_hospital_rank': avg_hospital_rank}])
            summary_stats_df = pd.concat([new_row, summary_stats_df], ignore_index=True)


    # Create plot for summary stats
    agg_df = summary_stats_df.groupby('n').agg({'num_proposals':'mean', 'avg_doctor_rank':'mean', 'avg_hospital_rank':'mean'}).reset_index()
    
    # Num Proposal Plot
    agg_df.plot(x='n', y='num_proposals')
    # Add title and labels
    plt.title('Average Number of Proposals by N')
    plt.xlabel('Number of Pairs (N)')
    plt.ylabel(f'Average Number of Proposals ({NUM_TRIALS_PER_N} for each N)')
    # Show the plot
    plt.savefig('Images/avg_proposals.png')
    plt.close()

    # Ranking Plot
    plt.plot(agg_df['n'], agg_df['avg_doctor_rank'], label = 'Average Doctor Pair Rank')
    plt.plot(agg_df['n'], agg_df['avg_hospital_rank'], label = 'Average Hospital Pair Rank')
    # Add title and labels
    plt.title('Average Rankings by N')
    plt.xlabel('Number of Pairs (N)')
    plt.ylabel(f'Average Number of Rankings ({NUM_TRIALS_PER_N} for each N)')
    plt.legend()
    # Show the plot
    plt.savefig('Images/avg_rankings.png')
    plt.close()

def distribution_proposals_for_n():
    '''
    Driver program for mini-project 2
    '''
    # Base variables for this expiriment
    NUM_PAIRS = 100
    NUM_TRIALS_PER_N = 100

    summary_stats_df = pd.DataFrame(columns=['n', 'trial_num', 'num_proposals', 'avg_doctor_rank', 'avg_hospital_rank'])

    for j in range(NUM_TRIALS_PER_N):
        doctor_list, hospital_list = generate_doctors_hospitals(NUM_PAIRS)
        pairs, num_proposals, avg_doctor_rank, avg_hospital_rank = gale_shapley(doctor_list, hospital_list)

        # Record information
        new_row = pd.DataFrame([{'n':NUM_PAIRS, 
                                 'trial_num': j, 
                                 'num_proposals':num_proposals, 
                                 'avg_doctor_rank': avg_doctor_rank, 
                                 'avg_hospital_rank': avg_hospital_rank}])
        summary_stats_df = pd.concat([new_row, summary_stats_df], ignore_index=True)


    # Create plot for summary stats
    summary_stats_df.plot.hist(column=["num_proposals"], by="n", bins = 10)

    # Add title and labels
    plt.title(f'Distribution of Proposals for n = {NUM_PAIRS}')
    plt.xlabel('Number of Proposals')
    plt.ylabel(f'Count')

    # Show the plot
    plt.savefig('Images/distribution_proposals.png')
    plt.close()

    # Doctors Rank Histogram
    summary_stats_df.plot.hist(column=["avg_doctor_rank"], by="n", bins = 10)

    # Add title and labels
    plt.title(f'Distribution of Average Doctors Rank for n = {NUM_PAIRS}')
    plt.xlabel('Average Rank')
    plt.ylabel(f'Count')

    # Show the plot
    plt.savefig('Images/distribution_avg_doctor_rank.png')
    plt.close()

    # Hospitals Rank Histogram
    summary_stats_df.plot.hist(column=["avg_hospital_rank"], by="n", bins = 10)

    # Add title and labels
    plt.title(f'Distribution of Average Hospitals Rank for n = {NUM_PAIRS}')
    plt.xlabel('Average Rank')
    plt.ylabel(f'Count')

    # Show the plot
    plt.savefig('Images/distribution_avg_hospital_rank.png')
    plt.close()


if __name__ == '__main__':
    avg_num_proposals_by_n()
    distribution_proposals_for_n()