from team_fitness import team_fitness
import random

def crossover(chromo1, chromo2, budget, population, strategy, lim, num_players):
	position = random.randint(0,len(chromo1))
	for index in range(0,position):
		chromo2[index] = chromo1[index]
	team_value, teamFitness = team_fitness(chromo2, budget, population, strategy)
	if(team_value <= budget):
		return chromo2
	else:
		chromo2 = random.sample(range(lim), num_players)
		return chromo2