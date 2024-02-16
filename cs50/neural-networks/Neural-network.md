# Neural network 

mimic human brain structure, neuron 

- neurons are connected to and receive electrical signals form other neurons
- neurons process input signals and can be activated 

## Artificial neural network 

mathematical model for learning inspired by biological neural networks 

- model mathematical function from inputs to outputs based on the structure and parameters of the network
- maps input to output based on the structure and parameters of the network
- structure of the network is shaped through training(learning) data 

### Activation functions 

function with threshold based on value to use hypothesis function 

- inputs are modified by weights 

#### Step function 

```
g(x)
if x >= threshold 0:
    = 1
else:
    = 0
``` 

#### Logistic function 

`g(x) = e^x / (e^x + 1)` 

- gives output between 0 and 1
- express graded confidence in its judgment 

#### Rectified Linear Unit(ReLU) 

`g(x) = max(0, x)` 

- output can be any positive value
- set 0 if value is negative 

### In neural network structure 

`h(x1, x2 ...) = g(w0 + w1x1 + w2x2 ...)` 

- each of inputs(`x1, x2`) are connected to the output with the arrows, defined by weights
- output(`g(x)`) is calculated with the inputs and weights
- bias `w0` exists 

### Gradient descent 

algorithm for minimizing loss when training neural network 

- loss: how bad hypothesis function can be 

#### Sequence 

1. start with a random choice of weights
2. repeat
    - calculate the gradient based on **all data points**, direction that will lead to decreasing loss
    - update weights according to the gradient 

#### Stochastic gradient descent 

choose **one data point** instead of **all data points** 

#### Mini batch gradient descent 

choose **one small batch** instead of **all data points** 

### Perceptrom 

units only capable of learning linearly separable decision boundary 

- can classify an input to be one type of another
- problem: data are not always linearly separable 

## Multilayer neural network 

artificial neural network with an input layer, an output layer, and at least one hidden layer 

- first hidden layer
    - receives a weighted value form each of the units in the input layer
    - performs some action on it
    - outputs value
- each of values from hidden layer is weighted and futher propagated to the next layer 
- possible to model non-linear data

### Backpropagation 

algorithm for training neural networks with hidden layers 

#### Sequence 

1. start with a random choice of weights
2. repeat
    - calculate *error* for output layer
    - for each layer starting with output layer, and moving inwards towards earliest hidden layer
        - propagate *error* back one layer
            - send errors from current layer to preceding layer
        - update weights 

### Deep neural networks 

neural network with multiple hidden layers 

### Overfitting 

danger of modeling of training data too closely thus failing to generalize to new data 

#### Dropout 

way to combat overffiting 

- temporarily remove random units to prevent over-reliance on certain units 

### TensorFlow 

library of neural network using backpropagation implementation 

## Computer vision 

computational methods for analyzing and understanding digital images 

- each pixels are represented by three values(acronym RGB) range from 0 to 255 

### Creating neural network 

- input: color value in each pixel
- hidden layer
- ouput: number of units that tells what it is that was shown in the image 

#### Drawback 

1. breaking down the image into pixels and the value of their colors disables using the structure of that image as an aid
2. number of inputs is very big thus have to calculate a lot of weights 

### Image convolution 

applying a filter that adds each pixel value of an image to its neighbors, weighted according to a kernel matrix 

- can extract boundary of an image 

### Pooling 

reducing the size of an input by sampling from regions in the input 

#### Max-pooling 

pooling by choosing the maximum value in each region 

## Convolutional neural network 

neural networks that use convolution usually for analyzing images 

### Method 

repeat convolution and pooling twice 

- first to extract low-level features like edges, curves, shapes
- second to extract high-level features like objects 

## Feed-forward vs. Recurrent neural network 

### Feed-forward neural network 

neural network that has connections only in one direction 

- `input -> network -> output` 

### Recurrent neural network 

neural network that use output as an input 

- helpful in cases where the network deals with sequences and not a single individual object
    - ex: producing sentence about image like captionbot
