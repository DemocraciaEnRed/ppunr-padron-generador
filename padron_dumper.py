from padron_parser import get_padron

files = [
	'PPUNR _ PADRÓN POLITÉCNICO - Docentes.csv',
	'PPUNR_ PADRÓN SUPERIOR DE COMERCIO.xlsx - Docentes.csv',
	'PPUNR_ PADRÓN AGROTÉCNICA.xlsx - Padrón Graduados.csv'
]

#escuelas = [ 'POLITÉCNICO', 'COMERCIO', 'AGROTÉCNICA' ]
escuelas = [ 'ObjectId("5ee3a85bf8d07d447577fd84")', 'ObjectId("5ee3a85bf8d07d447577fd85")', 'ObjectId("5ee3a85bf8d07d447577fd86")' ]

padrones = []

for f in files:
	print(f'------ Getting padrón {f}')
	padrones.append(get_padron(f))

padron_general = {}

for i, padron in enumerate(padrones):
	escuela = escuelas[i]
	for dni, data in padron.items():
		if dni not in padron_general:
			padron_general[dni] = { 'escuelas': [escuela] }
		else:
			padron_general[dni]['escuelas'].append(escuela)

print('Dumping json')
with open('padron.json', 'w+') as dump_file:
	dump_file.write('[\n')
	for dni, data in padron_general.items():
		escuelas=data['escuelas']
		dump_file.write(f'{{"dni":"{dni}","escuelas":[{",".join(escuelas)}]}},\n')
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
