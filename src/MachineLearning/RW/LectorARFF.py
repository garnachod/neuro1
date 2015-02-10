# -*- coding: utf-8 -*-
#import os, sys
#lib_path = os.path.abspath('../')
#sys.path.append(lib_path)

import re
from MachineLearning.Instances import Instances
from MachineLearning.Instance import Instance

class LectorARFF(object):
	"""docstring for LectorARFF"""
	def __init__(self):
		super(LectorARFF, self).__init__()
		self.delimiters = r' |,|\t|\n|\r|\{|\}'

	def leerFichero(self, nombre_fichero):
		f = open(nombre_fichero,'r')
		instances = Instances()
		#espera @RELATION nombre
		#espera tambien @ATTRIBUTE
		#espera tambien @data
		i = 0
		while True:
			linea = f.readline()
			tokens = re.split(self.delimiters, linea)

			if len(tokens) > 1:
				if tokens[0] == '@RELATION':
					continue
				elif tokens[0] == '@ATTRIBUTE':
					if tokens[1] == 'class':
						for indice in range(2, len(tokens)):
							if tokens[indice] != '':
								instances.addClase(tokens[indice])
					elif tokens[2] == 'REAL':
						instances.addColumna(tokens[1], tokens[2])
						continue
					else:
						instances.addColumna(tokens[1], 'NOMINAL')
						continue

				elif tokens[0] == '@DATA':
					print '@DATA'
					break

			i = i+1
			if i > 100:
				print 'Error de fichero'
				return None

		for linea in iter(lambda: f.readline(), ''):
			tokens = self.privateLimpiaVacioTokens(re.split(self.delimiters, linea))
			longitud = len(tokens)
			if longitud > 1:
				#por ahora solo lee reales
				instance = Instance()
				for i in range(0, longitud - 1):
					instance.addElement(float(tokens[i]))

				instance.addElement(tokens[longitud - 1])
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

	def soloLeerCabecera(self, nombre_fichero):
		f = open(nombre_fichero,'r')
		instances = Instances()
		#espera @RELATION nombre
		#espera tambien @ATTRIBUTE
		#espera tambien @data
		i = 0
		while True:
			linea = f.readline()
			tokens = re.split(self.delimiters, linea)

			if len(tokens) > 1:
				if tokens[0] == '@RELATION':
					continue
				elif tokens[0] == '@ATTRIBUTE':
					if tokens[1] == 'class':
						for indice in range(2, len(tokens)):
							if tokens[indice] != '':
								instances.addClase(tokens[indice])
					elif tokens[2] == 'REAL':
						instances.addColumna(tokens[1], tokens[2])
						continue
					else:
						instances.addColumna(tokens[1], 'NOMINAL')
						continue

				elif tokens[0] == '@DATA':
					print '@DATA'
					break

			i = i+1
			if i > 100:
				print 'Error de fichero'
				return None

		f.close()
		return instances


#pruebas unitarias
if __name__ == '__main__':
	lector = LectorARFF()
	instances = lector.leerFichero('../test.arff');
	print len(instances.getListInstances())
		