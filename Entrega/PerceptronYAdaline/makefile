
all:
	@echo "Ejecutando todos los casos de prueba:"
	@echo "-------------------------------------"
	@echo "Ejecutando AND"
	cd src && python testNeuroAND.py
	@echo "-------------------"
	@echo "Ejecutando NAND"
	cd src && python testNeuroNAND.py
	@echo "-------------------"
	@echo "Ejecutando NOR"
	cd src && python testNeuroNOR.py
	@echo "-------------------"
	@echo "Ejecutando OR"
	cd src && python testNeuroOR.py
	@echo "-------------------"
	@echo "Ejecutando Problema Real 1"
	cd src && python testNeuroProblemaReal1.py
	@echo "-------------------"
	@echo "Ejecutando Problema Real 2"
	cd src && python testNeuroProblemaReal2.py
	@echo "-------------------"
	@echo "Ejecutando Problema Real 2 Combinación"
	cd src && python testNeuroProblemaReal2Combinacion.py
	@echo "-------------------"
	@echo "Ejecutando Problema Real 2 No Etiquetados"
	cd src && python testNeuroProblemaReal2NoEtiquetados.py
	@echo "-------------------"
	@echo "Ejecutando XOR"
	cd src && python testNeuroXOR.py
	@echo "-------------------"
	@echo "Ejecutando XOR COmbinados"
	cd src && python testNeuroXORCombinacion.py



help:
	@echo ""
	@echo "Código para simular un Perceptrón y Adaline."
	@echo "Requiere Python 2.7."
	@echo ""
	@echo "No es necesario ejecutar el comando de 'make compile' previamente."
	@echo "El código se encuentra en la carpeta src."
	@echo "Dentro de ella, existen varios ficheros con una función main. Son todos los ficheros testNeuro*.py"
	@echo "Cada uno de ellos ejecuta una de las ejecuciones detalladas a lo largo de la memoria."
	@echo "Para ejecutarlos todos basta con hace 'make' o 'make all'"

compile: ;

clean: 
	rm ./data/predicciones_*.txt
	rm ./src/debugAdaline.txt
	rm ./src/debugPerceptron.txt

