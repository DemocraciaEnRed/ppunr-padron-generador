import csv, re, sys

'''
Este archivo tiene la data formateada así:
# no duplicados.csv
GUARNIZO CABRERA;JHOAN SEBASTI�N;CI;1006513895;21/02/2000;MASCULINO
REINES URIELES;JUAN SEBASTIAN;CI;1010140098;29/05/2000;MASCULINO
...
# Agregar PP Facultades.csv
Apellido,Nombre,Identificación,Número
ACQUARONE,Alicia,DNI,10187728
CHIROLEU,Adriana Rosa,DNI,13174062
...
'''

FNAME='Agregar PP Facultades.csv'
DELIMETER=','
ENCODING='utf8'
JUMP_FIRST=True
COL_DNI=3

#FNAME='no duplicados.csv'
#DELIMETER=';'
#ENCODING='latin1'
#JUMP_FIRST=False
#COL_DNI=3
COL_APES=0
COL_NOMS=1

REPORTAR_RAREZAS=False

def printERR(*msgs):
 print('ERROR:', *msgs)
def printWARN(*msgs):
 print('ALERTA:', *msgs)

dni_regex = re.compile('^[a-zA-Z0-9-]{3,11}$')
has_letter = re.compile('[a-zA-Z]+')

dnis = set()
if REPORTAR_RAREZAS:
	dnis_con_e = []
	dnis_con_letras = []
	dnis_con_guion = []
	dnis_cortos_7 = []
	dnis_cortos_6 = []

with open(FNAME, 'r', encoding=ENCODING) as csvfile:
	reader = csv.reader(csvfile, delimiter=DELIMETER)

	# esto si la primer línea tiene headers
	if JUMP_FIRST:
		next(reader)

	LINE_N=0
	for row in reader:
		LINE_N+=1

		if len(row) < COL_DNI-1:
			printWARN(f'#{LINE_N} Salteando línea vacía o con menos campos')
			continue

		dni=row[COL_DNI].strip()
		if REPORTAR_RAREZAS:
			apes=row[COL_APES].strip()
			noms=row[COL_NOMS].strip()

		if not dni:
			printERR(f'#{LINE_N} Salteando dni vacío')
			continue

		if REPORTAR_RAREZAS:
			if dni.find('E+') != -1:
				dnis_con_e.append({'dni': dni, 'apes': apes, 'noms': noms, 'line': LINE_N})
			elif has_letter.match(dni):
				dnis_con_letras.append({'dni': dni, 'apes': apes, 'noms': noms, 'line': LINE_N})
			if dni.find('-') != -1:
				dnis_con_guion.append({'dni': dni, 'apes': apes, 'noms': noms, 'line': LINE_N})
			if len(dni) == 6:
				dnis_cortos_7.append({'dni': dni, 'apes': apes, 'noms': noms, 'line': LINE_N})
			if len(dni) < 6:
				dnis_cortos_6.append({'dni': dni, 'apes': apes, 'noms': noms, 'line': LINE_N})

		if not dni_regex.match(dni) and not dni == '0000000296/2007':
			printERR(f'#{LINE_N} DNI extraño: {dni}')
			continue

		if dni in dnis:
			#printERR(f'#{LINE_N} DNI duplicado: {dni_original}')
			print(dni)
			continue

		dnis.add(dni)
	#endfor
#end with

if REPORTAR_RAREZAS:
	print(f'\nReportando rarezas (esto se puede deshabilitar desde el código):')
	print(f'\n{len(dnis_con_e)} DNIs con E+:')
	for p in dnis_con_e:
	    print(f'Registro #{p["line"]}: {p["apes"]}, {p["noms"]}, {p["dni"]}')
	print(f'\n{len(dnis_con_letras)} DNIs con letras:')
	for p in dnis_con_letras:
	    print(f'Registro #{p["line"]}: {p["apes"]}, {p["noms"]}, {p["dni"]}')
	print(f'\n{len(dnis_con_guion)} DNIs con guión:')
	for p in dnis_con_guion:
	    print(f'Registro #{p["line"]}: {p["apes"]}, {p["noms"]}, {p["dni"]}')
	print(f'\n{len(dnis_cortos_7)} DNIs con 6 caracteres:')
	for p in dnis_cortos_7:
	    print(f'Registro #{p["line"]}: {p["apes"]}, {p["noms"]}, {p["dni"]}')
	print(f'\n{len(dnis_cortos_6)} DNIs con menos de 6 caracteres:')
	for p in dnis_cortos_6:
	    print(f'Registro #{p["line"]}: {p["apes"]}, {p["noms"]}, {p["dni"]}')
	sys.exit(0)

DUMP_FILE='padron.json'
print(f'Dumping {DUMP_FILE}')
LEN_DNIS=len(dnis)
with open(DUMP_FILE, 'w+') as dump_file:
	DUMPED_DNIS=0
	dump_file.write('[\n')
	for dni in dnis:
		if DUMPED_DNIS == LEN_DNIS-1:
			dump_file.write(f'{{"dni":"{dni}"}}\n')
		else:
			dump_file.write(f'{{"dni":"{dni}"}},\n')
		DUMPED_DNIS+=1
	dump_file.write(']\n')
print(f'Done! {DUMPED_DNIS} dnis')

print()
print('Next:')
print('docker cp padron.json mongocontainer:/')
print('docker exec mongocontainer mongoimport --db dbName --collection collectionName --file padron.json --jsonArray')
print()
print('Example:')
print('docker cp padron.json mongodb-unr-escuelas:/')
print('docker exec mongodb-unr-escuelas mongoimport --db DemocracyOS-dev --collection padron --file padron.json --jsonArray')
