FROM python:3.11.1-alpine

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY . .

EXPOSE 8000

# ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.6.0/wait /wait
# RUN chmod +x /wait

# RUN python manage.py makemigrations
RUN python manage.py migrate
# CMD python manage.py runserver
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]