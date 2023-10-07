# AppMO

AppMO is a Django-based web application that allows users to query information through an API and request an API key for authentication.

## Prerequisites
- Python 3.8 or higher
- Docker (if you want to run the application in a container)

## Installation and Configuration

1. Clone this repository on your local machine:


   git clone https://github.com/camiloquinteror92/appMO.git


2. Navigate to the project directory:


   cd appMO


3. Create and activate a virtual environment (optional but recommended):

   python -m venv myenv
   source myenv/bin/activate # On Windows, use 'myenv\Scripts\activate'


4. Install project dependencies:


   pip install -r requirements.txt


5. Create a copy of the example configuration file:


   cp .env.example .env


6. Open the `.env` file in a text editor and configure the necessary environment variables, such as database settings and secret keys.

7. Apply database migrations:

   python manage.py migrate


8. Create a superuser account to access the admin panel (optional):


   python manage.py createsuperuser


## Execution

You can run the application locally or within a Docker container.

### Local Execution

To run the application locally, use the following command:


python manage.py runserver

The application will be available at [http://localhost:8000/](http://localhost:8000/).

### Docker Execution

If you prefer to run the application in a Docker container, ensure you have Docker installed on your machine. Then, run the following command:


docker-compose up -d


The application will be available at [http://localhost:8000/](http://localhost:8000/).

## Usage

- Access the admin panel at [http://localhost:8000/admin/](http://localhost:8000/admin/) (or the corresponding URL) using the credentials of the superuser you created.

- Users can register in the application and request an API key for authentication to access the API.

- Check the API documentation at [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/) to learn about available endpoints and how to use them.

## Contribution

If you wish to contribute to this project, follow these steps:

1. Create a fork of the repository.
2. Clone your fork to your local machine.
3. Create a branch for your feature or bug fix: `git checkout -b my-feature`.
4. Make your changes and commit them.
5. Push your changes to your fork on GitHub: `git push origin my-feature`.
6. Create a Pull Request in the main repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


