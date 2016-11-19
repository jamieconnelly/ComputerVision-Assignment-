# ComputerVision-Assignment
## Instalation instructions
1. Download this repo and the [training images](https://www.mediafire.com/?xyv14so0xuz2mfx)
2. Unzip the training_images directory and move it to the root directory of the project
3. [Ensure Python 2.7 is installed](https://www.python.org/download/releases/2.7/)
4. [Install Anaconda](https://docs.continuum.io/anaconda/install)
5. Create and activate conda virtual envirnment then install OpenCV
```
	conda create -n yourenvname python=2.7 anaconda
	source activate yourenvname
	conda install -c menpo opencv3=3.1.0
```

## Running the GUI application
Run the command
```
	python main.py
``` 

## Run the classifier script
Run the command
```
	python classifier.py <feature_name>
``` 
where <feature_name> is replaced with one of the following arguments
	* histogram
	* hog
	* hough
	* canny