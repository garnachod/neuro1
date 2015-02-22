# -*- coding: utf-8 -*-
from src.Instance import Instance
from src.Instances import Instances
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
		self.alpha = 0.001
		self.nEpocas = 1000
		self.umbral = 0
		self.debug = False
		self.debugFileName = "debugPerceptron.txt"
		self.debugFile = None

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
			n_errores = 0
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
				
				flagPesos_aux = False
				for j in range(0, self.nClases):
					if yIn[j] != vectorObjetivo[j]:
						#error de clasificacion en la neurona de salida
						flagPesos = True
						flagPesos_aux =True
						auxDeltaPesos = self.alpha * vectorObjetivo[j]
						for indNE in range(0, self.nColumnas + 1):
							self.pesosByNeuronaSalida[self.clases[j]][indNE] += (auxDeltaPesos * self.neuronasEntrada[indNE])
				
				if flagPesos_aux == True:
					#ha habido un error de clasificacion en ese elemento
					n_errores += 1

			if self.debug == True:
				self.debugFile.write(str(epoca) + '\t' + str(n_errores) + '\n')

			if flagPesos == False:
				break

		if self.debug:
			print "# época:", epoca
		

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


		mejorClase = None
		mejorProb = -100.0
		for i in range(0, self.nClases):
			if yIn[i] > mejorProb:
				mejorClase = self.clases[i]
				mejorProb = yIn[i]

		return mejorClase


	"""retorna un String JSON para que el Clasificador se pueda guardar en un fichero o donde sea necesario"""
	def saveClassifierToJSON(self):
		raise NotImplementedError( "Should have implemented this" )

	def restoreClassifierFromJSON(self, jsonObj):
		raise NotImplementedError( "Should have implemented this" )

	"""retorna un string con el funcionamiento del Clasificador"""
	def getCapabilities(self):
		raise NotImplementedError( "Should have implemented this" )
	
	"""Hace que el clasificador entre en modo debug o no"""
	def setDebug(self, value):
		self.debug = value
		if self.debug == True:
			self.debugFile = open(self.debugFileName, 'w')
		