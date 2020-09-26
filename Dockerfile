FROM python:3.7
RUN pip install pipenv
WORKDIR /code
COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv && pipenv install --system
COPY . /code/
CMD flask run 
