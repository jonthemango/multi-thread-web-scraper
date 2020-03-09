FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
CMD gunicorn --log-level=info --workers=4 -b 0.0.0.0:5000 main