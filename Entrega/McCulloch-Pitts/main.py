import sys

class Neurona(object):
	def __init__(self, conexionesEntrantes=[], pesos=[], umbral=0, valor=0):
		super(Neurona, self).__init__()
		self.conexionesEntrantes = conexionesEntrantes
		self.pesos = pesos
		self.umbral = umbral
		self.valor = valor

	def setUmbral(self, umbral):
		self.umbral = umbral

	def calcula(self):
		suma = 0
		for i in range(0, len(self.conexionesEntrantes)):
			suma += self.conexionesEntrantes[i].getValor() * self.pesos[i]

		if suma >= self.umbral:
			self.valor = 1
		else:
			self.valor = 0

	def getValor(self):
		return self.valor

	def setValor(self, valor):
		self.valor = valor


if __name__ == '__main__':
	# Capa de entrada
	neuronaX1 = Neurona()
	neuronaX2 = Neurona()
	neuronaX3 = Neurona()

	entrada = [neuronaX1, neuronaX2, neuronaX3]

	# Capa de retraso
	neuronaZ1 = Neurona([neuronaX1], [2], 2)
	neuronaZ2 = Neurona([neuronaX2], [2], 2)
	neuronaZ3 = Neurona([neuronaX3], [2], 2)

	retraso = [neuronaZ1, neuronaZ2, neuronaZ3]

	# Capa de AND para Abajo
	neuronaZ1X2 = Neurona([neuronaZ1, neuronaX2], [1, 1], 2)
	neuronaZ2X3 = Neurona([neuronaZ2, neuronaX3], [1, 1], 2)
	neuronaZ3X1 = Neurona([neuronaZ3, neuronaX1], [1, 1], 2)

	# Capa de AND para Arriba
	neuronaZ1X3 = Neurona([neuronaZ1, neuronaX3], [1, 1], 2)
	neuronaZ2X1 = Neurona([neuronaZ2, neuronaX1], [1, 1], 2)
	neuronaZ3X2 = Neurona([neuronaZ3, neuronaX2], [1, 1], 2)

	ands = [neuronaZ1X2, neuronaZ2X3, neuronaZ3X1, neuronaZ1X3, neuronaZ2X1, neuronaZ3X2]

	# Neuronas de salida
	abajo = Neurona([neuronaZ1X2, neuronaZ2X3, neuronaZ3X1], [2, 2, 2], 2)
	arriba = Neurona([neuronaZ1X3, neuronaZ2X1, neuronaZ3X2], [2, 2, 2], 2)



	# Ficheros de entrada y salida
	ficheroEntrada = open(sys.argv[1], "r")
	ficheroSalida = open(sys.argv[2], "w")

	# Bucle principal
	for linea in ficheroEntrada:
		valores = map(lambda x: int(x), linea.split(" "))

		# Introducimos los valores a la red
		for i in range(0, len(entrada)):
			entrada[i].setValor(valores[i])
		
		# Para simular correctamente la red de McCulloch-Pitts, vamos calculando los valores
		# desde el final al principio, de tal manera que se van propagando correctamente en el tiempo

		# Primero, la salida
		abajo.calcula()
		arriba.calcula()
		ficheroSalida.write(str(arriba.getValor()) + " " +  str(abajo.getValor())+ "\n")

		# Ahora, la capa del AND
		for neurona in ands:
			neurona.calcula()

		# La capa del retraso
		for neurona in retraso:
			neurona.calcula()

	# Hacemos una iteracion mas, para sacar lo que tengamos procesandose en la red
	abajo.calcula()
	arriba.calcula()
	ficheroSalida.write(str(arriba.getValor()) + " " +  str(abajo.getValor())+ "\n")