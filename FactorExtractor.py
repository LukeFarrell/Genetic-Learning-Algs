import numpy as np
import csv
from sklearn.preprocessing import StandardScaler


def extract(ticker, daysBackward):
	factorDict = {}
	ticker = "LUVBBF4"
	with open(ticker + '.csv', 'rb') as factorCsv:
		factorD = csv.DictReader(factorCsv)
		factorNames = factorD.fieldnames
		day = 0
		for row in factorD:
			factorDict[day] = row
			day +=1

	factorNames.remove('Date')
	factorNames.remove('Last Price')

	#Create Factor Dictonaries for Values, Delats, and Percentages
	factorDictDeltas = {}
	factorDictValues = {}
	factorDictPercent = {}
	index = len(factorDict)
	for day in range(2,len(factorDict)):
		index -= 1
		factorDictDeltas[index] = {}
		factorDictValues[index] = {}
		factorDictPercent[index] = {}
		for factor in factorNames:
			factorDictDeltas[index][factor] = float(factorDict[day-1][factor])-float(factorDict[day-2][factor])
			factorDictValues[index][factor] = factorDict[day-1][factor]
			if float(factorDict[day-2][factor]) != 0:
				factorDictPercent[index][factor] = abs((float(factorDict[day-1][factor])-float(factorDict[day-2][factor]))/float(factorDict[day-2][factor]))
			else:
				factorDictPercent[index][factor] = 0

	#Scale Each Dictionary
	scaler = StandardScaler()

	#Scale FactorDictDelats
	x = [[float(factorDictDeltas[day][factor]) for factor in factorDictDeltas[day]] for day in factorDictDeltas]
	factorArray = scaler.fit_transform(x)
	#Replace unscaled values with scaled ones
	dayindex = 0
	for day in factorDictDeltas:
		factorindex = 0
		for factor in factorDictDeltas[day]:
			factorDictDeltas[day][factor] = factorArray[dayindex][factorindex]
			factorindex += 1
		dayindex += 1

	#Scle FactorDictValues
	x = [[float(factorDictValues[day][factor]) for factor in factorDictValues[day]] for day in factorDictValues]
	factorValuesArray = scaler.fit_transform(x)
	#Replace unscaled values with scaled ones
	dayindex = 0
	for day in factorDictValues:
		factorindex = 0
		for factor in factorDictValues[day]:
			factorDictValues[day][factor] = factorValuesArray[dayindex][factorindex]
			factorindex += 1
		dayindex += 1

	#Scle FactorDictPercent
	x = [[float(factorDictPercent[day][factor]) for factor in factorDictPercent[day]] for day in factorDictPercent]
	factorPercentsArray = scaler.fit_transform(x)
	#Replace unscaled values with scaled ones
	dayindex = 0
	for day in factorDictPercent:
		factorindex = 0
		for factor in factorDictPercent[day]:
			factorDictPercent[day][factor] = factorPercentsArray[dayindex][factorindex]
			factorindex += 1
		dayindex += 1

	return factorDictDeltas[daysBackward+1], factorDictValues[daysBackward+1], factorDictPercent[daysBackward+1]

if __name__ == "__main__":
	ticker = "LUVBBF4"
	DAY = 2
	extract(ticker, DAY)
