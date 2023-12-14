Steps To execute this application

1. Clone this Repository or Download the zip file from this url: https://github.com/Chiranjit32/fatmug
2. From APP directory, 
        Execute command for creating virtual environment(env): python -m venv env
        Execute command for activating virtual environment(env): .\env\Scripts\activate
        Execute command for installing necessary packanges: pip install -r requirements.txt
3. Configure .env file in the directory: fatmug/.env
4. To make migrations, Execute command: python manage.py makemigrations
5. To create and alter the tables in the DB, Execute command: python manage.py migrate
6. To create the superuser, Execute command: python manage.py createsuperuser
        Fill up the neccessary informations
7. To run the application, execute the command: python manage.py runserver