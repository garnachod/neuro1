class Instance(object):
	"""docstring for Instance"""
	def __init__(self):
		super(Instance, self).__init__()
		self.listaDatos = []
		self.instances = None
	
	def addElement(self, elemento):
		self.listaDatos.append(elemento)

	def setInstances(self, instances):
		self.instances = instances

	def getElementAtPos(self, pos):
		return self.listaDatos[pos]

	def getAllElements(self):
		return self.listaDatos

	def getClase(self):
		longitud = len(self.listaDatos)
		return self.listaDatos[longitud - 1]

		