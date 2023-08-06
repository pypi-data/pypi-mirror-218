import numpy as np
import concurrent.futures

def initializeWeightsAndBiases(layers):
    model_weights = np.zeros(len(layers), dtype=object)
    model_biases = np.zeros(len(layers), dtype=object)
    for i in range(1, len(layers)):
        match layers[i][1]:
            case "sigmoid":
                model_weights[i] = np.random.uniform(low=-0.1, high=0.1, size=(layers[i][0], layers[i-1][0]))
            case "relu":
                std_dev = np.sqrt(2 / layers[i-1][0])
                model_weights[i] = np.random.normal(loc=0, scale=std_dev, size=(layers[i][0], layers[i-1][0]))
            case "leakyRelu":
                std_dev = np.sqrt(2 / layers[i-1][0])
                model_weights[i] = np.random.normal(loc=0, scale=std_dev, size=(layers[i][0], layers[i-1][0]))
                model_weights[i] *= np.where(model_weights[i] > 0, 1, 0.1)
        model_biases[i] = np.zeros(layers[i][0])
    return model_weights, model_biases

def runModel(model_weights, model_biases, layers, input):
    for layer in range(1,len(layers)):
        input = np.add(np.dot(model_weights[layer], input), model_biases[layer])
        match layers[layer][1]:
            case "sigmoid": input = 1 / (1 + np.exp(-input))
            case "relu": lambda input: (abs(input) + input) / 2
            case "leakyRelu": input = np.maximum(0.1 * input, input)
    return input

def runModelForTraining(model_weights, model_biases, layers, layer_history):
    for layer in range(1,len(layers)):
        layer_history[layer] = np.add(np.dot(model_weights[layer], layer_history[layer-1]), model_biases[layer])
        match layers[layer][1]:
            case "sigmoid": layer_history[layer] = 1 / (1 + np.exp(-layer_history[layer]))
            case "relu": lambda input: (abs(input) + input) / 2
            case "leakyRelu": layer_history[layer] = np.maximum(0.1 * layer_history[layer], layer_history[layer])
    return layer_history

def backprop(data_input, data_output, weights, biases, layers, learning_rate):
    layer_number = len(layers)
    layers_output_space = np.empty(layer_number, dtype=object)
    layers_output_space[0] = data_input
    layers_output_space = runModelForTraining(weights, biases, layers, layers_output_space)
    weights_mod = np.zeros_like(weights)
    biases_mod = np.zeros_like(biases)
    output_error = np.subtract(layers_output_space[-1], data_output)
    match layers[-1][1]:
        case "sigmoid": output_delta = output_error * layers_output_space[-1] * (1 - layers_output_space[-1])
        case "relu": output_delta = output_error * np.where(layers_output_space[-1] > 0, 1, 0)
        case "leakyRelu": output_delta = output_error * np.where(layers_output_space[-1] > 0, 1, 0.1)
    weights_mod[-1] = np.multiply(np.outer(output_delta, layers_output_space[-2]), learning_rate)
    biases_mod[-1] = np.multiply(output_delta, learning_rate)
    for layer in range(layer_number - 2, 0, -1):
        match layers[layer][1]:
            case "sigmoid": delta = np.dot(weights[layer + 1].T, output_delta) * layers_output_space[layer] * (1 - layers_output_space[layer])
            case "relu": delta = np.multiply(np.dot(weights[layer + 1].T, output_delta), np.where(layers_output_space[layer] > 0, 1, 0))
            case "leakyRelu": delta = np.multiply(np.dot(weights[layer + 1].T, output_delta), np.where(layers_output_space[layer] > 0, 1, 0.1))
        weights_mod[layer] = np.multiply(np.outer(delta, layers_output_space[layer - 1]),learning_rate)
        biases_mod[layer] = np.multiply(delta,learning_rate)
        output_delta = delta
    return [weights_mod, biases_mod, abs(np.mean(layers_output_space[-1] - data_output))]

def computeBatch(batch_input, batch_output, batch_size, weights, biases, layers, learning_rate):
    result = [None] * batch_size
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(batch_size):
            result[i] = executor.submit(backprop, batch_input[i], batch_output[i], weights, biases, layers, learning_rate)
    concurrent.futures.wait(result)
    return [a.result() for a in result]

class neuralNetwork:
    def __init__(self, **options):
        if options.get("load"):
            self.load(options.get("load"))
        else:
            if options.get("name") == None: self.name = "unknown"
            else: self.name = options.get("name")
            self.layers = options.get("layers")
            self.initializeWeights()

    def run(self, input):
        return runModel(self.weights, self.biases, self.layers, input)

    def train(self, data_input, data_output, **options):
        batch_size = options.get("batch_size")
        epoch_number = options.get("epoch_number")
        learning_rate = options.get("rate")
        for epoch in range(epoch_number):
            t_loss, t_counter = 0, 0
            batch_start = 0
            batch_end = batch_size
            stopper = False
            while not(stopper):
                batch_result = computeBatch(data_input[batch_start:batch_end], data_output[batch_start:batch_end], batch_end-batch_start, self.weights, self.biases, self.layers, learning_rate)
                self.applyBatch(batch_result)
                t_loss += np.mean([mod[2] for mod in batch_result])
                t_counter += 1
                batch_start += batch_size
                batch_end += batch_size
                if batch_end >= len(data_input):
                    batch_end = len(data_input)
                if batch_start>=len(data_input):
                    stopper = True
            print("Epoch " + str(epoch) + "        Loss = " + str(t_loss/t_counter), end='\r')
        self.save()
        print("\nTraining finished, weights and biases saved.\n")

    def applyBatch(self, batch_result):
        self.weights -= np.mean([mod[0] for mod in batch_result], axis=0)
        self.biases = np.subtract(self.biases, np.mean([mod[1] for mod in batch_result], axis=0))

    def save(self):
        np.savez(self.name + ".npz", matrix1=self.weights, matrix2=self.biases, matrix3=self.layers)

    def load(self, filename):
        data = np.load(filename + ".npz", allow_pickle=True)
        self.weights = data['matrix1']
        self.biases = data['matrix2']
        self.layers = data['matrix3']
        self.name = filename

    def initializeWeights(self):
        self.weights, self.biases = initializeWeightsAndBiases(self.layers)
