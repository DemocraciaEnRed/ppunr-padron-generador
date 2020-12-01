import csv, re

'''
Este archivo tiene la data formateada así:
"Aguilar Saliva, Luz Zahira",DNI 43005756
"Aimino, Celeste",DNI 42609108
...
'''
FNAME='Agregado Padrón Graduadxs Poli PP.csv'
ESCUELA_OBJECT_ID='ObjectId("5ee395856d49d83d65eab64c")'
COL_DNI=1

def printERR(*msgs):
 print('ERROR:', *msgs)
def printWARN(*msgs):
 print('ALERTA:', *msgs)

dni_regex = re.compile('^([A-Z]{2}[0-9]{7}|[0-9]{7,9})$')

dnis = set()

with open(FNAME, 'r') as csvfile:
	reader = csv.reader(csvfile)

	# esto si la primer línea tiene headers
	next(reader)
	LINE_N=0
	for row in reader:
		LINE_N+=1

		if len(row) < COL_DNI-1:
			printWARN(f'#{LINE_N} Salteando línea vacía o con menos campos')
			continue

		dni=row[COL_DNI].replace('.','').replace('DNI','').replace('PAS','').strip()

		if not dni:
			printERR(f'#{LINE_N} Salteando dni vacío')
			continue

		if not dni_regex.match(dni):
			printERR(f'#{LINE_N} DNI extraño: {dni}')
			continue

		if dni in dnis:
			printERR(f'#{LINE_N} DNI duplicado: {dni}')
			continue

		dnis.add(dni)
	#endfor
#end with


print('Dumping json')
LEN_DNIS=len(dnis)
with open('padron.json', 'w+') as dump_file:
	DUMPED_DNIS=0
	dump_file.write('[\n')
	for dni in dnis:
		if DUMPED_DNIS == LEN_DNIS-1:
			dump_file.write(f'{{"dni":"{dni}","escuelas":[{ESCUELA_OBJECT_ID}]}}\n')
		else:
			dump_file.write(f'{{"dni":"{dni}","escuelas":[{ESCUELA_OBJECT_ID}]}},\n')
		DUMPED_DNIS+=1
	dump_file.write(']\n')
print('Done!')

print()
print('Next:')
print('docker cp padron.json mongocontainer:/')
print('docker exec mongocontainer mongoimport --db dbName --collection collectionName --file padron.json --jsonArray')
print()
print('Example:')
print('docker cp padron.json mongodb-unr-escuelas:/')
print('docker exec mongodb-unr-escuelas mongoimport --db DemocracyOS-dev --collection padron --file padron.json --jsonArray')
