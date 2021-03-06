Scripts de python que toman distintos padrones ubicados en la misma carpeta del proyecto como archivos csv y generan un archivo json para subir a una base de datos MongoDB.

Se deben ubicar los padrones como archivos csv en la misma carpeta que los scripts. En el archivo `padron_parser.py` figuran los índices de las columnas de estos archivos (todos deben tener las mismas columnas en el mismo orden).

Para generar el json:
- Modificar los ids de `escuelas` en `padron_dumper.py`
- Si hace falta modificar los nombres de archivos también en el mismo archivo
- Ejecutar `python3 padron_dumper.py`
- Subir el `padron.json` generado a la base de datos

Si se desean cambiar los caracteres admitidos o los mensajes de aviso o error ver `padron_parser.py`.

### Importación

Para importarlo desde la shell del server hacer:

`mongoimport --host localhost:27032 --db BASE_DE_DATOS --collection padron --file ARCHIVO_DUMP.json --jsonArray`

Para importarlo a un docker local:
```
docker cp ARCHIVO_DUMP.json MONGO_CONTAINER:/
docker exec MONGO_CONTAINER:/ mongoimport --db DemocracyOS-dev --collection padron --file ARCHIVO_DUMP.json --jsonArray
```
