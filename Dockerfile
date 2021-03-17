FROM python:3.6.9

WORKDIR /code
COPY requirements.txt .
RUN pip install pip --upgrade
RUN pip install -r requirements.txt
COPY . .
WORKDIR /code/foodgram
CMD /code/foodgram/gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000