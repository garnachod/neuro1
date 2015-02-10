# -*- coding: utf-8 -*-
from Instance import Instance
from Instances import Instances
from Clasificador import Clasificador
import math   # This will import math module

class NaiveBayes(Clasificador):
	"""docstring for NaiveBayes"""
	def __init__(self):
		super(NaiveBayes, self).__init__()
		self.diccionarioINFO = {}
		self.clases = []
		self.columnas = []
		self.nFilasTrain = 0

	"""parametros es un string de configuracion para el clasificador"""
	"""para KNN por ejemplo k=11, para una red reuronal,numero de capas
	 	nl=2... cada clasificador se puede preguntar con getCapabilities()"""
	def setParameters(self, parametros):
		raise NotImplementedError( "Should have implemented this" )
		
	"""data es un array de instancias"""
	def buildClassifier(self, data):
		listaClases = data.getClases()
		self.clases = list(listaClases)
		listaColumnas = data.getColumnasList()
		self.columnas = list(listaColumnas)
		

		#simulamos unas instacias que contengan todos los elementos
		for clase in listaClases:
			instance = Instance()
			for columna in listaColumnas:
				instance.addElement(1)
			instance.addElement(clase)
			data.addInstance(instance)

		self.nFilasTrain = data.getNumeroInstances()
		#inicializamos el diccionario, va a tener la siguente forma
		#{clase1: {columna1:{media:0.0, varianza:0.0, incidencias:0}}, clase2...}

		for clase in listaClases:
			self.diccionarioINFO[clase] = {}
			self.diccionarioINFO[clase]['rep_clase'] = 0
			for columna in listaColumnas:
				self.diccionarioINFO[clase][columna] = {}
				self.diccionarioINFO[clase][columna]['media'] = 0.0
				self.diccionarioINFO[clase][columna]['varianza'] = 0.0
				self.diccionarioINFO[clase][columna]['incidencias'] = 0

		#****************calculamos la media
		#calculo de la suma
		listaInstancias = data.getListInstances()
		for instancia in listaInstancias:
			clase = instancia.getClase()
			self.diccionarioINFO[clase]['rep_clase'] += 1
			i = 0
			for columna in listaColumnas:
				self.diccionarioINFO[clase][columna]['media'] += instancia.getElementAtPos(i);
				i+=1
		#division para calcular la media
		for clase in listaClases:
			for columna in listaColumnas:
				sumaTotal = self.diccionarioINFO[clase][columna]['media']
				
				incidencias = self.diccionarioINFO[clase]['rep_clase']
				self.diccionarioINFO[clase][columna]['media'] = sumaTotal / float(incidencias)
				#if columna == 'calle':
				#	print columna + ' media'
				#	print self.diccionarioINFO[clase][columna]['media']
		#**************fin del calculo de la media		

		#**************calculo de la varianza
		#calculo de la suma (xi - media)
		for instancia in listaInstancias:
			clase = instancia.getClase()
			i = 0
			for columna in listaColumnas:
				media = self.diccionarioINFO[clase][columna]['media']
				elem = instancia.getElementAtPos(i);
				difCuadrado = math.pow(elem - media, 2)
				self.diccionarioINFO[clase][columna]['varianza'] += difCuadrado
				i+=1
		#division para calcular la varianza
		for clase in listaClases:
			for columna in listaColumnas:
				sumaTotal = self.diccionarioINFO[clase][columna]['varianza']
				incidencias = self.diccionarioINFO[clase]['rep_clase']
				self.diccionarioINFO[clase][columna]['varianza'] = sumaTotal / float(incidencias)
				#print self.diccionarioINFO[clase][columna]['varianza']
				#if columna == 'calle':
				#	print columna + ' varianza'
				#	print self.diccionarioINFO[clase][columna]['varianza']
		#**************fin del calculo de la varianza

	"""se clasifica una sola instancia, retornando la clase, int"""
	def classifyInstance(self, instance):
		mejorClase = None
		mejorProb = -1.0;

		for clase in self.clases:
			#simulacion de la clase, decimos, si fuera esta clase, que prob da
			probClase = 1
			i = 0
			for columna in self.columnas:
				probColumna = 0
				media = self.diccionarioINFO[clase][columna]['media']
				varianza = self.diccionarioINFO[clase][columna]['varianza']

				if varianza != 0.0:
					# Calcular P(D|H) según func. de dist. de una normal
					diferenciaCuadrado = math.pow(instance.getElementAtPos(i) - media, 2)
					aux = -(diferenciaCuadrado / (2.0 * varianza))

					#double elevado = (fila[i].getValorContinuo() - media);
					#elevado = - (Math.pow(elevado, 2.0) / (double)(2.0 * varianza));
					aux = math.exp(aux)
					#elevado = Math.pow(Math.E, elevado);
					#probAux = elevado / (double) Math.sqrt(2.0 * Math.PI * varianza);
					probColumna = aux / math.sqrt(2.0 * math.pi * varianza) 
				else:
					# Si la varianza es 0 se ignora esa columna
					probColumna = 1
					print 'probColumna'
					#

				probClase = probColumna * probClase
				#print probClase
				i+=1
			#fin for columnas
			#print probClase
			probAux = self.diccionarioINFO[clase]['rep_clase']
			#print probAux
			probAux = probAux / float(self.nFilasTrain)
			probClase = probClase*probAux
			

			if probClase > mejorProb:
				mejorProb = probClase
				mejorClase = clase

		return mejorClase


	"""retorna un String JSON para que el Clasificador se pueda guardar en un fichero o donde sea necesario"""
	def saveClassifierToJSON(self):
		raise NotImplementedError( "Should have implemented this" )

	"""retorna un string con el funcionamiento del Clasificador"""
	def getCapabilities(self):
		raise NotImplementedError( "Should have implemented this" )