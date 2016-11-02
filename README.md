# Music_Recommandation
Music Recommandation System based on Yahoo! music dataset.

--Hierarchy.py  generate hierarchy structure for a list of track items.

--Rating.py  generate ratings for all the items in the hierarchy structure.

--matrix_factorization.py  apply matrix_factorization on datasets to make predictions.

--ADD.py  make predictions by simply adding album and artist rating.

--Ensemble.py  ensemble all the results obtained from previous steps and make new predictions.


Here is a instruction about how to use our programs.

1. Run Hierarchy.py to get the hierarchy structure.

2. Run Rating.py to get ratings for every item of each user.

3. Run Add.py to apply our methods by changing some parameters.

---------------------------------------------------------------
Above steps are for Method 1--7 metioned in the report
---------------------------------------------------------------

Method 7

Run matrix_factorization.py to perform matrix factorization method by adjusting rank and numiter

---------------------------------------------------------------
Method 8

Run Ensemble.py to perform ensemble method
