import json

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def main():


	font = {'family' : 'normal',
	        'weight' : 'bold',
		        'size'   : 12}
	plt.rc("font", **font)


	fig = plt.figure()
	ax = plt.axes(projection='3d')
	with open("dataS24-1519176396.json", 'r') as dfile:
		data = json.loads(dfile.read())['data']
	kD = []
	qD = []
	timeD = []
	posGenD = []
	steps = []
	data = {int(k):v for k, v in data.items()}
	for k in sorted(data.keys()):
		data[k] = {int(q):i for q,i in data[k].items()}
		for q in sorted(data[k].keys()):
			kD.append(k)
			qD.append(q)
			timeD.append(data[k][q]['avgT'])
			posGenD.append(data[k][q]['avgPosGen'])
			steps.append(data[k][q]['avgSteps'])

	ax.set_xlabel("k", size = 30)
	ax.set_ylabel("Queens", size = 30)
	ax.set_zlabel("Nb of positions explored", size = 30)

	ax.scatter3D(kD, qD, posGenD, c='r', cmap='Greens')

	#ax.bar3d(kD, qD, timeD, 1, 1, 10,  shade = True)

	plt.show()
	Q = 8
	timeD2 = []
	posGenD2 = []
	steps2 = []
	kD2 = []
	posPerStep = []
	for k in sorted(data.keys()):
		kD2.append(k)
		timeD2.append(data[k][Q]['avgT'])
		posGenD2.append(data[k][Q]['avgPosGen'])
		steps2.append(data[k][Q]['avgSteps'])
		posPerStep.append(data[k][Q]['avgPosGen']/data[k][Q]['avgSteps'])

	bestFit = np.polyfit(kD2, posGenD2, 1, full=True)
	print("Best fit data", bestFit)



	#Positions by k
	plt.bar(kD2, posPerStep)
	plt.xlabel('k')
	plt.ylabel('Positions explored by step')
	plt.show()

	#Time by k
	plt.bar(kD2, timeD2)
	plt.xlabel('k', size = 30)
	plt.ylabel('Time(s)', size = 30)
	plt.show()


	#plt.plot(kD2, posGenD2, 'ro')
	plt.bar(kD2, posGenD2)
	plt.xlabel('k', size = 30)
	plt.ylabel('Nb of positions explored', size= 30)
	plt.show()

	#plt.plot(kD2, timeD2, 'ro')
	#plt.bar(kD2, timeD2)
	#plt.show()


	plt.xlabel('k', size = 30)
	plt.ylabel('Nb of iterations', size= 30)
	plt.bar(kD2, steps2)
	plt.show()



if __name__=='__main__':
	main()
