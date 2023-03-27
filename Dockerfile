FROM python:3.10-slim

EXPOSE 80

WORKDIR /home

COPY . /home

RUN pip install --no-cache-dir --upgrade -r requirements.txt


#CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
CMD ["tail", "-f", "/dev/null"]