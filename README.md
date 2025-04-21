# Implementation of a Customer Service Chatbot.  
ChatBot built in two parts. 
A simple chatbot implementation with PyTorch for simple and quick responses. 
A LLM reader to transform natural language into the required fields

- The implementation is straightforward with a Feed Forward Neural net with 2 hidden layers.
- Customization is super easy. Just modify `intents.json` with possible patterns and responses and re-run the training (see below for more info).
- The factor to call this part of the bot is 98%

A free LLM model from open router is ready for requested information.
A paid model like openai o claude can be used, or a llama agent can be downloaded to local use.
For Test Challange, this model is being used and it has 50 uses each day.
[model="agentica-org/deepcoder-14b-preview:free"](https://openrouter.ai/nvidia/llama-3.3-nemotron-super-49b-v1:free/api)

api token can be created free here.
https://openrouter.ai/settings/keys

for this practice, I will provide a token that will be deleted later.

## Installation

### Create an environment
Whatever you prefer (e.g. `conda` or `venv`)
```console
mkdir chatbot
$ cd chatbot
clone or download github code
$ python3 -m venv venv

### Activate it
Mac / Linux:
. venv/bin/activate
Windows:
venv\Scripts\activate
```
### Install dependencies


 ```console
  pip install -r /path/to/requirements.txt

 ```
(if you are not using docker)
You also need `nltk`:
Run this once in your terminal:
 ```console
  $ python
  >>> import nltk
  >>> nltk.download('punkt')
```
### Run Testings 
The test were created using TDD technique

```console
python test.py
```

## Before
if train.py has been changed, Run
```console
python train.py
```
This will dump `data.pth` file. And then run


## Docker 

Have docker installed on the computer.

```console
docker-compose up --build
```
flask Application will be opened for the conversation with the url 
localhost:5000

## Customization
Have a look at [intents.json](intents.json). 
There is tag defined with possible `patterns`, and possible `responses` for the chat bot. 
You have to re-run the training whenever this file is modified.


## Pipeline

User:
Bot:
User:
Bot:
User:
Bot:


## Deployment on google cloud platform

wwha