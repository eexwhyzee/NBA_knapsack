import csv
import argparse

arg_p = argparse.ArgumentParser()
arg_p.add_argument('-csv', default='')
args = vars(arg_p.parse_args())

CSV = args['csv']

class Player():
    def __init__(self, position, name, salary, points, value):
        self.self = self
        self.position = position
        self.name = name
        self.salary = salary
        self.points = points
        self.value = value
        
    def __iter__(self):
        return iter(self.list)
    
    def __str__(self):
        return "{} {} {} {}".format(self.name,self.position,self.salary, self.points)

with open(CSV,'r') as data:
    reader = csv.reader(data)
    next(reader)
    players = []
    for row in reader:
        name = row[1]
        position = row[0]
        salary = int(row[2])
        points = float(row[4])
        value = points / salary  
        player = Player(position, name, salary, points, value)
        players.append(player)

def lineup_knapsack(players):
    cap = 50000
    current_lineup_cap = 0
    limits = {
        'PG':1,
        'SG':1,
        'SF':1,
        'PF':1,
        'C':1,
        'G':1,
        'F':1,
        'UTIL':1
        }
    
    counter = {
        'PG':0,
        'SG':0,
        'SF':0,
        'PF':0,
        'C':0,
        'G':0,
        'F':0,
        'UTIL':0
        }
    
    players.sort(key=lambda x: x.value, reverse=True)
    lineup = []
    
    for player in players:
        nam = player.name
        pos = player.position
        sal = player.salary
        pts = player.points
        if counter['PG'] < limits['PG'] and current_lineup_cap + sal <= cap and pos in ['PG','PG/SG']:
            lineup.append(player)
            counter['PG'] = counter['PG'] + 1
            current_lineup_cap += sal
            continue
        if counter['SG'] < limits['SG'] and current_lineup_cap + sal <= cap and pos in ['SG','SG/SF']:
            lineup.append(player)
            counter['SG'] = counter['SG'] + 1
            current_lineup_cap += sal
            continue
        if counter['SF'] < limits['SF'] and current_lineup_cap + sal <= cap and pos in ['SF','SF/PF']:
            lineup.append(player)
            counter['SF'] = counter['SF'] + 1
            current_lineup_cap += sal
            continue
        if counter['PF'] < limits['PF'] and current_lineup_cap + sal <= cap and pos in ['PF','PF/C']:
            lineup.append(player)
            counter['PF'] = counter['PF'] + 1
            current_lineup_cap += sal
            continue
        if counter['C'] < limits['C'] and current_lineup_cap + sal <= cap and pos in ['C','PF/C']:
            lineup.append(player)
            counter['C'] = counter['C'] + 1
            current_lineup_cap += sal
            continue
        if counter['G'] < limits['G'] and current_lineup_cap + sal <= cap and pos in ['PG','SG']:
            lineup.append(player)
            counter['G'] = counter['G'] + 1
            current_lineup_cap += sal 
            continue
        if counter['F'] < limits['F'] and current_lineup_cap + sal <= cap and pos in ['SF', 'PF','C']:
            lineup.append(player)
            counter['F'] = counter['F'] + 1
            current_lineup_cap += sal 
            continue
        if counter['UTIL'] < limits['UTIL'] and current_lineup_cap + sal <= cap and pos in ['PG','SG','SF', 'PF','C']:
            lineup.append(player)
            counter['UTIL'] = counter['UTIL'] + 1
            current_lineup_cap += sal 
    
    players.sort(key=lambda x: x.points, reverse=True)
    for player in players:
        nam = player.name
        pos = player.position
        sal = player.salary
        pts = player.points
        if player not in lineup:
            pos_players = [ x for x in lineup if x.position == pos]
            pos_players.sort(key=lambda x: x.points)
            for pos_player in pos_players:
                if (current_lineup_cap + sal - pos_player.salary) <= cap and pts > pos_player.points:
                    lineup[lineup.index(pos_player)] = player
                    current_lineup_cap = current_lineup_cap + sal - pos_player.salary
                    break
    return lineup

lineup = lineup_knapsack(players)
points = 0
salary = 0
for player in lineup:
    points += player.points
    salary += player.salary
    print(player)
print("\nPoints: {}".format(points))
print("Salary: {}".format(salary))