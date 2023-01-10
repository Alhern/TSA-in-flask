FROM python:3.6-slim
LABEL maintainer="Alhern"

WORKDIR /app

# copy all files from local directory to the container
COPY . .
ADD algo_container/model_config.json /app/model_config.json
ADD algo_container/model_weights.h5 /app/model_weights.h5
ADD algo_container/my_w2vmodel /app/my_w2vmodel
ADD algo_container/tfidf.pickle /app/tfidf.pickle

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV PYTHONPATH "${PYTHONPATH}:/app"

# install dependencies
RUN apt-get update -y && apt-get upgrade -y && pip install --upgrade pip && pip install -r algo_container/requirements.txt

ENTRYPOINT ["python3"]

EXPOSE 5000
# execute the command
CMD ["algo_container/app.py"]