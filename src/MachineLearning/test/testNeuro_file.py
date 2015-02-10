import os, sys
lib_path = os.path.abspath('../')
sys.path.append(lib_path)

from Clasificadores.NaiveBayes import NaiveBayes
from Clasificadores.RedNeuronal import RedNeuronal
from Particionado.DivisionPorcentual import DivisionPorcentual
from Particionado.Particion import Particion
from RW.LectorARFF import LectorARFF
from Instance import Instance
from Instances import Instances
import json

"""pruebas unitarias"""
if __name__ == '__main__':
	lector = LectorARFF()
	instances = lector.leerFichero('test.arff')
	

	particionado = DivisionPorcentual()
	particionado.setPortcentajeTrain(0.7)
	particion = particionado.generaParticionesProporcional(instances)


	clasificador = RedNeuronal()
	clasificador.buildClassifier(particion.getTrain())

	error = 0
	erroresPorClase = {}
	aciertosPorClase = {}
	for clase in instances.getClases():
		erroresPorClase[clase] = 0
		aciertosPorClase[clase] = 0

	for instance in particion.getTest().getListInstances():
		clase = instance.getClase()
		if clasificador.classifyInstance(instance) != clase:
			erroresPorClase[clase] += 1
			error += 1
		else:
			aciertosPorClase[clase] += 1 

	procentajeError = error / float(particion.getTest().getNumeroInstances())
	print 'Error: ' + str(procentajeError)
	for clase in instances.getClases():
		print 'Error '+ clase + ': ' + str(erroresPorClase[clase] ) + ' aciertos: ' + str(aciertosPorClase[clase])

	nombre_fichero = 'pesos.json'
	f = open(nombre_fichero,'w')
	f.write( json.dumps(clasificador.saveClassifierToJSON()))
	f.close()
	f = open(nombre_fichero,'r')
	#stringJson = f.read()
	clasificador = RedNeuronal()
	clasificador.restoreClassifierFromJSON(json.load(f))

	error = 0
	erroresPorClase = {}
	aciertosPorClase = {}
	for clase in instances.getClases():
		erroresPorClase[clase] = 0
		aciertosPorClase[clase] = 0

	for instance in particion.getTest().getListInstances():
		clase = instance.getClase()
		if clasificador.classifyInstance(instance) != clase:
			erroresPorClase[clase] += 1
			error += 1
		else:
			aciertosPorClase[clase] += 1 

	procentajeError = error / float(particion.getTest().getNumeroInstances())
	print 'Error: ' + str(procentajeError)
	for clase in instances.getClases():
		print 'Error '+ clase + ': ' + str(erroresPorClase[clase] ) + ' aciertos: ' + str(aciertosPorClase[clase])

	#print clasificador.classifyInstance(instances.getListInstances()[4])
	#print (instances.getListInstances()[4]).getClase()