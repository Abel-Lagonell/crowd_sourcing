# crowd_sourcing

This is a repository containing all different submodules, as seen in the submodules present.

This readme will go over how to run the main function in this program and detail some of the other functions in the other submodules.

## Running the main function

The main function is located in ```local_Double_POI``` and is called ```systemic_double.py```.
From now on, I will be detailing the instructions to get this Python code to work within a Ubuntu Linux environment.
In the Ubuntu environment, run these commands to install dependencies.
   ```sudo apt-get install python3-tk```
   ```pip install numpy matplotlib scipy```

Then, you will be able to run the file but make sure that where you are located, the files need to be accessed.
There are two main functions in the file,
1. To make the data
2. To graph the data

Both are located in the main function the file will run, whichever is not commented.

There is a third averageTest(), but that function does not run anything that is later saved.

The largeVehicleRegimeineTesting() takes in an integer and saves a data file with that integer at the end. 
-  The data file's name has to be changed later to make whatever you need, as the file's name is hardcoded.
-  The function uses the class nashASsigner to run the main tests of the research paper.

The data produced in the form of graphs are similar to those found under ```Important Figures```

This file can produce both single-point and double-point POI. Although the DoublePOI tests are better run with the original code, the code seen here has been modified.

The other files located in double POI print different graphs that talk about the data located in the CSV's located within the ```local_Double_POI```

## The contents of the rest of the folders

In ```local_temp_cov```, the files are mostly data and graphs, while the python files in the folder deal with generating the files in the folder. These files are more of a prebuilt version of the ones in DoublePOI.

```local_sumo_temp_cov``` is just a folder with data files of all types that sumo uses for their simulation.

```SinglePOI``` is a folder I created that includes the data from the runs of the Single POI done with ```local_Double_POI/systemic_double.py```. Similarly, the ```Important Figures``` are the graphs generated by the function.

```local_Double_POI``` boasts the data gathered for the paper that I modified, with the majority being CSV files.

The rest of the files are miscellaneous folders that either deal with external libraries or papers that this was written for originally.

The original GitHubs:

[Double POI]https://github.com/jcobra713/DoublePOI

[SUMO temporal Coverage]https://github.com/QuentinGoss/sumo-temporal-coverage
