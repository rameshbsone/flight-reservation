FROM python:3.8-slim-buster

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get clean

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . /backend
ENTRYPOINT ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port"]CMD ["port"]
