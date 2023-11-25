FROM python:3.10.5

RUN mkdir /order_status_management

WORKDIR /order_status_management

copy requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x app.sh
