## Dependencies

Make sure to install the following packages before running the stability script.

PyMesh: http://pymesh.readthedocs.io/en/latest/installation.html

numpy-stl: http://numpy-stl.readthedocs.io/en/latest/usage.html#installation

## The Model

*StaticStability.py*: is a class that implements several functions to manipulate and compute properties of the STL mesh. 

*RunStabilityModel.py*: is a script that depends on the Static Stability class and runs the analysis given inputs defined in the file. It outputs images to create an animation of the stability analysis. It also saves numpy objects with righting moment information.

*ProcessMomentOutput.py*: is a script that processes the saved numpy objects so that we can create plots without re-running the entire stability model (which takes several minutes).

To run the model, set your desired parameters and run *RunStabilityModel.py*. Then run *ProcessMomentOutput.py* to create plots of the outputs.



