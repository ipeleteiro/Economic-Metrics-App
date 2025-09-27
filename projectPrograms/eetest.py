import pandas as pd

df = pd.read_csv("Rules.csv")
df = df.set_index(['policy','date'])


policies = ['Income Tax', 'Demerit Goods Tax', 'Education Spending', 'Healthcare Spending', 'Environment Spending', 'Benefits Spending', 'Interest Rates', 'Regulation', 'Protectionism', 'Infrastructure']

'''
print(df.loc['Demerit Goods Tax'])
print(df.loc['Demerit Goods Tax'].sum(axis='index'))
print(df.loc['Demerit Goods Tax'].sum(axis='index').sum())

temp = df.loc['Protectionism'].sum(axis='index')
temp = temp*10
temp = temp.astype(int)
s = temp.sum()
print(s/10)
temp = temp/10
print(temp)
print(temp.sum())'''

# policy = {'policy2': dist}
'''
nodes = {}

for policy in policies:
    temp = df.loc[policy].sum(axis='index')
    temp = temp*10
    temp = temp.astype(int)
    s = temp.sum()
    nodes[policy] = s/10

print(nodes)

Start = {'Income_Tax': nodes['Income Tax'], 'Demerit_Goods_Tax': nodes['Demerit Goods Tax']}
Income_Tax = {'Demerit_Goods_Tax': nodes['Demerit Goods Tax'], 'Education_Spending': nodes['Education Spending'], 'Healthcare_Spending': nodes['Healthcare Spending'], 'Environment_Spending': nodes['Environment Spending'], 'Benefits_Spending': nodes['Benefits Spending'], 'Infrastructure': nodes['Infrastructure']}
Demerit_Goods_Tax = {'Income_Tax': nodes['Income Tax'], 'Education_Spending': nodes['Education Spending'], 'Healthcare_Spending': nodes['Healthcare Spending'], 'Environment_Spending': nodes['Environment Spending'], 'Benefits_Spending': nodes['Benefits Spending'], 'Infrastructure': nodes['Infrastructure']}
Education_Spending = {'Regulation': nodes['Regulation'], 'Protectionism': nodes['Protectionism'], 'Healthcare_Spending': nodes['Healthcare Spending'], 'Environment_Spending': nodes['Environment Spending'], 'Benefits_Spending': nodes['Benefits Spending'], 'Infrastructure': nodes['Infrastructure']}
Healthcare_Spending = {'Regulation': nodes['Regulation'], 'Protectionism': nodes['Protectionism'], 'Education_Spending': nodes['Education Spending'], 'Environment_Spending': nodes['Environment Spending'], 'Benefits_Spending': nodes['Benefits Spending'], 'Infrastructure': nodes['Infrastructure']}
Benefits_Spending = {'Regulation': nodes['Regulation'], 'Protectionism': nodes['Protectionism'], 'Education_Spending': nodes['Education Spending'], 'Environment_Spending': nodes['Environment Spending'], 'Healthcare_Spending': nodes['Healthcare Spending'], 'Infrastructure': nodes['Infrastructure']}
Environment_Spending = {'Regulation': nodes['Regulation'], 'Protectionism': nodes['Protectionism'], 'Education_Spending': nodes['Education Spending'], 'Benefits_Spending': nodes['Benefits Spending'], 'Healthcare_Spending': nodes['Healthcare Spending'], 'Infrastructure': nodes['Infrastructure']}
Infrastructure = {'Regulation': nodes['Regulation'], 'Protectionism': nodes['Protectionism'], 'Education_Spending': nodes['Education Spending'], 'Benefits_Spending': nodes['Benefits Spending'], 'Healthcare_Spending': nodes['Healthcare Spending'], 'Environment_Spending': nodes['Environment Spending']}
Regulation = {'Protectionism': nodes['Protectionism'], 'Interest_Rates': nodes['Interest Rates']}
Protectionism = {'Regulation': nodes['Regulation'], 'Interest_Rates': nodes['Interest Rates']}
Interest_Rates = {'End': 0}
End = {}'''

A = {'B': -10, 'C': 5}
B = {'C': 2, 'D': -1}
C = {'B': 2, 'D': -3}
D = {}

nodes = {'A': A, 'B': B, 'C': C, 'D': D}

#nodes = {'Start': Start, 'Income_Tax': Income_Tax, 'Demerit_Goods_Tax': Demerit_Goods_Tax, 'Education_Spending': Education_Spending, 
#'Healthcare_Spending':Healthcare_Spending, 'Benefits_Spending': Benefits_Spending, 'Environment_Spending': Environment_Spending, 
#'Infrastructure': Infrastructure, 'Regulation': Regulation, 'Protectionism': Protectionism, 'Interest_Rates': Interest_Rates, 'End': End}

start = 'A'
distance = {}

for node in nodes:
    if node == start:
        distance[node] = 0
    else:
        distance[node] = -100000

print(distance)


#priorityQueue = ['Start', 'Income_Tax', 'Demerit_Goods_Tax', 'Education_Spending', 'Healthcare_Spending', 'Benefits_Spending', 'Environment_Spending', 'Infrastructure', 'Regulation', 'Protectionism', 'Interest_Rates', 'End']
priorityQueue = ['A', 'B', 'C', 'D']
previous = {}

while len(priorityQueue) > 0:
        currentNode = priorityQueue.pop(0)
        for neighbour in nodes[currentNode]:
            newDist = distance[currentNode] + nodes[currentNode][neighbour]
            if newDist > distance[neighbour]:
                distance[neighbour] = newDist
                sortedDist = dict(sorted(distance.items(), key=lambda item: item[1], reverse=True))
                temp = []
                for node in sortedDist:
                    if node in priorityQueue:
                        temp.append(node)
                priorityQueue = temp
                if neighbour not in previous:
                    previous[neighbour] = 1
                else:
                    previous[neighbour] += 1
                
            
            newDist = distance[currentNode] - nodes[currentNode][neighbour]
            if newDist > distance[neighbour]:
                distance[neighbour] = newDist
                sortedDist = dict(sorted(distance.items(), key=lambda item: item[1], reverse=True))
                temp = []
                for node in sortedDist:
                    if node in priorityQueue:
                        temp.append(node)
                priorityQueue = temp
                if ('Negative' + neighbour) not in previous:
                    previous["Negative " + neighbour] = 1
                else:
                    previous["Negative " + neighbour] += 1


for node in distance:
    distance[node] = round(distance[node], 1)

print(previous)
print(distance)