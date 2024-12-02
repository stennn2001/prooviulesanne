# Project Installation Guide

## Quick Installation Guide

Follow the steps below to set up and run the project on **Windows**.

### Requirements

- Python installed on your system.
- Django installed via `requirements.txt`.
- **Database** : Refer to `database.schema.png` for the database structure.

### Installation Steps

Git clone and then navigate to root folder where 'manage.py' exists.

1. **Create and activate a virtual environment**:

```
python -m venv venv
```

```
venv\Scripts\activate 
```

2. **Install required dependencies**:

```
pip install -r requirements.txt
```

3. **Run migrations (to create database tables)**:

```
python manage.py makemigrations
```

```
python manage.py migrate
```

4. **Load database from JSON**:
   After successful migrations, execute the following command to load initial data into the database:

```
python manage.py load_database_from_json
```

5. ****Start the server****:
   To start the server, run:

```
python manage.py runserver
```

6. **Access the admin page**:
   To access the Django admin interface, go to `/admin` in your browser. The default username and password are (if you loaded the data from JSON):

- **Username**: `admin`
- **Password**: `admin`

  Or to create a new admin user, run the following command:

```
python manage.py createsuperuser
```
