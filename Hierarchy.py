##################################################################
## g_Hierarchy.py
#Generate hierarchy structure for a list of track items.

##################################################################
### Libraries & Functions
## Load Libraries
from __future__ import print_function
import time
import sys

## Define variables
TRACK_DATA_FILE = "RawData/trackData2.txt"
TRACK_HIERARCHY_FILE = "RawData/testTrack_hierarchy.txt"
TEST_DATA_FILE = "RawData/testIdx2.txt"

##################################################################
### Main Program
## Load trackData2.txt as Library for hierarchy structure.
# Define hte track-hierarchy structure
lib_trackData = {}
start_time = time.time()
# Hierarchy structure of all the track items are stored in trackData2.txt
with open(TRACK_DATA_FILE) as trackData:
	for line in trackData:
		# We only need the track ID as index, so only split once		
		if sys.version_info.major == 3:
			[track_Id,track_detail] = line.strip("\n").split("|",maxsplit = 1)
		else:
			[track_Id,track_detail] = line.strip("\n").split("|",1)
		lib_trackData[track_Id] = track_detail

## Load list of track items and save the hierarchy structure in a new file
# Open the destiantion file. You can change to your own
with open(TRACK_HIERARCHY_FILE,"w") as testHierarchy:
	# Open the source file, you can use your own source
	with open(TEST_DATA_FILE) as testData:
		for line in testData:
			# "|" represent user information
			if "|" in line:
				[cur_user,cur_track] = line.strip("\n").split("|")

			# Track item have no "|" in the line			
			else:
				cur_track = line.strip("\n")
				testHierarchy.write(cur_user+"|"+cur_track+"|"+lib_trackData[cur_track]+"\n")
			print(cur_user)
print("Finished, Spend %.2f s"%(time.time()-start_time))
