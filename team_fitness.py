# Calculate Team Fitness, Solutions violating Budget constraint rejected
from player_score import calc_score

def team_fitness(team, budget, population, strategy):
    f = 0
    team_value = 0
    for i in team:
        lens = len(population[i][1])
        try:
            team_value += float(population[i][1][1:lens-1])
        except ValueError:
            team_value += 0
        f+=calc_score(population[i][2:],strategy)
    if team_value > budget:
        f = 0
    return f, team_value

# Form a string of Players in Team
def createTeam(team, population):
    name = ""
    for index in team:
        name = name + "    " + population[index][0]
    return name