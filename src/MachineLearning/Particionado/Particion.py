class Particion(object):
	"""docstring for Particion"""
	def __init__(self):
		super(Particion, self).__init__()
		#objeto de tipo Instances
		self.train = None
		self.test = None

	def setTrain(self, instances):
		self.train = instances
		
	def setTest(self, instances):
		self.test = instances

	def getTrain(self):
		return self.train

	def getTest(self):
		return self.test