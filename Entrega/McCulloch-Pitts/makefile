
all:
	@echo "Ejecutando todos los casos de prueba:"
	@echo "-------------------------------------"
	python main.py ./data/1.in ./data/1.out
	python main.py ./data/2.in ./data/2.out
	python main.py ./data/3.in ./data/3.out
	@echo ""
	@echo "Comprobación de los resultados"
	@echo "-------------------------------------"
	diff -Bb ./data/1.out ./data/1.test
	diff -Bb ./data/2.out ./data/2.test
	diff -Bb ./data/3.out ./data/3.test

help:
	@echo ""
	@echo "Código para simular una red de McCulloch-Pits."
	@echo "Requiere Python 2.7."
	@echo ""
	@echo "No es necesario ejecutar el comando de 'make compile' previamente."
	@echo "El ejecutable es 'main.py' y recibe como argumento dos parámetros:"
	@echo "\t1. El fichero de entrada."
	@echo "\t2. El fichero de salida."
	@echo ""
	@echo "Si se ejecuta 'make' o 'make all' se ejecutarán tres casos de prueba además de tres comandos diff para comparar la salida real con la esperada."
	@echo "Los ficheros de prueba están en la carpeta 'data':"
	@echo "\tLos *.in son los ficheros de entada"
	@echo "\tLos *.test los ficheros con la salida esprada"
	@echo "\tLos *.txt incluyen una descripción de qué se está probando"

compile: ;

clean: 
	rm ./data/*.out
