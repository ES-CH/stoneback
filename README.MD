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

### Solucion propuesta

Para dar solucion a el problema del sistema de seguridad implemente un sistema de autenticacion por token usando jwt donde estara almacenado los permisos y roles
asignados a cada usuario al momento de hacer login, al momento de hacer una peticion a algun modulo la vista de ese modulo valida si tiene el rol o el permiso configurado para cada modulo configurado de esta manera se garantiza primero que solo usuarios autenticados tengan acceso a los modulos y solo los usuarios
que cuenten con permisos especificados podran interactuar.


### Serivios expuestos para pruebas

PARA PROBAR CADA SERVICIO SE RECOMIENDA USAR POSTMAN O Insomnia

Crear usuario:

URL: http://localhost:8000/auth/users

    {
        "email":"stone@gmail.com",
        "password":"stonepassword"
    }


Obtener token / Verificar permissos y roles asignados

URL: http://localhost:8000/auth/token/

    {
        "username":"stone@gmail.com",
        "password":"stonepassword"
    }


Asignar roles 

URL: http://localhost:8000/auth/users/id_usuario/assign-role


    {        
        "roles": ["counter"]
    }
    
Asignar permisos

URL: http://localhost:8000/auth/users/id_usuario/assign-permission

    {
        "permissions":[
            {
                "model":"user",
                "action": ["view", "add"]
            }
            
        ]
    }

Crear roles

URL: http://localhost:8000/auth/users/create-role

    {
        "name": "prueba",
        "permissions": [
            {
                "model": "employee",
                "action": ["view", "add", "change", "delete"]
            }
        ]
    }