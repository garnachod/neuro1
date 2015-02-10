class Clasificador(object):
	"""docstring for Clasificador"""
	def __init__(self):
		super(Clasificador, self).__init__()

	"""parametros es un string de configuracion para el clasificador"""
	"""para KNN por ejemplo k=11, para una red reuronal,numero de capas
	 	nl=2... cada clasificador se puede preguntar con getCapabilities()"""
	def setParameters(self, parametros):
		raise NotImplementedError( "Should have implemented this" )
		
	"""data es un array de instancias"""
	def buildClassifier(self, data):
		raise NotImplementedError( "Should have implemented this" )

	"""se clasifica una sola instancia, retornando la clase, int"""
	def classifyInstance(self, instance):
		raise NotImplementedError( "Should have implemented this" )

	"""retorna un String JSON para que el Clasificador se pueda guardar en un fichero o donde sea necesario"""
	def saveClassifierToJSON(self):
		raise NotImplementedError( "Should have implemented this" )

	def restoreClassifierFromJSON(self, jsonObj):
		raise NotImplementedError( "Should have implemented this" )

	"""retorna un string con el funcionamiento del Clasificador"""
	def getCapabilities(self):
		raise NotImplementedError( "Should have implemented this" )
