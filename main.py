import csv
import pandas as pd
import numpy as np
import random

# Strategies to assign weight to different features
# Agility, Ball Control, ... , Vision

POP_SIZE = 20
MADRID = [20,15,5,15,5,10,10,0,10,10,0]
BARCA = [0,0,10,5,20,0,5,20,15,5,20]
STRATEGY = []

teamname = input("Enter the Strategy(BARCA/MADRID): ")
num_players = int(input("Enter the Number of Players: "))

budget = int(input("Enter the Max Budget in Million Euros (Recommended = " +  str(num_players*60) + "): "))
if teamname == "BARCA":
    STRATEGY = BARCA
else:
    STRATEGY = MADRID

included_columns = ['Name', 'Value', 'Acceleration', 'Agility', 'Ball control', 'Crossing', 'Dribbling', 'Heading accuracy', 'Long shots', 'Short passing', 'Sprint speed', 'Strength', 'Vision']

# Extracting required columns from the Data

dataFile = pd.read_csv('CompleteDataset.csv')
dataSet = dataFile[included_columns]

# Taking only first 100 Players from the dataset
population = dataSet[0:102].values.tolist()

# calculate PlayerScore
def calc_score(player):
    m = np.array(STRATEGY, dtype='float64')
    try:
        p = np.array(player, dtype='float64')
        sum = 0
        res = np.multiply(p,m)
        for i in res:
            sum+=i
        return sum/(11)
    except ValueError:
        return 0

fit = []
names = []

# Calculate Team Fitness, Solutions violating Budget constraint rejected
def team_fitness(team):
    f = 0
    team_value = 0
    for i in team:
        lens = len(population[i][1])
        team_value += float(population[i][1][1:lens-1])
        f+=calc_score(population[i][2:])
    if team_value > budget:
        f = 0
    return f, team_value

# Form a string of Players in Team
def createTeam(team):
    name = ""
    for index in team:
        name = name + "    " + population[index][0]
    return name

finalTeam = ""
currFitness = 0

# Generate initial population by random selection
chromosomes = [random.sample(range(101), num_players) for _ in range(POP_SIZE)]

# Evolution over 500 generations
for gen in range(500):  
    for chromo in chromosomes:
        fitnessValue, teamCost = team_fitness(chromo)
        name = createTeam(chromo)
        names.append(name)
        fit.append(fitnessValue)
        if fitnessValue > currFitness:
            finalTeam = name
            finalCost = teamCost
            currFitness = fitnessValue
    
    # Generate next generation
    def ret_fit(elem):
        return team_fitness(elem)
    
    # Top 10 Teams are carried forward to next generation
    next_chromosomes = sorted(chromosomes, reverse = True, key = ret_fit)[0:10]
    
    # Mutation in Teams 5-10, once in every 5 generations 
    def mutate(chromo):
        chromo[random.randint(0,num_players-1)] = random.randint(0,101)
        chromo[random.randint(0,num_players-1)] = random.randint(50,101)
        return chromo
    if gen%5 == 0:
        for index in range(5,10):
            next_chromosomes[index] = mutate(next_chromosomes[index])
    
    # Crossover among 10 parents (TBD, 10 new random chromos for now)
    for ctr in range(10):
        chromo = random.sample(range(101), num_players)
        next_chromosomes.append(chromo)
        
    chromosomes = next_chromosomes

# Printing out the Final Team & Final Cost
print(teamname)
print(finalTeam)
print("Total Cost = $", finalCost, "M")