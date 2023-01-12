FROM python:3.6-slim
LABEL maintainer="Alhern"

WORKDIR /app

# copy all files from local directory to the container
COPY . .

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV PYTHONPATH "${PYTHONPATH}:/app"

# install dependencies
RUN apt-get update -y && apt-get upgrade -y && pip install --upgrade pip && pip install -r ui_container/requirements.txt

ENTRYPOINT ["python3"]

EXPOSE 5001
# execute the command
CMD ["ui_container/app.py"]