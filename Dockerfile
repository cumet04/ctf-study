FROM python

RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
ADD . /app/
CMD ["python", "main.py", "--host", "0.0.0.0"]
