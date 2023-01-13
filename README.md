# TSA in Flask
This is a web application that allows you to analyze the sentiment of a string or a corpus of tweets. 

TSA in Flask is based on my [Twitter Sentiment Analyzer](https://github.com/Alhern/TSA), which uses Gensim's Word2Vec, NLTK, Keras and now Flask. And it now works in Docker. And in Vagrant too. 🐳

### Table of Contents
- [Recommendations](#recommendations)
- [Installation](#installation):
  - [Docker](#1-docker)
  - [Vagrant](#2-vagrant)
  - [Without Docker or Vagrant](#3-without-docker-or-vagrant)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)

## Recommendations
The recommended versions of Docker and Vagrant are:
* ```Docker version 20.10.22, build 3a2c30b```
* ```Vagrant 2.2.6```

The recommended version of VirtualBox used by Vagrant is:
* ```VirtualBox 6.1.38```

This build has been tested on Windows 10 and Ubuntu 20.04 focal.


## Installation
TSA in Flask can be installed in 3 different ways: with Docker ([1](#1-docker)), with Vagrant ([2](#2-vagrant)) or manually ([3](#3-without-docker-or-vagrant)).
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

## Troubleshooting
You might encounter some issues with Vagrant, for example:
### VT-x is disabled
```
There was an error while executing `VBoxManage`, a CLI used by Vagrant
for controlling VirtualBox. The command and stderr is shown below.

Command: ["startvm", "a5467e19-ec3d-4e50-96c3-65216be1a90a", "--type", "headless"]

Stderr: VBoxManage: error: VT-x is disabled in the BIOS for all CPU modes (VERR_VMX_MSR_ALL_VMX_DISABLED)
VBoxManage: error: Details: code NS_ERROR_FAILURE (0x80004005), component ConsoleWrap, interface IConsole
```

To fix this, you will have to enable virtualization (VT-x) in your BIOS.
To do so, restart your computer and press the key to enter the BIOS. 
Then, go to the "Advanced" tab and enable virtualization (VT-x). Save and exit and you should be good to go.

### Using WSL2
If you use WSL2 in Windows to run Vagrant and VirtualBox you might encounter issues. This can be due to Hyper-V on the host and tensorflow (1.14) requiring AVX and AVX2 instructions, it's therefore not recommended to use a virtual machine to run another virtual machine!
