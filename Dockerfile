FROM python:3.8

LABEL maintainer="Farbod Ahmadian farbodahmadian2014@gmail.com"

EXPOSE 5000

WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "api:app"]
