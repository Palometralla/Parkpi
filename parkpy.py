#! /usr/bin/env python
#-*- coding: ascii -*-
import sys
from datetime import datetime, time
import os
import barcode
from barcode.writer import ImageWriter
import LCD

topmin = 120 #Tiempo maximo de estacionamiento
valmin = 2 # Constante precio del minuto de parking en  centimos de euro
horaini = datetime.strptime("09:00:00", "%H:%M:%S")
horafin = datetime.strptime("21:00:00", "%H:%M:%S")
LCD.GPIO.setwarnings(False)
LCD.main()





LCD.GPIO.add_event_detect(LCD.M_10, LCD.GPIO.FALLING,bouncetime = 500) #Detectar pulsos bajos en pulsadores de entrada
LCD.GPIO.add_event_detect(LCD.M_20, LCD.GPIO.FALLING,bouncetime = 500)
LCD.GPIO.add_event_detect(LCD.M_50, LCD.GPIO.FALLING,bouncetime = 500)
LCD.GPIO.add_event_detect(LCD.ENTER_BUT, LCD.GPIO.FALLING,bouncetime = 200)



while True:
  



  importe = 0.00



  while True:
    fecha = datetime.now()
    d = fecha.strftime("%d/%m/%Y")
    h = fecha.strftime ("%H:%M:%S")
    horaact=datetime.strptime(h,"%H:%M:%S")
    LCD.time.sleep(1)        #minimiza efecto rebote
            
    if (fecha.time() > horaini.time()) & (fecha.time() < horafin.time()):
      
      if LCD.GPIO.event_detected(LCD.ENTER_BUT) and importe > 0.0:
      
	break
      
      elif LCD.GPIO.event_detected(LCD.M_10):
	  importe += 10.0
	  LCD.lcd_byte(LCD.LCD_LINE_1, LCD.LCD_CMD)
	  LCD.lcd_string("Inserted:")
	  LCD.lcd_byte(LCD.LCD_LINE_2, LCD.LCD_CMD)
	  LCD.lcd_string(str("%.2f" %(importe / 100 )) + " Euros")
	
      elif LCD.GPIO.event_detected(LCD.M_20):
	  importe += 20.0
	  LCD.lcd_byte(LCD.LCD_LINE_1, LCD.LCD_CMD)
	  LCD.lcd_string("Inserted:")
	  LCD.lcd_byte(LCD.LCD_LINE_2, LCD.LCD_CMD)
	  LCD.lcd_string(str("%.2f" %(importe / 100 )) + " Euros")
	    
      elif LCD.GPIO.event_detected(LCD.M_50):
	  importe += 50.0
	  LCD.lcd_byte(LCD.LCD_LINE_1, LCD.LCD_CMD)
	  LCD.lcd_string("Inserted:")
	  LCD.lcd_byte(LCD.LCD_LINE_2, LCD.LCD_CMD)
	  LCD.lcd_string(str("%.2f" %(importe / 100 )) + " Euros")
	    
      else:
	      
	  if importe == 0.0:
		
	    LCD.lcd_byte(LCD.LCD_LINE_1, LCD.LCD_CMD)
	    LCD.lcd_string(str(h))
	    LCD.lcd_byte(LCD.LCD_LINE_2, LCD.LCD_CMD)
	    LCD.lcd_string("Insert coin")
		
		
	  else:
		  
	    LCD.lcd_byte(LCD.LCD_LINE_1, LCD.LCD_CMD)
	    LCD.lcd_string("Inserted:")
	    LCD.lcd_byte(LCD.LCD_LINE_2, LCD.LCD_CMD)
	    LCD.lcd_string(str("%.2f" %(importe / 100 )) + " Euros")
		  
    else:
	LCD.lcd_byte(LCD.LCD_LINE_1, LCD.LCD_CMD)
	LCD.lcd_string(str(h))
	LCD.lcd_byte(LCD.LCD_LINE_2, LCD.LCD_CMD)
	LCD.lcd_string("Free parking")
       	  
  saldomin = importe / valmin #* importe #Tiempo de aparcamiento en minutos

  if saldomin > topmin:
 	saldomin = topmin
 	#horend += 2
  	#minend -= 120
    	cambio = (importe - (valmin * topmin)) / 100
    	importe = valmin * topmin
  	LCD.lcd_byte(LCD.LCD_LINE_1, LCD.LCD_CMD)
  	LCD.lcd_string("2 hour max") 
  	LCD.lcd_byte(LCD.LCD_LINE_2, LCD.LCD_CMD) 
  	LCD.lcd_string("Change: "+ str("%.2f" %cambio) + "E")
  	LCD.time.sleep(4)           #Tiempo de impresion 
  
  minend = int(fecha.strftime("%M")) + int(saldomin) #Fin de los minutos aparcados
  horend = int(fecha.strftime("%H")) # Fin de la hora de aparcamiento
 	
  while minend > 60:
	horend += 1
	minend -= 60
	#print minend
	#print "op3"
  nombref= str(fecha)
  x = 0
  
  while not nombref.isalnum():
    charnul = [":", " ", "-", "."]
  
    while x < len(charnul):
      nombref = nombref.replace(charnul[x],"")
      x += 1
      nombref = nombref[0:17]
                   
 
  LCD.lcd_byte(LCD.LCD_LINE_1, LCD.LCD_CMD)
  LCD.lcd_string("Printing ticket:") 
  LCD.lcd_byte(LCD.LCD_LINE_2, LCD.LCD_CMD) 
  LCD.lcd_string(str("Please wait...")) 
  
  varcode="AB" #Codigo ficticio de identificacion de maquina
  
  taginfo = nombref + varcode #taginfo indicara la informacion del barcode compuesto de la fecha hora mas el codigo de maquina

  crea_tag = ImageWriter()
  parkitag=barcode.get('code39',taginfo, crea_tag) # se crea la etiqueta
  filetag = parkitag.save(nombref)# guardamos el tag con el mismo nombre que el ticket
	
  f=open(nombref + '.html','w')               # creamos el ticket
  f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head> <meta http-equiv="content-type" content="text/html;charset=utf-8" /> <meta name="generator" content="Adobe GoLive" /> <title>parki</title> <!-- --></style> </head> <body> <table border="0" cellspacing="0" cellpadding="0"> <tr height="63"> <td nowrap="nowrap" bgcolor="#333399" height="63"></td> <td class="park" nowrap="nowrap" bgcolor="#333399" width="30%" height="63"> <div class="park"> <h5 class="park"></h5> </div> </td> <td nowrap="nowrap" bgcolor="#333399" height="63"></td> <td nowrap="nowrap" bgcolor="#333399" height="63"> <div align="center"> <font size="6" color="white" face="Verdana, Arial, Helvetica, sans-serif"><b>ESTACIONAMIENTO</b></font></div> </td><td nowrap="nowrap" height="63"></td> <td nowrap="nowrap" height="63"><img src="indice.jpg" alt="" height="102" width="102" border="0" /></td> </tr> <tr height="90"> <td nowrap="nowrap" bgcolor="#333399" height="90"></td> <td nowrap="nowrap" bgcolor="#333399" width="30%" height="90"> <div align="center"> <font color="white" face="Verdana, Arial, Helvetica, sans-serif"><strong>Fin de estacionamiento </strong></font></div> </td> <td nowrap="nowrap" bgcolor="#333399" height="90"></td> <td nowrap="nowrap" bgcolor="#333399" height="90"> <div align="center"> <font size="6" color="white" face="Verdana, Arial, Helvetica, sans-serif"><b>REGULADO</b></font></div> </td> <td nowrap="nowrap" height="90"></td> <td nowrap="nowrap" height="90"></td> </tr> <tr> <td nowrap="nowrap"></td> <td nowrap="nowrap" width="30%"><div align="center"><font size="6" face="Verdana, Arial, Helvetica, sans-serif"><b>' + str('%02d' % horend) + ":"+ str('%02d' % minend) +'</b></font></div></td> <td nowrap="nowrap"> <div align="center"> <font size="4" face="Verdana, Arial, Helvetica, sans-serif">' + str("%.2f" %(importe / 100)) +' &euro;</font></div> </td> <td nowrap="nowrap"> <div align="center"> <font size="4" face="Verdana, Arial, Helvetica, sans-serif">'+ str(h) +'</font></div> </td> <td nowrap="nowrap"> <div align="center"> <font size="4" face="Verdana, Arial, Helvetica, sans-serif">'+ str(d) +'</font></div> </td> <td nowrap="nowrap"></td> </tr> <tr> <td nowrap="nowrap" bgcolor="#0079c0"></td> <td nowrap="nowrap" bgcolor="#0079c0" width="30%"></td> <td nowrap="nowrap" bgcolor="#0079c0"> <div align="center"> <font color="white" face="Verdana, Arial, Helvetica, sans-serif">Precio</font></div> </td> <td nowrap="nowrap" bgcolor="#0079c0"> <div align="center"> <font color="white" face="Verdana, Arial, Helvetica, sans-serif">Hora de inicio</font></div> </td> <td nowrap="nowrap" bgcolor="#0079c0"> <div align="center"> <font size="4"color="white" face="Verdana, Arial, Helvetica, sans-serif">Fecha</font></div> </td> <td nowrap="nowrap" bgcolor="#0079c0"> <div align="center"> </div> </td> </tr> <tr> <td nowrap="nowrap"></td> <td nowrap="nowrap" width="30%"><img src="'+ nombref +'.png" alt=""  width="50" border="0" /></td> <td nowrap="nowrap"><font size="3" face="Verdana, Arial, Helvetica, sans-serif">Codigo:</font></td> <td nowrap="nowrap"><font size="3" face="Verdana, Arial, Helvetica, sans-serif">' +varcode + '</font></td> <td nowrap="nowrap"><font size="3" face="Verdana, Arial, Helvetica, sans-serif">Distrito:</font></td> <td nowrap="nowrap"><font size="3" face="Verdana, Arial, Helvetica, sans-serif">84</font></td> </tr> </table> <p></p> </body> </html>') 
  f.close()



  os.system("html2ps \ "+ f.name + " | lp")


  LCD.time.sleep(25)	  

