# -*- coding: utf-8 -*-
from MachineLearning.Instance import Instance
from MachineLearning.Instances import Instances
from Clasificador import Clasificador
import random
import math   # This will import math module
import json

class RedNeuronal(Clasificador):
	"""docstring for RedNeuronal"""
	def __init__(self):
		super(RedNeuronal, self).__init__()
		self.clases = []
		self.columnas = []
		self.nColumnas = 0
		self.nFilasTrain = 0
		self.nClases = 0
		self.capaEntrada = []
		self.pesosCapaOculta = []
		self.pesosCapaSalida = []
		self.neuronasCapaOculta = 20
		self.nEpocas = 500
		self.alpha = 0.1

	"""parametros es un string de configuracion para el clasificador"""
	"""para KNN por ejemplo k=11, para una red reuronal,numero de capas
	 	nl=2... cada clasificador se puede preguntar con getCapabilities()"""
	def setParameters(self, parametros):
		raise NotImplementedError( "Should have implemented this" )
		
	"""data es un array de instancias"""
	def buildClassifier(self, data):
		self.clases = list(data.getClases())
		self.nClases = len(self.clases)
		self.columnas = list(data.getColumnasList())
		self.nColumnas = len(self.columnas)
		self.nFilasTrain = data.getNumeroInstances()

		#creamos las neuronas de entrada
		for indNeurona in range(0, self.nColumnas + 1):
			self.capaEntrada.append(1)

		#inicializamos los pesos de manera aleatoria
		#por cada neurona de la capa oculta
		for indNeurona in range(0, self.neuronasCapaOculta):
			#por cada neurona de la capa de entrada
			self.pesosCapaOculta.append([])
			for indNeuronaEntr in range(0, self.nColumnas + 1):
				peso = (random.random() - 0.5)
				self.pesosCapaOculta[indNeurona].append(peso)

		#inicializamos los pesos de la capa de salida
		for indNeurona in range(0, self.nClases):
			self.pesosCapaSalida.append([])
			for indNeuronaOculta in range(0, self.neuronasCapaOculta + 1):
				peso = (random.random() - 0.5)
				self.pesosCapaSalida[indNeurona].append(peso)

		instancias = data.getListInstances()
		#paso1
		for epoca in range(0, self.nEpocas):
			#print epoca
			#paso2 por cada instancia en train
			for instancia in instancias:
				#***********inicio de Feedforward**********************************
				#paso 3, valores de entrada
				for indNeurona in range(1, self.nColumnas + 1):
					self.capaEntrada[indNeurona] = instancia.getElementAtPos(indNeurona - 1)
				#paso 4, salida neuronas capa oculta, vector Z
				salidaCapaOculta = []
				#z0 siempre es 1
				salidaCapaOculta.append(1)
				#por cada neurona realizamos una salida
				for indNeurona in range(0, self.neuronasCapaOculta):
					suma = 0
					for indNeuronaEntr in range(0, self.nColumnas + 1):
						suma += (self.pesosCapaOculta[indNeurona][indNeuronaEntr] * self.capaEntrada[indNeuronaEntr])
					#aplicamos la sigmoidal a la suma, esto nos da la salida de la neurona
					salidaCapaOculta.append(1.0/(1.0 + math.exp( - suma)))

				#paso 5, calculamos las respuestas de las neuronas de la capa de salida, vector Y
				salidaFinal = []
				for indNeurona in range(0, self.nClases):
					suma = 0
					for indNeuronaOculta in range(0, self.neuronasCapaOculta + 1):
						suma += (self.pesosCapaSalida[indNeurona][indNeuronaOculta] * salidaCapaOculta[indNeuronaOculta])
					#aplicamos la sigmoidal a la suma, esto nos da la salida de la neurona
					salidaFinal.append(1.0/(1.0 + float(math.exp( - suma))))
				#***********fin de Feedforward **********************************
				#***********inicio Retropropagación del error *******************
				#paso 6
				vectorObjetivo = self.generaVectorObjetivoSalida(instancia.getClase())
				restaVOSalida = self.restaVectores(vectorObjetivo, salidaFinal)
				deltaMinusculaK = []
				for indNeuronaSalida in range(0, self.nClases):
					deltaMinusculaK.append(restaVOSalida[indNeuronaSalida] * (salidaFinal[indNeuronaSalida] * (1.0 - salidaFinal[indNeuronaSalida])))
				
				deltaMayusculaJK = []
				for indNeuronaSalida in range(0, self.nClases):
					#calculamos delta mayuscula
					deltaMayusculaJK.append([])
					for indNeuronaOculta in range(0, self.neuronasCapaOculta + 1):
						#print deltaMinusculaK[indNeuronaSalida]
						#print salidaCapaOculta[indNeuronaOculta]
						aux = self.alpha*salidaCapaOculta[indNeuronaOculta]
						#aux = (self.alpha*)
						deltaMayusculaJK[indNeuronaSalida].append(deltaMinusculaK[indNeuronaSalida] * aux)
				#paso 7
				deltaMinusculaJ = []
				for indNeuronaOculta  in range(0, self.neuronasCapaOculta + 1):
					suma = 0
					for indNeurona in range(0, self.nClases):
						suma += self.pesosCapaSalida[indNeurona][indNeuronaOculta] * deltaMinusculaK[indNeurona]

					deltaMinusculaJ.append(suma*(salidaCapaOculta[indNeuronaOculta] * (1 - salidaCapaOculta[indNeuronaOculta])))
				
				deltaMayusculaIJ = []
				for indNeuronaOculta  in range(0, self.neuronasCapaOculta):
					deltaMayusculaIJ.append([])
					for indNeuronaIN in range(0, self.nColumnas + 1):
						deltaMayusculaIJ[indNeuronaOculta].append(self.alpha*deltaMinusculaJ[indNeuronaOculta] * self.capaEntrada[indNeuronaIN])
				#paso 8
				#Actualizar pesos y sesgos
				for indiceClase in range(0, self.nClases):
					self.pesosCapaSalida[indiceClase] = self.sumaVectores(self.pesosCapaSalida[indiceClase] , deltaMayusculaJK[indiceClase])

				for indiceNOculta in range(0, self.nClases):
					self.pesosCapaOculta[indiceNOculta] = self.sumaVectores(self.pesosCapaOculta[indiceNOculta] , deltaMayusculaIJ[indiceNOculta])
	#private
	def generaVectorObjetivoSalida(self, claseIn):
		vector = []
		for clase in self.clases:
			if clase == claseIn:
				vector.append(1)
			else:
				vector.append(0)

		return vector
	#private
	def restaVectores(self, vector1, vector2):
		vector = []
		for i in range(0, len(vector1)):
			vector.append(vector1[i] - vector2[i])

		return vector

	#private
	def sumaVectores(self, vector1, vector2):
		vector = []
		for i in range(0, len(vector1)):
			vector.append(vector1[i] + vector2[i])

		return vector

	#private
	def multiplicaVectorPorCte(self, vector1, cte):
		vector = []
		for i in range(0, len(vector1)):
			vector.append(vector1[i] * cte)

		return vector

		

	"""se clasifica una sola instancia, retornando la clase, int"""
	def classifyInstance(self, instance):
		#***********inicio de Feedforward**********************************
		#paso 3, valores de entrada
		for indNeurona in range(1, self.nColumnas + 1):
			self.capaEntrada[indNeurona] = instance.getElementAtPos(indNeurona - 1)
		#paso 4, salida neuronas capa oculta, vector Z
		salidaCapaOculta = []
		#z0 siempre es 1
		salidaCapaOculta.append(1)
		#por cada neurona realizamos una salida
		for indNeurona in range(0, self.neuronasCapaOculta):
			suma = 0
			for indNeuronaEntr in range(0, self.nColumnas + 1):
				suma += (self.pesosCapaOculta[indNeurona][indNeuronaEntr] * self.capaEntrada[indNeuronaEntr])
			#aplicamos la sigmoidal a la suma, esto nos da la salida de la neurona
			salidaCapaOculta.append(1.0/(1.0 + math.exp( - suma)))

		#paso 5, calculamos las respuestas de las neuronas de la capa de salida, vector Y
		salidaFinal = []
		for indNeurona in range(0, self.nClases):
			suma = 0
			for indNeuronaOculta in range(0, self.neuronasCapaOculta + 1):
				suma += (self.pesosCapaSalida[indNeurona][indNeuronaOculta] * salidaCapaOculta[indNeuronaOculta])
			#aplicamos la sigmoidal a la suma, esto nos da la salida de la neurona
			salidaFinal.append(1.0/(1.0 + math.exp( - suma)))
		#***********fin de Feedforward **********************************
		#print salidaFinal
		for i in range(0, self.nClases):
			if salidaFinal[i] >= 0.500:
				return self.clases[i]

		return self.clases[0]


	"""retorna un String JSON para que el Clasificador se pueda guardar en un fichero o donde sea necesario"""
	def saveClassifierToJSON(self):
		redJSON = {}
		redJSON['n_neuronas'] = self.neuronasCapaOculta
		redJSON['n_entradas'] = self.nColumnas
		redJSON['n_clases'] = self.nClases
		redJSON['clases'] = list(self.clases)
		redJSON['pesos_entrada_oculta'] = self.pesosCapaOculta
		redJSON['pesos_oculta_salida'] = self.pesosCapaSalida

		return redJSON

	def restoreClassifierFromJSON(self, jsonObj):
		self.neuronasCapaOculta = jsonObj['n_neuronas']
		self.nColumnas = jsonObj['n_entradas']
		self.nClases = jsonObj['n_clases']
		self.clases = jsonObj['clases']
		self.pesosCapaOculta = jsonObj['pesos_entrada_oculta']
		self.pesosCapaSalida = jsonObj['pesos_oculta_salida']

		#creamos las neuronas de entrada
		for indNeurona in range(0, self.nColumnas + 1):
			self.capaEntrada.append(1)


	"""retorna un string con el funcionamiento del Clasificador"""
	def getCapabilities(self):
		raise NotImplementedError( "Should have implemented this" )