
# AppMO

AppMO es una aplicación web basada en Django que permite a los usuarios consultar información a través de una API y solicitar una clave de API para autenticarse.

## Requisitos previos
- Python 3.8 o superior
- Docker (si deseas ejecutar la aplicación en un contenedor)

## Instalación y configuración

1. Clona este repositorio en tu máquina local:

   ```bash
   git clone https://github.com/tuusuario/appMO.git
   ```

2. Entra al directorio del proyecto:

   ```bash
   cd appMO
   ```

3. Crea y activa un entorno virtual (opcional pero recomendado):

   ```bash
   python -m venv myenv
   source myenv/bin/activate  # En Windows, usa 'myenv\Scripts\activate'
   ```

4. Instala las dependencias del proyecto:

   ```bash
   pip install -r requirements.txt
   ```

5. Crea una copia del archivo de configuración de ejemplo:

   ```bash
   cp .env.example .env
   ```

6. Abre el archivo `.env` en un editor de texto y configura las variables de entorno necesarias, como la configuración de la base de datos y las claves secretas.

7. Aplica las migraciones de la base de datos:

   ```bash
   python manage.py migrate
   ```

8. Crea un superusuario para acceder al panel de administración (opcional):

   ```bash
   python manage.py createsuperuser
   ```

## Ejecución

Puedes ejecutar la aplicación de forma local o dentro de un contenedor Docker.

### Ejecución local

Para ejecutar la aplicación localmente, usa el siguiente comando:

```bash
python manage.py runserver
```

La aplicación estará disponible en [http://localhost:8000/](http://localhost:8000/).

### Ejecución con Docker

Si prefieres ejecutar la aplicación en un contenedor Docker, asegúrate de tener Docker instalado en tu máquina. Luego, ejecuta el siguiente comando:

```bash
docker-compose up -d
```

La aplicación estará disponible en [http://localhost:8000/](http://localhost:8000/).

## Uso

- Accede al panel de administración en [http://localhost:8000/admin/](http://localhost:8000/admin/) (o la URL correspondiente) con las credenciales del superusuario que creaste.

- Los usuarios pueden registrarse en la aplicación y solicitar una clave de API para autenticarse y acceder a la API.

- Consulta la documentación de la API en [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/) para conocer los endpoints disponibles y cómo usarlos.



