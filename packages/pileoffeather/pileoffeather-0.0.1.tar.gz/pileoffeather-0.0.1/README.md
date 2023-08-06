<div align="center">
<h1>POF - pile of feather</h1>
<img src="https://github.com/usedToBeTomas/pile-of-feather/blob/main/images/pof.png" width="400" height="400" />

Lightweight and easy to use neural network library for small projects, create a neural network in minutes. A fun project.

<h3>

[Homepage](https://github.com/usedToBeTomas/pile-of-feather) | [Documentation](https://github.com/usedToBeTomas/pile-of-feather#documentation) | [Examples](https://github.com/usedToBeTomas/pile-of-feather#examples)

</h3>

</div>

---

# Documentation :book:
The library is structured in 2 files, pof.py (pile of feather) is the library for creating and training neural networks and pod.py (pile of data) is the library for importing your own data to create a training dataset for the neural network.
## pof.py - neural network module
Import module
```python
import pof
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
import pod
```
Load images from a folder
```python
ones = pod.load(data_type = "image", folder = "folder_name_containing_all_images", resize = (20,20))
```


---


# Examples :rocket:
Working in progress...

