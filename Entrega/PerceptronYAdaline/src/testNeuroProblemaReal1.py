# -*- coding: utf-8 -*-
import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)
from Clasificadores.Perceptron import Perceptron
from Clasificadores.Adaline import Adaline
from Particionado.DivisionPorcentual import DivisionPorcentual
from Particionado.Particion import Particion
from RW.LectorNeuro import LectorNeuro
from Instance import Instance
from Instances import Instances


def calculaError(clasificador, instances):
	error = 0.0
	erroresPorClase = {}
	aciertosPorClase = {}
	for clase in instances.getClases():
		erroresPorClase[clase] = 0
		aciertosPorClase[clase] = 0

	for instance in instances.getListInstances():
		clase = instance.getClase()
		prediccion = clasificador.classifyInstance(instance)
		#print "clase: " + str(clase) + " prediccion: " + str(prediccion)

		if prediccion != clase:
			erroresPorClase[clase] += 1
			error += 1.0
		else:
			aciertosPorClase[clase] += 1 

	procentajeError = error / float(instances.getNumeroInstances())
	print 'Error medio: ' + str(procentajeError)
	for clase in instances.getClases():
		sumaAux = float(erroresPorClase[clase] + aciertosPorClase[clase])
		print '\t'+ clase + ': ' + str(erroresPorClase[clase]) + ' aciertos: ' + str(aciertosPorClase[clase]) + ' porcentaje: ' + str(erroresPorClase[clase] / sumaAux)

"""pruebas unitarias"""
if __name__ == '__main__':
	lector = LectorNeuro()
	instances = lector.leerFichero('../data/problema_real1.txt');
	
	porcentajeParticionado = 0.7
	particionado = DivisionPorcentual()
	particionado.setPortcentajeTrain(porcentajeParticionado)
	particion = particionado.generaParticionesProporcional(instances)
	
	print "Adaline"
	clasificador = Adaline()
	clasificador.setDebug(True)
	clasificador.buildClassifier(particion.getTrain())
	print "Error TRAIN:"
	calculaError(clasificador, particion.getTrain())
	if porcentajeParticionado != 1.0:
		print "Error TEST:"
		calculaError(clasificador, particion.getTest())
	
	print "Perceptron"
	clasificador = Perceptron()
	clasificador.setDebug(True)
	clasificador.buildClassifier(particion.getTrain())
	print "Error TRAIN:"
	calculaError(clasificador, particion.getTrain())
	if porcentajeParticionado != 1.0:
		print "Error TEST:"
		calculaError(clasificador, particion.getTest())

	#print clasificador.classifyInstance(instances.getListInstances()[4])
	#print (instances.getListInstances()[4]).getClase()

