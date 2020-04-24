import math
import random
import pandas as pd

# read in and store data
df = pd.read_csv('rankings.csv')
team_numbers = df['Team Number'].tolist()

# initialize team stats: 0th element is team name, 1st element is number of wins
team_stats = []
for x in range(len(team_numbers)):
	team_stats.append([team_numbers[x], 0])



# create matchups based on a list of teams ordered by rank
def make_matchups(teams):
	matchups = []
	for i in range(int(len(teams)/2)):
		# match the top ranked teams with the lower ranked teams
		matchups.append((teams[i], teams[len(teams)-1-i]))
	return matchups

# complete games for all matchups provided
def play_matchups(matchups):
	results = [0] * len(matchups)
	for i in range(len(matchups)):
		print("Team " + str(matchups[i][0]) + " vs. Team " + str(matchups[i][1]))
		# get winner from each matchup by randomly choosing one of the teams
		results[i] = random.choice(matchups[i])
		print("Winner: " + str(results[i]))
	return results

# recursive function that completes all rounds in a tournament, returns a winner
def complete_rounds(teams_playing, teams_with_byes, round_num):
	if len(teams_playing) == 1:
		return teams_playing
	print("Round of " + str(round_num))
	matchups = make_matchups(teams_playing)
	results = play_matchups(matchups)
	if teams_with_byes:
		results = teams_with_byes + results
	return complete_rounds(results, [], int(round_num / 2))



def make_random_matchups(team_copy):
	matchups = []
	while len(team_copy) > 1:
		team1 = random.randrange(0, len(team_copy))
		team_copy.pop(team1)
		team2 = random.randrange(0, len(team_copy))
		team_copy.pop(team2)
		matchups.append((team1,team2))
	return matchups

def play_rand_matchups(matchups):
	results = [0] * len(matchups)
	for i in range(len(matchups)):
		# get winner from each matchup by randomly choosing one of the teams
		results[i] = random.choice(matchups[i])
		team_stats[results[i]][1] += 1
	print(team_stats)
	return results

def play_10(teams, num):
	if num == 0:
		return
	else:
		team_copy = teams
		print("Here")
		play_rand_matchups(make_random_matchups(team_copy))
		return play_10(teams, num - 1)

# organizes the original number of playing teams and teams with a bye
# initializes game play
def initialize_tournament(teams):
	number_of_byes = 0
	number_of_teams = len(team_numbers)
	if (number_of_teams % 2 != 0): # if there are an odd number of teams
		play_in = random.choice([0, 1]) # simulate a "play in" round for the bottom two teams
		if play_in == 0:
			del teams[-1]
		elif play_in == 1:
			del teams[-2]
		number_of_teams -= 1

	closest_power = 2**(math.ceil(math.log(len(team_numbers),2)))

	# if number of entered teams is a power of two, there must be some byes in the first round
	if math.log(number_of_teams, 2) != math.ceil(math.log(number_of_teams,2)):
		number_of_byes =  closest_power - number_of_teams # this assumes that the number of teams is initially even

	teams_with_byes = team_numbers[:number_of_byes] # teams with higher seeds should get byes
	teams_playing = team_numbers[number_of_byes:]
	return complete_rounds(teams_playing, teams_with_byes, closest_power)

initialize_tournament(team_numbers);











