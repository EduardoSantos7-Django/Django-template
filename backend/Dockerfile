# syntax=docker/dockerfile:1
FROM python:3
# set work directory
WORKDIR /usr/src/backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# Command
CMD ["gunicorn", "--bind", ":8000", "admin.wsgi:application"]