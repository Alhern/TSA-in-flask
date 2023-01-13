# TSA in Flask
This is a web application that allows you to analyze the sentiment of a string or a corpus of tweets. 

TSA in Flask is based on my [Twitter Sentiment Analyzer](https://github.com/Alhern/TSA), which uses Gensim's Word2Vec, NLTK, Keras and now Flask. And it now works in Docker. And in Vagrant too. 🐳

## Recommendations
The recommended versions of Docker and Vagrant are:
* ```Docker version 20.10.22, build 3a2c30b```
* ```Vagrant 2.2.6```

The recommended version of VirtualBox used by Vagrant is:
* ```VirtualBox 6.1.38```

This build has been tested on Windows 10 and Ubuntu 20.04 focal.


## Installation
TSA in Flask can be installed in 3 different ways: with Docker ([1](#1--docker)), with Vagrant ([2](#2--vagrant)) or manually ([3](#3--without-docker-or-vagrant)).
### 1) Docker
Use the following command in the project's root directory to build and run the app:

``` docker compose up ```

The app will be available at ```localhost:5001```.

### 2) Vagrant
Use the following command in the project's root directory to build and run the app:

``` vagrant up ```

The app will be available at ```localhost:5001```.

### 3) Without Docker or Vagrant
You will have to change one line (#9) in ```ui_container/app.py``` to be able to run the app manually.

Change ```url = 'http://algo_container:5000'``` to ```url = 'http://localhost:5000'```.

Finally, use the following commands to run the app:

``` 
$ cd algo_container
$ pip3 install -r requirements.txt
$ python3 app.py
$ cd ..
$ pip3 install -r requirements.txt
$ cd ui_container python3 app.py 
```

The app will be available at ```localhost:5001```.

## Usage
The app has 2 main functionalities:
* Predict the sentiment of a string
* Predict the sentiment of a corpus of tweets

### Predict the sentiment of a string
![image](https://res.cloudinary.com/takeout/image/upload/v1673612961/tsa1_dns3jh.png)
![image](https://res.cloudinary.com/takeout/image/upload/v1673613527/res1_eeepks.png)

### Predict the sentiment of a corpus of tweets
![image](https://res.cloudinary.com/takeout/image/upload/v1673613119/tsa2_qkrqya.png)
![image](https://res.cloudinary.com/takeout/image/upload/v1673613525/res2_bgkfus.png)

⚠️ Only .json files can be used, please refer to the [TSA](https://github.com/Alhern/TSA) repository for more information on how to get a valid .json file.