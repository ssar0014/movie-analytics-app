FROM alpine:latest
RUN apk update
RUN apk add py-pip
RUN apk add --no-cache python3-dev 
RUN pip install --upgrade pip

WORKDIR /app

# Set an environment variable
ENV API_TOKEN=${API_TOKEN}
ENV API_URL=${API_URL}

COPY ./api_poller.py .
COPY ./requirements.txt .
COPY ./service.py .

RUN pip --no-cache-dir install -r requirements.txt
EXPOSE 5000

ENTRYPOINT [ "python3" ]
CMD [ "service.py" ]

