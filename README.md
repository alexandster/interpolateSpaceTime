# STIDW
Performs spatiotemporal domain decomposition followed by inverse distance weighting (IDW) interpolation.
Finds optimal value of power-paremter p by k-fold cross-validation.

Relevant Literature:
Desjardins, M. R., Hohl, A., Griffith, A., & Delmelle, E. (2017). Fine-scale visualization of pollen concentrations across the Eastern United States: A space-time parallel approach. Proceedings of the 2017 International Conference on GeoComputation.
Desjardins M., Hohl, A., Griffith, A., & Delmelle, E. A space-time parallel framework for fine-scale visualization of pollen concentrations across the Eastern United States. (In Review) International Journal of Geographical Information Science.

Files:
dc.py - performs spatiotemporal domain decpomposition
st_idw.py - performs space-time inverse-distance weighting (STIDW) interpolation on the subdomains resulting from dc.py
files/data.txt - random sample data. contains 100 tuples of [x,y,t,p] - x,y: spatial coordinates, t: timestamp, p: feature value to interpolate
files/data_bds.txt - rectangular envelope (domain) of data.txt

Procedure:
To perform space-time interpolation: Execute dc.py first, then st_idw.py. dc.py produces a number of textfiles. st_idw.py takes a parameter which indexes the decomposition output. It performs space-time inverse-distance interpolation (STIDW). Hence, it needs to be executed in a loop or concurrently by multiple processors.
To perform cross-validation on power-parameter p for inverse distance weighting: 1. Create k folds (training/test) by executing n_folds.py (specify the number of folds in the script, default is 10). 2. Decompose training sets by executing decomposition_CV.py, which takes 1 parameter: fold (from 0 to k-1). Do so multiple times for all your folds. 3. Run CV.py (takes 2 parameters: fold, p). Execute multiple times for every combination of fold/p). 4. Run results_CV.py, which prints out a table of performance (error) measures for each value of p. Select p according to the smallest error. 
