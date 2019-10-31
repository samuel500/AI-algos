#Samuel Knoche
#Beam search to find a solution to the N-Queens problem

from operator import itemgetter
import random
import time
import sys
import json

#Counts the number of queen pairs attacking each other
def countQueenPairs(V):
	allPairs = []
	nbPairs = 0
	for i in range(len(V)):
		x1 = i
		y1 = V[i]

		for y in range(i+1, len(V)):
			x2 = y
			try:
				y2 = V[y]
			except:
				print("V: ", V)
				raise
			if y1 == y2 or y1-x1 == y2-x2 or y1+x1 == y2+x2:
				allPairs.append((i,y))
				nbPairs += 1
	return nbPairs


#Generates a list of nbOfP random positions
def generatePositions(nbOfP, nQueens):

	positions = []
	for i in range(nbOfP):
		newP = random.sample(range(0,nQueens), nQueens)
		#if newP not in positions:
		positions.append(newP)

	return positions


#Returns all possible changes by moving only one Queen from position V
def possibleChanges(V, nQueens):
	allChanges = [] #(fromRow, toColumn)
	for i in range(len(V)):
		iChanges = list(range(nQueens))
		iChanges.remove(V[i])
		for y in iChanges:
			allChanges.append((i, y))

	return allChanges


#Searches a solution to the nQueens-Queens problem by using k beams
def beamSearch(k, nQueens):
	queue = generatePositions(k, nQueens)
	nSet = set()
	stepCount = 1
	queueCount = len(queue)
	generatedPositionsCount = len(queue)


	for V in queue:
		nSet.add(str(V))
		if not countQueenPairs(V):
			return {'V': V, 'data': {'queueCount': queueCount, 'stepCount': stepCount, 'generatedPositionsCount': generatedPositionsCount}}

	while queue:

		allChanges = []
		found = False
		for i in range(len(queue)):

			allPossibleChanges = possibleChanges(queue[i], nQueens)
			for change in allPossibleChanges:
				V1 = list(queue[i])
				V1[change[0]] = change[1]
				allChanges.append({'V': V1, 'score': countQueenPairs(V1)})
				if allChanges[-1]['score'] == 0:
					generatedPositionsCount += len(allChanges)
					return {'V': allChanges[-1]['V'], 'data': {'queueCount': queueCount, 'stepCount': stepCount, 'generatedPositionsCount': generatedPositionsCount}}
		generatedPositionsCount += len(allChanges)
		allChanges = sorted(allChanges, key=itemgetter('score'))
		queue = []
		i = 0
		y = 0
		while i < k and y < len(allChanges):
			if not str(allChanges[y]['V']) in nSet:
				queue.append(allChanges[y]['V'])
				nSet.add(str(allChanges[y]['V']))
				i += 1
			y+=1

		queueCount += len(queue)
		stepCount += 1


#Displays board V
def displayBoard(V):

	for i in reversed(range(len(V))):
		blanks = [' ']*len(V)
		try:
			blanks[V.index(i)] = 'Q'
		except ValueError:
			pass

		print(("|"+len(V)*"{}|").format(*blanks))


#Runs beamSearch nbOfI times and gathers performance data
def beamSearchTime(nbOfI, k, nQueens, verbose = False):
	global solSets
	print("#TEST k =", k, "; nQueens =", nQueens)
	avgTime = 0
	totTime = 0
	startT = time.time()
	totPositionsCount = 0
	totSteps = 0
	for i in range(nbOfI):
		s = beamSearch(k, nQueens)
		solSets[nQueens].add(json.dumps(s['V']))
		if verbose:
			print("Found solution(" + str(i+1) + '/' + str(nbOfI) + "):")
			print(s['V'])
			displayBoard(s['V'])
		else:
			sys.stdout.write("\r{}/{}".format(str(i+1), str(nbOfI)))
		totPositionsCount += s['data']['generatedPositionsCount']
		totSteps += s['data']['stepCount']
	lengthT = time.time() - startT
	avgT = lengthT/nbOfI
	avgSteps = totSteps/nbOfI
	avgPosGen = totPositionsCount/nbOfI

	print("\nBeam Search takes on average " + str(avgT) + " s and generates on average " + str(avgPosGen) + " positions. It went through an average of " + str(avgSteps) + " iterations to find the solution. (averages of " + str(nbOfI) + " samples)")
	return {'avgT': avgT, 'avgSteps': avgSteps, 'avgPosGen': avgPosGen}


#Runs the program
def main():
	startMain = time.time()
	isVerbose = True #Displays all solutions found if True
	writeData = False #Puts data perf data into json file if True
	ks = [1,10,50]#list(range(1,51))
	samples = 8
	nQueens = [8] #list(range(4,19))

	data = {l:{q:None for q in nQueens} for l in ks}
	global solSets
	solSets = {l:set() for l in nQueens}


	for k in ks:
		for q in nQueens:
			data[k][q] = beamSearchTime(samples, k, q, isVerbose)

	if writeData:
		dataJ = json.dumps({'data': data})
		dataFileName = "data/dataS" + str(samples) + '-' + str(int(time.time())) + ".json"
		with open(dataFileName, 'w') as datafile:
			datafile.write(dataJ)


		for k in solSets:
			solSets[k] = list(solSets[k])

		dataJ = json.dumps(solSets)
		solutionsFileName = "data/solutionsS" + str(samples) + '-' + str(int(time.time())) + ".json"

		with open(solutionsFileName, 'w') as datafile:
			datafile.write(dataJ)

	print("time:", str(time.time() - startMain), "s.")




if __name__ == "__main__":
	main()
