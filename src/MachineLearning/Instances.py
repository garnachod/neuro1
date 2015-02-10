class Instances(object):
	"""docstring for Instances"""
	def __init__(self):
		super(Instances, self).__init__()
		self.clases = []
		self.columnas = []
		self.columnaTipo = {}
		self.instances = []

	def setClases(self, clasesPar):
		self.clases = list(clasesPar)

	def addClase(self, clase):
		self.clases.append(clase)

	def getClases(self):
		return self.clases

	def getNumeroColumnas(self):
		return len(self.columnas)

	def getNumeroInstances(self):
		return len(self.instances)

	def addInstance(self, instance):
		self.instances.append(instance)
		instance.setInstances(self)

	def getListInstances(self):
		return self.instances
		
	def addColumna(self, nombreColumna, tipoColumna):
		self.columnas.append(nombreColumna)
		self.columnaTipo[nombreColumna] = tipoColumna

	def setColumnas(self, columnaList, columnaTipo):
		self.columnas = columnaList
		self.columnaTipo = columnaTipo

	def getColumnasTipo(self):
		return self.columnaTipo

	def getColumnasList(self):
		return self.columnas

	def getTipoColumnaByIndex(self, index):
		return self.columnaTipo[self.columnas[index]]

	def getTipoColumnaByNombre(self, nombre):
		return self.columnaTipo[nombre]
