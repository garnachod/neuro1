# -*- coding: utf-8 -*-
from MachineLearning.Instance import Instance
from MachineLearning.Instances import Instances
from Clasificador import Clasificador
import random
import math   # This will import math module

class Perceptron(Clasificador):
	"""docstring for Perceptron"""
	def __init__(self):
		super(Perceptron, self).__init__()
		self.clases = []
		self.columnas = []
		self.nColumnas = 0
		self.nClases = 0
		self.alpha = 0.1
		self.nEpocas = 10000
		self.umbral = 0

		self.pesosByNeuronaSalida = {}
		self.neuronasEntrada = []

	"""parametros es un string de configuracion para el clasificador"""
	"""para KNN por ejemplo k=11, para una red reuronal,numero de capas
	 	nl=2... cada clasificador se puede preguntar con getCapabilities()"""
	def setParameters(self, parametros):
		raise NotImplementedError( "Should have implemented this" )
		
	"""data es un array de instancias"""
	def buildClassifier(self, data):
		self.clases = list(data.getClases())
		self.columnas = list(data.getColumnasList())
		self.nClases = len(self.clases)
		self.nColumnas = len(self.columnas)

		#iniciar los pesos a valores aleatorios entre -0.5 y 0.5
		for clase in self.clases:
			self.pesosByNeuronaSalida[clase] = []
			for i in range(0, self.nColumnas + 1):
				peso = (random.random() - 0.5)
				self.pesosByNeuronaSalida[clase].append(peso)

		#inicializar las neuronas de entradas
		self.neuronasEntrada = [1 for i in range(0, self.nColumnas + 1)]

		vectoresObjetivos = {}
		for instancia in data.getListInstances():
			vectoresObjetivos[instancia] = self.generaVectorObjetivoSalida(instancia.getClase())

		instancias = data.getListInstances()
		for epoca in range(0, self.nEpocas):
			flagPesos = False
			for instancia in instancias:
				#Establecer las activaciones a las neuronas de entrada
				for indNeurona in range(1, self.nColumnas + 1):
					self.neuronasEntrada[indNeurona] = instancia.getElementAtPos(indNeurona - 1)

				#Calcular la respuesta de cada neurona de salida
				yIn = []
				for clase in self.clases:
					yIn.append(reduce(lambda x, y: x + y, [x * b for (x, b) in zip(self.neuronasEntrada, self.pesosByNeuronaSalida[clase])]))

				for i in range(0, self.nClases):
					if yIn[i] > self.umbral:
						yIn[i] = 1
					elif yIn[i] < -self.umbral:
						yIn[i] = -1
					else:
						yIn[i] = 0

				vectorObjetivo = vectoresObjetivos[instancia]
				
				for j in range(0, self.nClases):
					if yIn[j] != vectorObjetivo[j]:
						#hago cosas
						flagPesos = True
						for indNE in range(0, self.nColumnas + 1):
							self.pesosByNeuronaSalida[self.clases[j]][indNE] += (self.alpha * vectorObjetivo[j] * self.neuronasEntrada[indNE])


			if flagPesos == False:
				break
		

	#private
	def generaVectorObjetivoSalida(self, claseIn):
		vector = []
		for clase in self.clases:
			if clase == claseIn:
				vector.append(1)
			else:
				vector.append(-1)

		return vector

	"""se clasifica una sola instancia, retornando la clase, int"""
	def classifyInstance(self, instance):
		#Establecer las activaciones a las neuronas de entrada
		for indNeurona in range(1, self.nColumnas + 1):
			self.neuronasEntrada[indNeurona] = instance.getElementAtPos(indNeurona - 1)

		yIn = []
		for clase in self.clases:
			yIn.append(reduce(lambda x, y: x + y, [x * b for (x, b) in zip(self.neuronasEntrada, self.pesosByNeuronaSalida[clase])]))

		
		for i in range(0, self.nClases):
			if yIn[i] > self.umbral:
				yIn[i] = 1
			elif yIn[i] < -self.umbral:
				yIn[i] = -1
			else:
				yIn[i] = 0

		#si encuenta un 1 retorna esa clase
		for i in range(0, self.nClases):
			if yIn[i] == 1:
				return self.clases[i]

		#si no ha encontrado un 1, retorna el primer 0
		#si encuenta un 1 retorna esa clase
		for i in range(0, self.nClases):
			if yIn[i] == 0:
				return self.clases[i]

		#si no ha encontrado nada retorna la clase 0
		return self.clases[0]

	"""retorna un String JSON para que el Clasificador se pueda guardar en un fichero o donde sea necesario"""
	def saveClassifierToJSON(self):
		raise NotImplementedError( "Should have implemented this" )

	def restoreClassifierFromJSON(self, jsonObj):
		raise NotImplementedError( "Should have implemented this" )

	"""retorna un string con el funcionamiento del Clasificador"""
	def getCapabilities(self):
		raise NotImplementedError( "Should have implemented this" )
	
		