import csv, re

'''
Este archivo tiene la data formateada así:
GUARNIZO CABRERA;JHOAN SEBASTI�N;CI;1006513895;21/02/2000;MASCULINO
REINES URIELES;JUAN SEBASTIAN;CI;1010140098;29/05/2000;MASCULINO
...
'''
FNAME='no duplicados.csv'
COL_DNI=3

def printERR(*msgs):
 print('ERROR:', *msgs)
def printWARN(*msgs):
 print('ALERTA:', *msgs)

dni_regex = re.compile('^[a-zA-Z0-9-]{3,11}$')

dnis = set()

with open(FNAME, 'r', encoding='latin1') as csvfile:
	reader = csv.reader(csvfile, delimiter=';')

	# esto si la primer línea tiene headers
	#next(reader)
	LINE_N=0
	for row in reader:
		LINE_N+=1

		if len(row) < COL_DNI-1:
			printWARN(f'#{LINE_N} Salteando línea vacía o con menos campos')
			continue

		dni=row[COL_DNI].strip()

		if not dni:
			printERR(f'#{LINE_N} Salteando dni vacío')
			continue

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
