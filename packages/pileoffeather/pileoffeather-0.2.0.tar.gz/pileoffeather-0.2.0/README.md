<div align="center">
<h1>POF - pile of feather</h1>
<img src="https://github.com/usedToBeTomas/pile-of-feather/blob/main/images/pof.png" width="400" height="400" />

This library is not an alternative to big ml library like pytorch or tensorflow, it lacks features and optimization, such as gpu support. The goal is to create a lightweight library of about 100 lines of code that is easy to use and quick to implement for creating small projects or experiments.

<h3>

[Documentation](https://github.com/usedToBeTomas/pile-of-feather#documentation) | [Examples](https://github.com/usedToBeTomas/pile-of-feather#examples)

</h3>

</div>

---

Install module
```cmd
pip install pileoffeather
```
# Examples
Handwritten digit image classifier, dataset is made out of 500 images of ones and 500 images of zeros taken from the mnist dataset. The first code snippet is defining the neural network model, uploading the dataset and than training the model
```python
from pileoffeather import pof, pod
import numpy as np

#Define neural network model
model = pof.neuralNetwork(layers = [[400,"input"],[30,"relu"],[10,"relu"],[1,"sigmoid"]], name = "test1")

#Load the images for the dataset, 500 ones images and 500 zeros images
ones = pod.load(data_type = "image", color = "grayscale", folder = "ones", resize = (20,20))
zeros = pod.load(data_type = "image", color = "grayscale", folder = "zeros", resize = (20,20))
input = np.vstack((ones, zeros))

#Generate expected output, first 500 images should output 1, the other 500 0
output = np.concatenate((np.ones(500), np.zeros(500)))

#Train the neural network using backpropagation
model.train(input, output, batch_size = 16, epoch_number = 100, rate = 0.6)
```
The second code snippet is testing the neural network on some examples
```python
from pileoffeather import pof, pod
import numpy as np

#Define neural network model
model = pof.neuralNetwork(load = "test1")

#Run model
output = model.run(pod.loadImage("example_image_one.png", (20,20), "grayscale"))

#Print result
print(round(output[0],3))
```

---

# Documentation
The library is structured in 2 files, pof.py (pile of feather) is the library for creating and training neural networks and pod.py (pile of data) is the library for importing your own data to create a training dataset for the neural network.
## pof.py - neural network module
Install module
```cmd
pip install pileoffeather
```
Import module
```python
from pileoffeather import pof
```
Define neural network model, the available activation functions are "sigmoid","relu","leakyRelu"
```python
model = pof.neuralNetwork(layers = [[400,""],[50,"relu"],[10,"relu"],[1,"sigmoid"]], name = "test1")
```
Load an exsisting model
```python
model = pof.neuralNetwork(load = "test1")
```
Save the model
```python
model.save()
```
Train using backpropagation
```python
model.train(input_matrix, output_matrix, batch_size = 16, epoch_number = 100, rate = 0.03)
```
Use the neural network
```python
output = model.run(input)
```

## pod.py - data load module
Import module
```python
from pileoffeather import pod
```
Load images from a folder, color can be set to grayscale or rgb
```python
dataset = pod.load(data_type = "image", color = "grayscale", folder = "folder_name_containing_all_images", resize = (20,20))
```
Load a single image to feed the neural network loadImage(name, resize, color)
```python
input_vector = pod.loadImage("example_image.png", (20,20), "grayscale")
```
Convert neural network output to image and save, saveImage(neural_network_output, image_path, resize, color)
```python
pod.saveImage(neural_network_output, "image_path_and_name", (20,20), "grayscale")
```
