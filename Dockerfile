FROM python:2.7-slim
ADD . /src
ADD resources /src/resources
WORKDIR /src
RUN pip install -r requirements.txt
CMD python ./bot/app.py
