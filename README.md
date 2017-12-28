# STIDW
Performs spatiotemporal domain decomposition followed by inverse distance weighting (IDW) interpolation

Relevant Literature:
Desjardins, M. R., Hohl, A., Griffith, A., & Delmelle, E. (2017). Fine-scale visualization of pollen concentrations across the Eastern United States: A space-time parallel approach. Proceedings of the 2017 International Conference on GeoComputation.
Desjardins M., Hohl, A., Griffith, A., & Delmelle, E. A space-time parallel framework for fine-scale visualization of pollen concentrations across the Eastern United States. (In Review) International Journal of Geographical Information Science.

Files:
dc.py - performs spatiotemporal domain decpomposition
st_idw.py - performs space-time inverse-distance weighting (STIDW) interpolation on the subdomains resulting from dc.py
files/data.txt - random sample data. contains 100 tuples of [x,y,t,p] - x,y: spatial coordinates, t: timestamp, p: feature value to interpolate
files/data_bds.txt - rectangular envelope (domain) of data.txt

Procedure:
Execute dc.py first, then st_idw.py. dc.py produces a number of textfiles. st_idw.py takes a parameter which indexes the decomposition output. It performs space-time inverse-distance interpolation (STIDW). Hence, it needs to be executed in a loop or concurrently by multiple processors.

