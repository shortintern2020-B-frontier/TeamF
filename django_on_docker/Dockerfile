FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/

RUN pip install --upgrade pip \
&& pip install -r requirements.txt

COPY . /code/

RUN useradd -m myuser
USER myuser

CMD exec gunicorn -b 0.0.0.0:$PORT main.wsgi
