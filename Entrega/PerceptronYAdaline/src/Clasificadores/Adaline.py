# -*- coding: utf-8 -*-
from src.Instance import Instance
from src.Instances import Instances
from Clasificador import Clasificador
import random
import math

class Adaline(Clasificador):
	"""docstring for Adaline"""
	def __init__(self):
		super(Adaline, self).__init__()
		self.clases = []
		self.columnas = []
		self.nColumnas = 0
		self.nClases = 0
		self.alpha = 0.1
		self.nEpocas = 1000
		self.debug = False
		self.debugFileName = "debugAdaline.txt"
		self.debugFile = None
		self.errorCuadraticoMedio = 0
		self.errorCuadraticoMedio_old = 0.00000001

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
		self.nInstaces = data.getNumeroInstances()

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
			self.errorCuadraticoMedio = 0
			for instancia in instancias:
				#Establecer las activaciones a las neuronas de entrada
				for indNeurona in range(1, self.nColumnas + 1):
					self.neuronasEntrada[indNeurona] = instancia.getElementAtPos(indNeurona - 1)

				#Calcular la respuesta de cada neurona de salida
				yIn = []
				for clase in self.clases:
					yIn.append(reduce(lambda x, y: x + y, [x * b for (x, b) in zip(self.neuronasEntrada, self.pesosByNeuronaSalida[clase])]))


				vectorObjetivo = vectoresObjetivos[instancia]
				
				for j in range(0, self.nClases):
					diferencia = (vectorObjetivo[j] - yIn[j])
					self.errorCuadraticoMedio += pow(diferencia, 2)
					auxDeltaPesos = self.alpha * diferencia
					for indNE in range(0, self.nColumnas + 1):
						self.pesosByNeuronaSalida[self.clases[j]][indNE] += (auxDeltaPesos * self.neuronasEntrada[indNE])

			#calculo del error cuadratico medio de la época
			self.errorCuadraticoMedio = self.errorCuadraticoMedio/float(self.nInstaces)
			if self.debug == True:
				self.debugFile.write(str(epoca) + '\t' + str(self.errorCuadraticoMedio) + '\n')
				difErrCuadratico = abs((self.errorCuadraticoMedio - self.errorCuadraticoMedio_old)/self.errorCuadraticoMedio_old)
				
				if difErrCuadratico < 0.00000001:
					print "# época:", epoca
					return

				self.errorCuadraticoMedio_old = self.errorCuadraticoMedio
			else:
				difErrCuadratico = abs((self.errorCuadraticoMedio - self.errorCuadraticoMedio_old)/self.errorCuadraticoMedio_old)
				if difErrCuadratico < 0.00000001:
					return
					
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
		