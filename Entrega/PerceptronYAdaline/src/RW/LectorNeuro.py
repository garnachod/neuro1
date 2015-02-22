# -*- coding: utf-8 -*-
#solo usar para debug
import os, sys
lib_path = os.path.abspath('../../')
sys.path.append(lib_path)
#fin de solo usar para debug
import re
from src.Instances import Instances
from src.Instance import Instance

class LectorNeuro(object):
	"""docstring for LectorNeuro"""
	def __init__(self):
		super(LectorNeuro, self).__init__()
		self.delimiters = r' |,|\t|\n|\r|\{|\}'


	def leerFichero(self, nombre_fichero):
		f = open(nombre_fichero,'r')
		#instancias al estilo WEKA
		instances = Instances()

		primeraLinea = f.readline()
		cadenasLinea = re.split(self.delimiters, primeraLinea)
		numeroEntradas = int(cadenasLinea[0])
		numeroClases = int(cadenasLinea[1])

		for i in range(0, numeroEntradas):
			instances.addColumna(str(i), "REAL")

		for i in range(0, numeroClases):
			instances.addClase(str(i))

		for line in iter(lambda: f.readline(), ''):
			tokens = self.privateLimpiaVacioTokens(re.split(self.delimiters, line))
			#print tokens
			if len(tokens) <= 0:
				break
			#instancia al estilo WEKA
			instance = Instance()
			#se anyaden las entradas del perceptron
			for i in range(0, numeroEntradas):
				instance.addElement(float(tokens[i]))

			#transformacion de 1 0 a 0 por ejemplo y 0 1 a 1
			#con la finalidad de no usar un array de clases que no tiene sentido en clasificacion
			#puede tener sentido en un red neuronal, no lo niego
			j = 0
			for i in range(numeroEntradas, numeroEntradas + numeroClases):
				if tokens[i] == '1':
					instance.addElement(str(j))
					break

				j += 1

			instances.addInstance(instance)

		f.close()
		return instances

	def privateLimpiaVacioTokens(self, tokens):
		lista = []
		for token in tokens:
			if token == '':
				pass
			else:
				lista.append(token)

		return lista