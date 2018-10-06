import csv
import pandas as pd
import numpy as np
import random
from PIL import Image,ImageDraw,ImageFont
from player_score import calc_score
from team_fitness import team_fitness, createTeam
from crossover import crossover

# Strategies to assign weight to different features
# Agility, Ball Control, ... , Vision

POP_SIZE = 20
MADRID = [20,15,5,15,5,10,10,0,10,10,0]
BARCA = [0,0,10,5,20,0,5,20,15,5,20]

STRATEGY = []

categories = ['Attacking', 'MidField', 'Defensive', 'GoalKeeper']
base_cost, base_team = 0, ""

teamname = input("Enter the Strategy(BARCA/MADRID): ")

for base_index in range(0,4):
    num_players = int(input("Enter the Number of " + categories[base_index] + " Players: "))
    budget = int(input("Enter the Max Budget in Million Euros (Recommended = " +  str(num_players*60) + "): "))
    
    if teamname == "BARCA":
        STRATEGY = BARCA
    else:
        STRATEGY = MADRID

    included_columns = ['Name', 'Value', 'Acceleration', 'Agility', 'Ball control', 'Crossing', 'Dribbling', 'Heading accuracy', 'Long shots', 'Short passing', 'Sprint speed', 'Strength', 'Vision']

    # Extracting required columns from the Data
    dataFile = pd.read_csv('CompleteDataset.csv')

    listOfPositions = []
    for index in range(0,len(dataFile)):
        if(base_index==0):
            if(('ST' in dataFile.iloc[index]['Preferred Positions'] or 'RW' in dataFile.iloc[index]['Preferred Positions'] or 'LW' in dataFile.iloc[index]['Preferred Positions']) and dataFile.iloc[index]['Preferred Positions'] not in listOfPositions):
                listOfPositions.append(dataFile.iloc[index]['Preferred Positions'])
        if(base_index==1):
            if(('CM' in dataFile.iloc[index]['Preferred Positions'] or 'LM' in dataFile.iloc[index]['Preferred Positions'] or 'RM' in dataFile.iloc[index]['Preferred Positions']) and dataFile.iloc[index]['Preferred Positions'] not in listOfPositions):
                listOfPositions.append(dataFile.iloc[index]['Preferred Positions'])
        if(base_index==2):
            if(('CB' in dataFile.iloc[index]['Preferred Positions'] or 'RB' in dataFile.iloc[index]['Preferred Positions'] or 'LB' in dataFile.iloc[index]['Preferred Positions']) and dataFile.iloc[index]['Preferred Positions'] not in listOfPositions):
                listOfPositions.append(dataFile.iloc[index]['Preferred Positions'])
        else:
            if(('GK' in dataFile.iloc[index]['Preferred Positions']) and dataFile.iloc[index]['Preferred Positions'] not in listOfPositions):
                listOfPositions.append(dataFile.iloc[index]['Preferred Positions'])
    
    # Taking only first 300 Players from the dataset
    dataFile = dataFile[dataFile['Preferred Positions'].isin(listOfPositions)]
    dataSet = dataFile[included_columns][0:301]
    
    population = dataSet[included_columns].values.tolist()
    lim = len(population)-1

    fit, names, finalTeam, currFitness, chromosomes = [], [], "", 0, []

    # Generate initial population by random selection
    for x in range(POP_SIZE):
        chromo = random.sample(range(lim), num_players)
        chromosomes.append(chromo)

    # Evolution over 500 generations
    for gen in range(500):  
        for chromo in chromosomes:
            fitnessValue, teamCost = team_fitness(chromo, budget, population, STRATEGY)
            name = createTeam(chromo, population)
            names.append(name)
            fit.append(fitnessValue)
            if fitnessValue > currFitness:
                finalTeam = name
                finalCost = teamCost
                currFitness = fitnessValue
        
        # Generate next generation
        def ret_fit(elem):
            return team_fitness(elem, budget, population, STRATEGY)
        
        # Top 10 Teams are carried forward to next generation
        next_chromosomes = sorted(chromosomes, reverse = True, key = ret_fit)[0:10]
        
        # Mutation in Teams 5-10, once in every 5 generations 
        def mutate(chromo):
            chromo[random.randint(0,num_players-1)] = random.randint(0,lim)
            chromo[random.randint(0,num_players-1)] = random.randint(50,lim)
            return chromo
        if gen%5 == 0:
            for index in range(5,10):
                next_chromosomes[index] = mutate(next_chromosomes[index])
        
        # Crossover among 10 parents (TBD, 10 new random chromos for now)
        for num in range(0,5):
            cross_chromo = crossover(next_chromosomes[num],next_chromosomes[9-num], budget, population, STRATEGY, lim, num_players)
            next_chromosomes.append(cross_chromo)

        for ctr in range(5):
            chromo = random.sample(range(lim), num_players)
            next_chromosomes.append(chromo)
            
        chromosomes = next_chromosomes

    print(categories[base_index], " Players")
    print(finalTeam)
    print("Total Cost for ", categories[base_index], " Players = $", finalCost, "M")
    base_cost+=finalCost
    base_team= base_team + " " + finalTeam

# Printing out the Final Team & Final Cost
print("Final Team Sheet\n\n" + base_team)
print("Total Team Cost = $ ", base_cost, "M")


teamList = base_team.split(',')
img = Image.new('RGB', (400, 700), color = (26, 188, 156))
fnt = ImageFont.truetype("arial.ttf", 30)
d = ImageDraw.Draw(img)
d.text((100,50), "TEAM SHEET", font = fnt, fill=(255,255,255))
y_index = 65
for pl in teamList:
    d.text((50,y_index), pl, font = fnt, fill=(255,255,255))
    y_index = y_index + 50;
img.save('team_sheet.png')
