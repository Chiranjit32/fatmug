Steps To execute this application

1. Clone this Repository or Download the zip file from this url: https://github.com/Chiranjit32/fatmug
2. From APP directory, 
3. Execute command for creating virtual environment(env): python -m venv env
4. Execute command for activating virtual environment(env): .\env\Scripts\activate
5. Execute command for installing necessary packanges: pip install -r requirements.txt
6. Configure .env file in the directory: fatmug/.env
7. To make migrations, Execute command: python manage.py makemigrations
8. To create and alter the tables in the DB, Execute command: python manage.py migrate
9. To create the superuser, Execute command: python manage.py createsuperuser
10. Fill up the neccessary informations
11. To run the application, execute the command: python manage.py runserver