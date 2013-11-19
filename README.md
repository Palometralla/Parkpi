Parkpi
======

Parquímetro LowCost para Raspberry Pi



Parkpi es un parquimetro LowCost para Raspberry Pi, ha sido programado en Python 2.7.3.


	1. Para su instalación es necesario contar con el interprete de Python version 2.7.3

	2. Un servidor de impresion configurado en Raspberry Pi, yo he instalado CUPS y con una 
impresora configurada por defecto.

	3. Es necesario instalar html2ps es un conversor de html a PostScript, lo uso para imprimir
 los tickets de aparcamiento maquetados en html.
	
	4. Necesita instalar la libreria pyBarcode version 0.7

	5. He usado el script de python LCD.py Matt Hawkins para manejar un LCD 16x2 con alguna modificacion para los pulsadores.
	 

	6. Los scripts LCD.py y parki.py asi como la imagen indice.jpg deben de estar en el mismo directorio.

El hardware necesario para usar la aplicación serían 4 pulsadores en configuracion pull-up almentados a 3.3 V y un 
LCD con la configuracion que describe el documento RPi_16x2_LCD.pdf. Un resistor variable de 2.2K para controlar el 
contraste del LCD y una impresora conectada a Raspberry.
