##################################################################
## gscore_Hie.py
# Generate ratings for all the item in the hierarchy structure.


##################################################################
## Libraries & Functions
# Load Libraries
from __future__ import print_function
import time
import os
import linecache

# Environment Variables
TEST_HIE_SCORE = 'Data/test_raw_score.txt'
TEST_HIE_FILE = 'RawData/testTrack_hierarchy.txt'
TRAIN_DATA_FILE = 'RawData/trainIdx2.txt'
# Create Folder is not there
if not os.path.isdir("Data"):
	os.makedirs("Data")
	
# Functions
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
## Define Variables
train_dict = {}
train_user = -1
start_time = time.time()



## Read file
# Destination file
with open(TEST_HIE_SCORE,'w') as testResult:
	# Source file that contains the item ID in the hierarchy structure
	with open(TEST_HIE_FILE) as testData:
		# Source file that contains the item ratings by each user.
		with open(TRAIN_DATA_FILE) as trainData:
			# 6 test song for each user
                        

			lines_test = read_lines(testData,6)
                        
			while lines_test:
				cur_test = lines_test[0].strip("\n").split("|")
				cur_user = cur_test[0]

				# Navigate to the current user in training data.
				while int(train_user) < int(cur_user):
					lines_train = trainData.readline()
					[train_user,train_user_rates] = lines_train.strip("\n").split("|")
					lines_train = read_lines(trainData,int(train_user_rates))
					
				# Set Up Dictionary for the current user.
				train_dict.clear()
				for line_train in lines_train:
					train_dict_item = line_train.strip("\n").split("\t")
					train_dict[train_dict_item[0]] = train_dict_item[1]
				# Get ratings for each line in hierarchy structure.
				for line_test in lines_test:
					test_song = line_test.strip("\n").split("|")
					testResult.write(cur_user+"|"+test_song[1]+"|")
					#print(cur_user,train_user,train_user_rates,time.time()-start_time)
					del test_song[:2]
					cur_rating = [train_dict[x] if x in train_dict else "None" for x in test_song ]
								
					testResult.write("|".join(cur_rating))
					testResult.write("\n")
				# Read hierarchy structure for next user
				lines_test = read_lines(testData,6)
				print(cur_user,"%.2f s"%(time.time()-start_time))
				#print("Next User")
print("Finished, Spend %.2f s"%(time.time()-start_time))

