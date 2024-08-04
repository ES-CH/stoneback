# Prueba back-end Stone

### Ambiente virtual

Crear un ambiente virtual para este proyecto:

| Linux                       | Windows 10                     | Windows 10 second option |
| --------------------------- | ------------------------------ | ------------------------ |
| `python3 -m virtualenv env` | `python.exe -m virtualenv env` | `py -m virtualenv env`   |

En Caso de que no tengo virtualenv, instarlo con el siguiente comando:

`python3 -m pip install virtualenv` | `python.exe -m pip install virtualenv` | `py -m pip install virtualenv` |

Despues de que la instalacion se halla completado, activar el ambiente virtual:

| Linux                     | Windows 10               |
| ------------------------- | ------------------------ |
| `source env/bin/activate` | `.\env\Scripts\activate` |


### Bade de datos

Crear una base de datos, el nombre tiene que coinsidir con la configuracion del settings.

### Dependencias

Descargar las dependenciasd del proyecto usando pip

`python -m pip install -r requirements.txt`

### Server configuration

Despues de instalar las dependencias, ejecutar los siguientes comandos para iniciar la base de datos y crear el super usuario:

`python manage.py migrate`

`python manage.py createsuperuser`

El proyecto cuenta con roles predefinidos y permisos para pruebas, estos se pudene encontrar en el archivo initial_groups.yaml
ubicado en el directorio custom_auth/fixtures.
Para cagarlos usar el siguiente comando:
`python manage.py loadperms`