
# AppMO - Aplicación de Gestión de Préstamos y Pagos

## Descripción

AppMO es una aplicación web basada en Django diseñada para la gestión eficiente de préstamos y pagos. Esta aplicación permite a los usuarios llevar un registro detallado de clientes, realizar un seguimiento de préstamos pendientes y registrar los pagos asociados a estos préstamos. Además, proporciona un panel de control que ofrece información general sobre la actividad del sistema.

## Características Destacadas

- **Gestión de Clientes**: Registra y administra información de clientes, incluyendo nombre, apellido, correo electrónico, fecha de nacimiento y más. Se incluyen validaciones para garantizar la mayoría de edad.
- **Gestión de Préstamos**: Crea y gestiona préstamos asociados a clientes específicos. El sistema realiza validaciones para asegurarse de que los préstamos cumplen con ciertos criterios.
- **Gestión de Pagos**: Registra pagos hacia préstamos específicos y asocia detalles de pago. Se realizan validaciones para garantizar la integridad de los datos.
- **Panel de Control**: Ofrece una vista general del sistema, incluyendo estadísticas clave, resumen de clientes, préstamos y pagos recientes.
- **API RESTful**: Todos los datos y funcionalidades están disponibles a través de una API RESTful que facilita la integración con otras aplicaciones.

## Requisitos Previos

Para ejecutar AppMO en tu entorno, asegúrate de tener instalados los siguientes requisitos:

- Python 3.8 o superior.
- Docker y Docker Compose.

## Instalación y Configuración

Sigue estos pasos para instalar y configurar AppMO en tu sistema:

1. Clona este repositorio en tu máquina local:
```
git clone https://github.com/tuusuario/appMO.git
cd appMO
```
2. Crea una copia del archivo de configuración de ejemplo:
```
cp .env.example .env
```
3. Abre el archivo `.env` en un editor de texto y configura las variables de entorno necesarias, como la configuración de la base de datos y las claves secretas.

## Ejecución con Docker

Utiliza Docker y Docker Compose para ejecutar la aplicación en contenedores. Sigue estos pasos:

1. Construye y levanta los contenedores:
```
docker-compose up --build -d
```
2. Crea un superusuario para acceder al panel de administración y autenticarte en la API:
```
docker-compose exec web python manage.py createsuperuser
```
Sigue las instrucciones en la terminal para configurar el nombre de usuario, correo electrónico y contraseña del superusuario.

## Uso

### Panel de Administración

Accede al panel de administración en [http://localhost:8000/admin/](http://localhost:8000/admin/) con las credenciales del superusuario que creaste. Aquí podrás gestionar clientes, préstamos y pagos, y obtener una visión general de la aplicación.

### Registro de Usuarios

Los usuarios pueden registrarse en la aplicación y solicitar una clave de API para autenticarse y acceder a la API.

### Documentación de la API

Consulta la documentación de la API en [http://localhost:8000/swagger/](http://localhost:8000/swagger/) o [http://localhost:8000/swagger/redoc/](http://localhost:8000/swagger/redoc/) para conocer los endpoints disponibles y cómo usarlos.

## Detalles Técnicos

### Configuración (`settings.py`)

- La aplicación utiliza el paquete `rest_framework` para construir la API RESTful, lo que significa que las interacciones con los endpoints se manejarán en un formato estándar de API REST.
- Se utiliza el paquete `django_filters` para admitir filtrado avanzado en algunas vistas.
- La autenticación se maneja a través de tokens, lo que significa que los usuarios necesitarán un token para acceder a ciertas partes de la API.

### Modelos (`models.py`)

- Los modelos `Customer`, `Loan`, `Payment` y `PaymentDetail` representan la estructura fundamental de la aplicación.
- Se implementan señales (`signals.py`) que garantizan la actualización adecuada del monto pendiente de un préstamo cuando se realiza un pago.

### Serializadores (`serializers.py`)

Los serializadores convierten los modelos en un formato JSON adecuado para la API. También incluyen lógica adicional para validar datos, como la verificación de la mayoría de edad de los clientes antes de registrarlos.
```
