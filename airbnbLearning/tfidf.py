# tfidf scans through the entire dataset to generate the top K (most informative) Ngrams 
# then use the frequencies of such keywords as proxies of descriptions and amenities
# This module takes care of the data cleaning and transformation 
import re, sys, collections, math
from csv import reader
import operator

STOPWORDS_PATH = './stopwords.lst'
stopwords = set([])
with open(STOPWORDS_PATH, "rb") as file:
	lines = file.readlines()
	for line in lines:
		stopwords.add(line.rstrip())
	file.close()

def getNGrams(fPath, col_index, func=lambda x: x, class_index=-1, stopwords=stopwords, n=1, inner_delim=' '):
	tf = collections.defaultdict(int)
	idf = collections.defaultdict(set)
	classCount = {"Luxury": collections.defaultdict(int), "Budget": collections.defaultdict(int), "Premium": collections.defaultdict(int), "Classic": collections.defaultdict(int)}
	N = 4 # total number of data objects
	with open(fPath, 'r') as file:
		lines = reader(file)
		next(lines, None)
		for line in lines:
			#N += 1
			colString = func(line[col_index], ',', stopwords)
			#d = line[0] + ":"
			d = line[class_index] + ":"
			for word in colString:
				tf[d+word] += 1
				idf[word].add(d)
				classCount[d[:-1]][word] += 1

		file.close()
	res = {}
	for key in tf:
		_, t = key.split(':')
		res[key] = tf[key] * math.log(N / len(idf[t]))
	for key in classCount:
		classCount[key] = sorted(classCount[key].items(), key=operator.itemgetter(1), reverse=True)
	sorted_res = sorted(res.items(), key=operator.itemgetter(1), reverse=True)
	return(tf, idf, sorted_res, classCount)

def getAmenities(colString, delim, stopwords):
    return(set([x.lower() for x in re.sub(r'["{}(translation missing: )]', '', colString).split(delim) if x not in stopwords ]))
        


if __name__ == "__main__":
#	fPath = '/home/xiaoyiou/t/laohu/air_train_short.csv'
	fPath = sys.argv[1]
	print(getNGrams(fPath, 3, getAmenities)[2][:100])
