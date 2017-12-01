# Treehouse-Python-Techdegree-Project-9

# Description

Students were given a Django project to improve.</p>  

# Python

Version 3.6.0 

# Installing

- Download files.
- In the project directory install virtual environment: `python -m venv p9venv`
- Activate virtual environment: in Windows `p9venv\Scripts\activate` or Posix `source p9venv/bin/activate`
- Install requirements: `pip install -requirements.txt`
- Run migrations: `python manage.py migrate`
- Create superuser: `python manage.py createsuperuser`

# Running

- Start server: `python manage.py runserver 0.0.0.0:8000`
- Login as admin at `http://0.0.0.0:8000/admin`
- Go to home page at `http://0.0.0.0:8000`
    
# Testing

- Run tests using coverage.py: `coverage run --source='.' manage.py test menu`
- Generate report: `coverage report -m`
    
 
