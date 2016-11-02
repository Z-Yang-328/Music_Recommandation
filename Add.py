##################################################################
### Summary
## Simply judge like or dislike by adding album and artist rating.

##################################################################
### Libraries & Predefined Functions
## Load Libraries
from __future__ import print_function
from operator import itemgetter
import time
import os
import numpy as np

## Environment Variables
RESULT_FILE = "Results/prediction1.txt"		# Result file
TEST_SCORE_FILE = "Data/test_raw_score.txt"		# Hierarchy score file
none_value = -85 	# Number to replace the none values

# Create Folder is not there
if not os.path.isdir("Results"):
	os.makedirs("Results")

## Functions
# Replace the scores which larger than user mean with '1' and others with '0'.
def sort_list(input_list):
        global i
	for item in input_list:
            if len(item) > 3:
               y=0
               i=3
               for x in range(3,len(item)):
    
                     y=y+item[x]
                     i += 1
            else:
                     y=0
                     
            y=y/(i-2)  
            #sorted_list=[[item[0],item[1]+item[2]+y] for item in input_list]  
            sorted_list=[[item[0],1.2*item[1]+1.1*item[2]+0.5*y] for item in input_list]
            sorted_list=sorted(sorted_list, key = itemgetter(1))
        
	'''
	pred_dic = {}
        mean = np.mean([int(x[1]) for x in sorted_list])
        for item in sorted_list:
            if int(item[1]) > mean:
	         pred_dic[item[0]]=1
	    else:
	         pred_dic[item[0]]=0
        return 	[pred_dic[item[0]] for item in input_list]
        '''
        i = 0
        pred_dic = {}
	for item in sorted_list:
		if i < 3:
			pred_dic[item[0]]=0
		else:
			pred_dic[item[0]]=1
		i += 1
	return 	[pred_dic[item[0]] for item in input_list]
        
# Function that read multiple lines, "num" is the number of lines you want to read
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
### Main Program
## Variables
start_time = time.time()

## Main Program
with open(RESULT_FILE, "w") as predictionFile:
	with open(TEST_SCORE_FILE) as testHierarchy:
		test_list = read_lines(testHierarchy, 6)
		while test_list:
			
			test_list = [item.strip("\n").split("|")[1:] for item in test_list]
			
			# Replace the "None" item with a predefined value.
			# You can also change the value according to the mean rating score of each user.
			for i in range(6):
				test_list[i]=[int(item) if item!="None" else none_value for item in test_list[i]]
			#print(test_list)
			# Sort the list and get prediction
			prediction_result = sort_list(test_list)
                        
			
			# Output prediction to result file 
			for item in prediction_result:
				predictionFile.write(str(item)+"\n")
			
			test_list = read_lines(testHierarchy,6)

print("Finished, spend %.2f s"%(time.time()-start_time))
