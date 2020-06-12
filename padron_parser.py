import sys
import csv
import re

'''if len(sys.argv) < 2:
	print('Debes pasar el nombre del csv como primer parámetro')
	sys.exit(1)	
FNAME=sys.argv[1]'''

def get_padron(file_path):
	FNAME=file_path
	COL_NUM=0
	COL_APE=1
	COL_NOM=2
	COL_DNI=3

	def printERR(*msgs):
	 print('ERROR:', *msgs)
	def printWARN(*msgs):
	 print('ALERTA:', *msgs)
	 
	nom_ape_regex = re.compile('^[a-zA-ZáéíóúÁÉÍÓÚñ ü\']+$')
	dni_regex = re.compile('^([A-Z]{2}[0-9]{7}|[0-9]{7,9})$')

	def normalizar_caracteres(str):
		return str \
			.replace('á', 'a')\
			.replace('é', 'e')\
			.replace('í', 'i')\
			.replace('ó', 'o')\
			.replace('ú', 'u')\
			.replace('ü', 'u')\
			.replace('ì', 'i')\
			.replace('ö', 'o')\
			.replace('ä', 'a')\
			.replace('´', '\'')\
			.replace('`', '\'')
		
	padron = {}
		
	with open(FNAME, 'r') as csvfile:
		reader = csv.reader(csvfile)
		next(reader)
		for row in reader:
			num=row[COL_NUM].strip()
			ape=normalizar_caracteres(row[COL_APE].replace('-', '').strip().lower())
			nom=normalizar_caracteres(re.sub('(^[a-zA-Zá]{1,2}| [a-zA-Zá]{1,2})\.', '', row[COL_NOM]).strip().lower())
			dni=row[COL_DNI].strip().replace('.','')
			
			if not nom:
				printERR(f'({num}) No se permite nombre vacío (apellido={ape}, dni={dni})')
				continue
			if not nom_ape_regex.match(nom):
				printERR(f'({num}) Nombre inválido: {nom} (apellido={ape}, dni={dni})')
				continue
			if not ape:
				printERR(f'({num}) No se permite apellido vacío (nombre={nom}, dni={dni})')
				continue
			if not nom_ape_regex.match(ape):
				printWARN(f'({num}) Apellido inválido: {ape} (nombre={nom}, dni={dni})')
				pass
			if not dni:
				printERR(f'({num}) Salteando dni vacío (nombre={nom}, apellido={ape})')
				continue
			if not dni_regex.match(dni):
				printWARN(f'({num}) DNI extraño: {dni} (nombre={nom}, apellido={ape})')
				pass
			
			if dni not in padron:
				padron[dni]={'num': num, 'nom': nom, 'ape': ape}
			else:
				# si está en el padrón chequeamos que no sea un duplicado del mismo
				p=padron[dni]
				pnum=p['num']
				pape=p['ape']	
				pnom=p['nom']		
				
				papellidos=[s.strip() for s in pape.split(' ') if s.strip()]
				pnombres=[s.strip() for s in pnom.split(' ') if s.strip()]
				apellidos=[s.strip() for s in ape.split(' ') if s.strip()]
				nombres=[s.strip() for s in nom.split(' ') if s.strip()]
				
				def list_shares_item(list1, list2):
					for l1 in list1:
						if list2.count(l1) > 0:
							return True
					for l2 in list2:
						if list1.count(l2) > 0:
							return True	
					return False
				
				if list_shares_item(papellidos, apellidos) and list_shares_item(pnombres, nombres):
					pass
				else:
					printERR(f'({num}) DNI duplicado: {dni}. Datos cargados #{pnum} "{pnom}" "{pape}". Datos ahora: #{num} "{nom}" "{ape}".')
					#print(f'\nDNI {dni}\n#{pnum} {pnom.title()}, {pape.title()}\n#{num} {nom.title()}, {ape.title()}')
					continue
			#endfor
		#end with
	return padron
