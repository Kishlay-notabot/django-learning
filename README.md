# django-learning

## commands:
* `django-admin startproject mysite`  
starts the project and initial files  

* `python manage.py runserver`  
    run the development server  

* `python manage.py startapp polls`  
creates an app named polls  

* `python manage.py shell`  
django interactive shell

* `python manage.py migrate`  
    initial db file

* `python manage.py makemigrations polls`  
save migrations for the polls app, [run after including polls in the INSTALLED_APPS setting.]  

* `python manage.py sqlmigrate polls 0001`  
shows the sql commands which will we run in a particular migration script [here it is 0001_initial.py]

* `python manage.py migrate`  
apply migration  

* `python manage.py createsuperuser`  
create an admin user  

* `python manage.py test polls`  
run test file for a django app [here: polls]  

* `python manage.py createsuperuser`  
create admin account  


ref: https://docs.djangoproject.com/en/1.8/intro/tutorial02/
