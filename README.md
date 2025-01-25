# CMX Capstone Rest API

## Contributors
- William Morris [morriswa] morris.william@ku.edu
- Kevin Rivers [Kabuto1357] kevin.rivers14832@ku.edu


## Project Setup Guide
- Install python 3.12 https://www.python.org/downloads/
- Open project root directory in terminal
- Install Project environment

      python3.12 -m venv .
- Activate Project environment
    - Mac/Linux

          source bin/activate
        - NOTE: to deactivate project environment

              deactivate
        - NOTE: to reset project environment 

              rm -rf bin include lib pyvenv.cfg
    - Windows Powershell

          .\Scripts\activate
        - NOTE: to deactivate project environment

              .\Scripts\deactivate.bat
        - NOTE: to reset project environment 

              rm -r include
              rm -r lib 
              rm -r scripts
              rm -r pyvenv.cfg
- Install project in development mode and dependencies with PIP 

      pip install -e .
- Create local app environment file 'secrets.properties' in project root directory
- And include following line in file.

      SECRET_KEY=enter_random_string_here
- Open Postgres Admin app (PgAdmin4, Beekeeper, Postgres Desktop, etc)
- Open console to root database (usually 'postgres') 
as root user (usually 'postgres') and input...

      create role cmx_capstone_app_admin_role with login password 'password';
      create database cmx_capstone_app;
      grant create on database cmx_capstone_app to cmx_capstone_app_admin_role;
- Close console
- Open new console to new database 'cmx_capstone_app'
as root user (usually 'postgres') and input...

      grant create on schema public to cmx_capstone_app_admin_role;
- Close Postgres Admin app and return to cmx-capstone-rest project
- Create database tables/sequences/etc with Django

      python manage.py migrate
- Run on local machine http://localhost:8000
       
      python manage.py runserver



## Test Setup Guide
- Open Postgres Admin app (PgAdmin4, Beekeeper, Postgres Desktop, etc)
- Open console to root database (usually 'postgres') 
as root user (usually 'postgres') and input...

      create role testuser with createdb login password 'testpassword';
- Close Postgres Admin app and return to cmx-capstone-rest project
- Run test script
      
      python test.py
- Install coverage library

      pip install coverage
- Run test script with coverage
      
      coverage run test.py
      coverage report -m



## Django Migrate Guide
please note all database scripts are located in src/core/migrations 
and all sql commands are stored in src/*/daos.py 

- Reset app database

      python manage.py migrate core zero
- Migrate app database to specific version 
  (replace xxxx with migration code eg 0001, 0002, etc) 

      python manage.py migrate core xxxx

- Migrate app database to latest version

      python manage.py migrate 
