import pandas as pd

dfRules = pd.read_csv("Rules.csv")
dfRules = dfRules.set_index(['policy','date'])

dfSlopes = pd.read_csv("Slopes.csv")
dfSlopes = dfSlopes.set_index('country')

def optPlan(dfR, dfS, c):
    dfS = dfS.loc[c]
    # dont need to check for NaN values, since
    # 1. Slopes are only NaN if the WHOLE metric fot the country is NaN
    # 2. and so it'd be NaN * NaN (no change)
    # (The slopes will never override data)


    policies = ['Income Tax', 'Demerit Goods Tax', 'Education Spending', 'Healthcare Spending', 'Environment Spending', 'Benefits Spending', 'Interest Rates', 'Regulation', 'Protectionism', 'Infrastructure']

    data = {}

    for policy in policies:
        temp = dfR.loc[policy].sum(axis='index')
        temp = temp * (1 - (5*dfS))
        s = temp.sum()
        data[policy] = s
    print(data)

    # WARNING,, THE KEYS ARE NOT UPDATED TO HAVE _
    Start = {'Income_Tax': data['Income Tax'], 'Demerit_Goods_Tax': data['Demerit Goods Tax']}
    Income_Tax = {'Demerit_Goods_Tax': data['Demerit Goods Tax'], 'Education_Spending': data['Education Spending'], 'Healthcare_Spending': data['Healthcare Spending'], 'Environment_Spending': data['Environment Spending'], 'Benefits_Spending': data['Benefits Spending'], 'Infrastructure': data['Infrastructure']}
    Demerit_Goods_Tax = {'Income_Tax': data['Income Tax'], 'Education_Spending': data['Education Spending'], 'Healthcare_Spending': data['Healthcare Spending'], 'Environment_Spending': data['Environment Spending'], 'Benefits_Spending': data['Benefits Spending'], 'Infrastructure': data['Infrastructure']}
    Education_Spending = {'Regulation': data['Regulation'], 'Protectionism': data['Protectionism'], 'Healthcare_Spending': data['Healthcare Spending'], 'Environment_Spending': data['Environment Spending'], 'Benefits_Spending': data['Benefits Spending'], 'Infrastructure': data['Infrastructure']}
    Healthcare_Spending = {'Regulation': data['Regulation'], 'Protectionism': data['Protectionism'], 'Education_Spending': data['Education Spending'], 'Environment_Spending': data['Environment Spending'], 'Benefits_Spending': data['Benefits Spending'], 'Infrastructure': data['Infrastructure']}
    Benefits_Spending = {'Regulation': data['Regulation'], 'Protectionism': data['Protectionism'], 'Education_Spending': data['Education Spending'], 'Environment_Spending': data['Environment Spending'], 'Healthcare_Spending': data['Healthcare Spending'], 'Infrastructure': data['Infrastructure']}
    Environment_Spending = {'Regulation': data['Regulation'], 'Protectionism': data['Protectionism'], 'Education_Spending': data['Education Spending'], 'Benefits_Spending': data['Benefits Spending'], 'Healthcare_Spending': data['Healthcare Spending'], 'Infrastructure': data['Infrastructure']}
    Infrastructure = {'Regulation': data['Regulation'], 'Protectionism': data['Protectionism'], 'Education_Spending': data['Education Spending'], 'Benefits_Spending': data['Benefits Spending'], 'Healthcare_Spending': data['Healthcare Spending'], 'Environment_Spending': data['Environment Spending']}
    Regulation = {'Protectionism': data['Protectionism'], 'Interest_Rates': data['Interest Rates']}
    Protectionism = {'Regulation': data['Regulation'], 'Interest_Rates': data['Interest Rates']}
    Interest_Rates = {'End': 0}
    End = {}


    nodes = {'Start': Start, 'Income_Tax': Income_Tax, 'Demerit_Goods_Tax': Demerit_Goods_Tax, 'Education_Spending': Education_Spending, 
    'Healthcare_Spending':Healthcare_Spending, 'Benefits_Spending': Benefits_Spending, 'Environment_Spending': Environment_Spending, 
    'Infrastructure': Infrastructure, 'Regulation': Regulation, 'Protectionism': Protectionism, 'Interest_Rates': Interest_Rates, 'End': End}

    start = 'Start'
    distance = {}

    for node in nodes:
        if node == start:
            distance[node] = 0
        else:
            distance[node] = -100000



    priorityQueue = ['Start', 'Income_Tax', 'Demerit_Goods_Tax', 'Education_Spending', 'Healthcare_Spending', 'Benefits_Spending', 'Environment_Spending', 'Infrastructure', 'Regulation', 'Protectionism', 'Interest_Rates', 'End']
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

    return previous, distance


econSimData = []

countries = ["Italy", "United Kingdom", "United States", "France", "Japan", "Germany", "Canada"]
for country in countries:
    route, distances = optPlan(dfRules, dfSlopes, country)

    countryData = {}
    for path in route:
        if 'Negative' in path:
            temp = path.partition(' ')[2]
            countryData[temp] = countryData[temp] - route[path]
        elif path not in econSimData and path != 'End':
            countryData[path] = route[path]
    
    for policy in countryData:
        econSimData.append(countryData[policy])
    

temp = {}
temp['amount'] = econSimData       # just to have the column named 'amount' in the dataframe
econSimData = temp


policies = ['Income_Tax', 'Demerit_Goods_Tax', 'Education_Spending', 'Healthcare_Spending', 'Environment_Spending', 'Benefits_Spending', 'Infrastructure', 'Regulation', 'Protectionism', 'Interest_Rates']

econSimIndex = []
for country in countries:
    for policy in policies:
        econSimIndex.append((country, policy))


econSimIndex = pd.MultiIndex.from_tuples(econSimIndex, names=["country", "policy"])

projectedDf = pd.DataFrame(data= econSimData, index=econSimIndex)
projectedDf.to_csv('EconSimOptPlan.csv')


