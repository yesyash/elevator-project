# elevator-project
Business logic for simplified elevator model in python

## Setup
### 1. Prerequisites
- conda 
- postgresql (to quickly setup a could instance you can use [railway.app](https://www.railway.app))

### 2. Virtual environment
1. To create a virtual environment using python 3.10.0 type:
```
conda create -n elevator python=3.10.0
```

2. When conda asks you to proceed, type y:
```
proceed ([y]/n)?
```

3. Activate your virtual environment by typing:
```
conda activate elevator
```

### 3. Packages
once you have have your virtual environment setup it's time to install the required packages. 

1. Copy & paste the following in your terminal:
```
  pip install django djangorestframework psycopg2-binary
```

2. Enter `conda list` in your terminal, you should see packages from above in the list, else repeat the above step.

### 4. Postgres
As we are using postgres to store our data it is necessary to change the default `sqlite` database that django provides.
1. Go to `elevator/settings.py` file and enter your postgres db credentials:

#### 4.1 Before
 ```
  DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
} 
``` 
#### 4.2 After
Replace the detail below with your db credentials:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
} 
```
Read more about databases [here.](https://docs.djangoproject.com/en/4.0/ref/settings/#databases)

## Running the app
To run your django application enter the following in your terminal
```
python manage.py runserver
```

🎉 Congratulations your application is ready 🎉


## API List
- GET- **/requests** (Gets all pending requests)
- POST- **/requests** (Creates a request)
- GET - **/destination?elevator_id=2** (Gets destination of the elevator if travelling else null)
- POST - **/init** (Initializes the elevator system)
