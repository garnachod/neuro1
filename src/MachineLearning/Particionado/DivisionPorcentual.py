# -*- coding: utf-8 -*-
from Particion import Particion
from Particionado import Particionado
from MachineLearning.Instances import Instances
import random




class DivisionPorcentual(Particionado):
	"""docstring for DivisionPorcentual"""
	def __init__(self):
		super(DivisionPorcentual, self).__init__()
		self.porcentaje = 0.0

	def setPortcentajeTrain(self, porcentaje):
		self.porcentaje = porcentaje

	def generaParticiones(self, instances):
		#una sola particion
		particion = Particion()
		#generar las instacias para la particion
		instanceTrain = Instances()
		instanceTest = Instances()
		#	set clases
		instanceTrain.setClases(instances.getClases())
		instanceTest.setClases(instances.getClases())
		#	set columns
		instanceTrain.setColumnas(instances.getColumnasList(), instances.getColumnasTipo())
		instanceTest.setColumnas(instances.getColumnasList(), instances.getColumnasTipo())
		#generar las instancias
		listInstances = list(instances.getListInstances())
		random.shuffle(listInstances)

		n_instances = len(listInstances)
		n_instances_train = int(round(n_instances * self.porcentaje))
		n_instances_test = n_instances - n_instances_train

		#instancias de train
		for i in range(0, n_instances_train):
			instanceTrain.addInstance(listInstances[i])

		#instancias de test
		for i in range(n_instances_train, n_instances):
			instanceTest.addInstance(listInstances[i])

		#añadir a la particion las instancias
		particion.setTrain(instanceTrain)
		particion.setTest(instanceTest)

		return particion

	def generaParticionesProporcional(self, instances):
		#una sola particion
		particion = Particion()
		#generar las instacias para la particion
		instanceTrain = Instances()
		instanceTest = Instances()
		#	set clases
		instanceTrain.setClases(instances.getClases())
		instanceTest.setClases(instances.getClases())
		#	set columns
		instanceTrain.setColumnas(instances.getColumnasList(), instances.getColumnasTipo())
		instanceTest.setColumnas(instances.getColumnasList(), instances.getColumnasTipo())
		#generar las instancias
		listInstances = list(instances.getListInstances())
		random.shuffle(listInstances)

		n_instances = len(listInstances)
		n_instances_train = int(round(n_instances * self.porcentaje))
		n_instances_test = n_instances - n_instances_train

		#conteo de instancias en cada clase
		conteoClases = {}
		conteoIntroducido = {}
		listaClases = instances.getClases()
		for clase in listaClases:
			conteoClases[clase] = {}
			conteoClases[clase]['cont'] = 0
			conteoClases[clase]['instaces_id'] = []
			conteoIntroducido[clase] = 0

		i = 0
		for instancia in listInstances:
			clase = instancia.getClase()
			conteoClases[clase]['cont'] += 1
			conteoClases[clase]['instaces_id'].append(i)
			i+=1

		#instancias de train
		#por cada clase busca se ha de introducir una instancia
		for i in range(0, n_instances_train):
			for clase in listaClases:
				if conteoIntroducido[clase] < ((conteoClases[clase]['cont'] / float(n_instances)) * n_instances_train):
					identificador = conteoClases[clase]['instaces_id'][conteoIntroducido[clase]]
					conteoIntroducido[clase] += 1
					instanceTrain.addInstance(listInstances[identificador])

			#instanceTrain.addInstance(listInstances[i])

		#instancias de test
		for clase in listaClases:
			desde = conteoIntroducido[clase]
			hasta = conteoClases[clase]['cont']
			for i in range(desde, hasta):
				identificador = conteoClases[clase]['instaces_id'][i]
				instanceTest.addInstance(listInstances[identificador])
				conteoIntroducido[clase] += 1

		#for i in range(n_instances_train, n_instances):
		#	instanceTest.addInstance(listInstances[i])

		#añadir a la particion las instancias
		particion.setTrain(instanceTrain)
		particion.setTest(instanceTest)

		return particion