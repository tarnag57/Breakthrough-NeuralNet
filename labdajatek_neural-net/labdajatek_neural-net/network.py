import numpy as np
from random import randint

mutate_rate = 0.05
threshold = -100

'''
@guvectorize(['void(float64[:,:], float64[:,:], float64[:,:])'],
					'(m,n),(n,p)->(m,p)', target = 'cuda')
def gpu_matmul(A, B, C):
	m, n = A.shape
	n, p = B.shape
	for i in range(m):
		for j in range(p):
			C[i, j] = 0
			for k in range(n):
				C[i, j] += A[i, k] * B[k, j]

def matmul(a, b):
	return np.dot(a, b)	

'''


def network_from_file(file_name):
	file = open(file_name, 'r')
	num_layers = int(file.readline())

	#reading layout
	sizes = []
	for _ in range(0, num_layers):
		size = int(file.readline())
		sizes.append(size)

	#creating object
	net = Network(sizes)

	#changing biases
	for i in range(0, net.num_layers - 1):
		for j in range(0, net.sizes[i + 1]):
			net.biases[i][j][0] = float(file.readline())

	#changing weights
	for i in range(0, net.num_layers - 1):
		for j in range(0, len(net.biases[i])):
			for k in range(0, net.sizes[i]):
				net.weights[i][j][k] = float(file.readline())

	file.close()

	#net.write_to_file("TESTED_NET")

	return net




class Network(object):

	def __init__(self, sizes):

		self.num_layers = len(sizes)
		self.sizes = sizes
		self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
		self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]		#zip([1,2,3] , [4,5,6]) == [[1,4], [2,5], [3,6]]
		self.score = 0

        #biases: [L times sizes[l]*1 matrices]
		#weights: [L times sizes[l]*sizes[l-1] matrices]
		#input layer is the 0th layer

	def add_score(self, score):
		self.score = score

	def feedforward(self, a):
		for b, w in zip(self.biases, self.weights):
			a = np.dot(w, a) + b
			a = sigmoid(a)
		return a

	def breed(self):
		children = []

		for _ in range(0, 4):

			child = Network(self.sizes)

			#mutate biases
			for i in range(0, self.num_layers - 1):
				for j in range(0, self.sizes[i + 1]):
					#mutation
					pivot = np.random.randn()
					if pivot > threshold:
						child.biases[i][j] = self.biases[i][j] + np.random.randn() * mutate_rate
					else:
						child.biases[i][j] = self.biases[i][j]

			#mutate wieghts
			for i in range(0, self.num_layers - 1):
				for j in range(0, len(self.biases[i])):
					for k in range(0, self.sizes[i]):					
						pivot = np.random.randn()
						if pivot > threshold:
							child.weights[i][j][k] = self.weights[i][j][k] + np.random.randn() * mutate_rate
						else:
							child.weights[i][j][k] = self.weights[i][j][k]

			children.append(child)

		return children

	def write_to_file(self, file_name):

		file = open(file_name, 'w')
		
		file.write(str(len(self.sizes)) + '\n')
		for i in range(0, len(self.sizes)):
			file.write(str(self.sizes[i]) + '\n')

		for i in range(0, self.num_layers - 1):
			for j in range(0, self.sizes[i + 1]):
				file.write(str(self.biases[i][j][0]) + '\n')

		for i in range(0, self.num_layers - 1):
			for j in range(0, len(self.biases[i])):
				for k in range(0, self.sizes[i]):
					file.write(str(self.weights[i][j][k]) + '\n')

		file.write("Score: {0}".format(self.score))

		file.close()


def sigmoid(z):
	return 1.0/(1.0 + np.exp(-z))
