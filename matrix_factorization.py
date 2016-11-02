'''
Yahoo Music Dataset prediction using Spark
- By Meng Cao
------------------------------------------------------
** Important **
Need to have all the raw dataset in <RawData> folder
------------------------------------------------------
Instruction
- In the program, the rank can be adjusted and maxIter can
  be increased to impove the performance of Matrix Factorization
  of Spark. However, depends on the computing power and memory,
  Spark will get error when the maxIter exceed certian point.
  So, reduce the training data size will also increase the
  performance

- SQLContext, gives a new data set type called DataFrame. Which
  is like the database of Spark. Once the RDD saved in DataFrame
  format, it will be easier to use some Spark build-in machine
  learning libraries.(pyspark.mllib)
'''

# Import libraries
from __future__ import print_function
from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark.ml.recommendation import ALS
from operator import itemgetter 																																																																																																											
import time
import numpy as np
import os																																																																																																																																																																																																																																																															
import linecache

##################################################################
# Functions
def read_lines(file, num):
	lines = []
	line = file.readline()
	if line:
		lines.append(line.strip().split("|"))
		for i in range(1,num):
			lines.append(file.readline().strip().split("|"))
		return lines
	else:
		return line

def read_lines(file, num):
	lines = []
	line = file.readline()
	lines.append(line)
	if line:
		for i in range(1,num):
			lines.append(file.readline())
		return lines
	else:
		return line

##################################################################
# Programs
start_time = time.time()

# Check if the output folder exist
if not os.path.isdir("Data"):
	os.makedirs("Data")

if not os.path.isdir("Results"):
	os.makedirs("Results")

#Cut train data file
'''
with open("Data/trainData.txt","a") as trainFile:
#with open("Data/trainData3.txt","w") as train:
        list=linecache.getlines("Data/trainData3.txt")
        
train.close()
'''
#Rewrite train data, make it easier to load to spark
with open("Data/trainData.txt","w+") as train:
     with open("Data/trainData2.txt","w") as trainData:
        with open("RawData/trainIdx2.txt") as trainFile:
        #with open("Data/trainData.txt") as trainFile:
		for line in trainFile:
			if "|" in line:
				cur_user = line.split("|")[0]
				print(cur_user,end="\r")		      
                        else:
				train.write(cur_user+"\t"+line)
               
                         
print("----------------------------------------------------------------")
print("Rewrite train data finished, Spend %.2f s"%(time.time()-start_time))
print("----------------------------------------------------------------")

# Rewrite test data, make it easier to load to spark
with open("Data/testData2.txt","w") as testData:
	with open("Data/testData.txt") as testFile:
		for line in testFile:
			if "|" in line:
				cur_user = line.split("|")[0]
				print(cur_user,end="\r")
			else:
				testData.write(cur_user+"\t"+line)
                

print("Rewrite test data finished, Spend %.2f s"%(time.time()-start_time))
print("----------------------------------------------------------------")

print("Start Spark")
print("----------------------------------------------------------------")

sparkC = SparkContext()
sqlC = SQLContext(sparkC)
trainData = sparkC.textFile("Data/trainData.txt").map(lambda line: line.split("\t"))
testData = sparkC.textFile("Data/testData.txt").map(lambda line: line.split("\t"))



# Create data frame for both trainData and testData
trainDataFrame = sqlC.createDataFrame(trainData,["user","item","rating"])
#testData = trainDataFrame.map(lambda p: (p[0], p[1]))
testDataFrame = sqlC.createDataFrame(testData,["user","item"])

# You can change the rank and maxIter here
als = ALS(rank = 8, maxIter = 10)

# Matrix Factorization
model = als.fit(trainDataFrame)
PredTestData = model.transform(testDataFrame)
#print(type(PredTestData))

# Sort prediction by userID
prediction = sorted(PredTestData.collect(), key = lambda r: int(r[0]))
# Output raw prediction to file
with open("Results/raw_prediction.txt","w") as predFile:
	for line in prediction:
		# Check if the prediction is NULL, replace it with "0" or others
		if line[2]!=line[2]:
			temp_str = "0"
		else:
			temp_str = str(int(line[2]))
		predFile.write(str(line[0])+"|"+str(line[1])+"|"+temp_str+"\n")

sparkC.stop()

print("----------------------------------------------------------------")
print("Spark predicting job finished, Spend %d s"%(time.time()-start_time))

print("----------------------------------------------------------------")
print("Start to reorder prediction")
print("----------------------------------------------------------------")

# Even though the prediction is ordered, the item order is not the same
#  with test data

temp_dic = {}
with open("Results/prediction.txt","w") as predFile:
	with open("Results/raw_prediction.txt") as rawFile:
		with open("RawData/testIdx2.txt") as testFile:
			raw_lines = read_lines(rawFile,6)
			while raw_lines:
				temp_dic.clear()
				user_mean = np.mean([int(x[2]) for x in raw_lines])
                               
                                #print(user_median)
				for row in raw_lines:
					if int(row[2])>=user_mean:
						temp_dic[str(row[1])]="1"
					else:
						temp_dic[str(row[1])]="0"
				test_line = testFile.readline()
				# Read testing item and get it from prediction
				for i in range(6):
					test_line = testFile.readline().strip()
                                        predFile.write(temp_dic[test_line]+"\n")
				raw_lines = read_lines(rawFile,6)

print("----------------------------------------------------------------")
print("Reorder prediction finished, Spend %d s"%(time.time()-start_time))
