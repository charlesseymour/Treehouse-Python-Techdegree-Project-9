# Treehouse-Python-Techdegree-Project-9

# Description

Students were given a Django project to improve.  

# Installation

--Download files.
--In the project directory install virtual environment:  
    python -m venv p9venv
--Activate virtual environment:
    p9venv\Scripts\activate.bat
--Install requirements:
    pip install -r .\requirements.txt
--Run migrations:
    python manage.py migrate

# Testing

--Run tests using coverage.py:
    coverage run --source='.' manage.py test myapp
--Run report:
    coverage report -m
    
 
