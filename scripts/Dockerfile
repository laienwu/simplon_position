FROM python:latest-slim

RUN pip install requests
WORKDIR /app

COPY db_schema.sql /app/db_schema.sql
RUN mkdir /db

COPY analyse_script.py /app/analyse_script.py
CMD ["python", "analyse_script.py"]