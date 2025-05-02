#### DENANDA HENDRA PRATAMA

#### denanda.hendra.p@mail.ugm.ac.id

#### How to run locally:

##### 1. Install dependencies

1. clone the repository.

   ```
   https://github.com/rinofazar/drowsiness_detection-dashboard.git/
   ```
2. Create a [python virtual environment and activate it](https://docs.python.org/3/library/venv.html)
3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```
4. Migrate the app to create database table advertisements and publisher

   ```
   python .\manage.py migrate publishers
   python .\manage.py migrate advertisements  
   ```
5. Migrate the app to create view table from unmanaged model DenormalizedAdvertisement

   ```
   python .\manage.py migrate advertisement_views
   ```

##### 2. Launch the apps

1. Run the server locally

   ```
   python manage.py runserver
   ```
2. After the apps running is succesfully, we can start by calling routes. For example :

   ```
   http://127.0.0.1:8000/
   ```
