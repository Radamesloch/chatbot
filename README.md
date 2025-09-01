

# Implementation of a Customer Service Chatbot.  
ChatBot built in two parts. 
A simple chatbot implementation with PyTorch for simple and quick responses. 
A LLM reader to transform natural language into the required fields

- The implementation is straightforward with a Feed Forward Neural net with 2 hidden layers.
- Customization is super easy. Just modify `intents.json` with possible patterns and responses and re-run the training.

A free LLM model from open router is ready for requested information.
A paid model like openai, claude can be used, or a llama agent can be downloaded to local use.
For Test Challange, this model is being used and it has 50 uses each day.
```
[model="agentica-org/deepcoder-14b-preview:free"](https://openrouter.ai/nvidia/llama-3.3-nemotron-super-49b-v1:free/api)
```

api token can be created free in here.
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
```

### Activate it

```
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
You may also need `nltk`:
Run this once in your terminal:

 ```console
  $ python
  >>> import nltk
  >>> nltk.download('punkt')
```

### Run Testings 
The test were created using TDD technique, and they are automated by github actions.

```console
python test.py
```

## Before starting
if train.py has been changed, Run
```console
python train.py
```

This will dump `data.pth` file. And then run


## Docker and docker-compose installation

Have docker installed on the computer.

```console
docker-compose up --build
```
Flask Application will be opened for the bot conversation with the url 
localhost:5000

## Database

A redis server is running on a docker container and it can be used to store user information for the session.Set to max 1 hour.
(no crud implemented on the code yet)


## Pipeline

Greeting, thanks, and goodbye have self trained bot answers.
```
User:I want to buy an office with 200m2 for 200.000 USD in NYC, with 2 parking slots.
Bot:I got it! I will look for an available space with the following information:<br> budget: 200.000<br> size: 200<br> type: buy<br> city: NYC<br> purpose: office, parking slot: 2.
```

## Deployment on Google Cloud Platform

1) Go to GCP and access "service accounts" section.
2) Create service account.
3) Add name "githubaction", click create and continue.
4) Give roles: Cloud Run admin; Artifact Registry administrator; Service Account User
5) Enter on the service account created and click on key tab.
6) Add Key and Create a new one with json type. Download Key.

////GitHub secret
1) On GitHub repo, open settings.
2) Open secrets and variables. Open actions.
3) Create new repository secret.
4) Give a name "GCP_CREDENTIALS" and copy service account key json. 

////artifact registry
1) Go to Artifact Registry
2) Create Repository
3) Add Name, Region us-central1,

////Workflow to  automate  deployment for the website and chatbot


'''
name: Build and Deploy Chatbot to Cloud Run
on:
  push:
    branches:
     [ "main" ]

env:
  PROJECT_ID: <PROJECT_ID> # TODO: update to your Google Cloud project ID
  GAR_NAME: <NAME>
  GAR_LOCATION: us-central1
  SERVICE: <SERVICE_NAME> # TODO: update to your service name
  REGION: us-central1 # TODO: update to your region
jobs:
  deploy:    
    permissions:
      contents: 'read'
      id-token: 'write'

    runs-on: ubuntu-latest


    steps:
      - name: Checkout
        uses: actions/checkout@v2 # actions/checkout@v4
              
      - name: Google Auth
        id: auth
        uses: google-github-actions/auth@v2 # google-github-actions/auth@v2 ==> google-github-actions/auth@v2
        with:
          credentials_json: '${{ secrets.GCP_CREDENTIALS }}'

      # BEGIN - Docker auth and build
      #
      # If you already have a container image, you can omit these steps.
      - name: Docker Auth
        run: |-
          gcloud auth configure-docker "${{ env.GAR_LOCATION}}-docker.pkg.dev"

      - name: 'Build and Push Container'
        run: |- 
          docker build -t "${{ env.GAR_LOCATION }}-docker.pkg.dev/${{ env.PROJECT_ID }}/${{ env.GAR_NAME }}/${{ env.SERVICE }}:${{ github.sha }}" ./
          docker push "${{ env.GAR_LOCATION }}-docker.pkg.dev/${{ env.PROJECT_ID }}/${{ env.GAR_NAME }}/${{ env.SERVICE }}:${{ github.sha }}"

      - name: 'Deploy to Cloud Run'
        id: deploy  
        # END - Docker auth and build

        uses: google-github-actions/deploy-cloudrun@v2 # google-github-actions/deploy-cloudrun@v2
        with:
          service: ${{ env.SERVICE }}
          region: ${{ env.REGION }}
          # NOTE: If using a pre-built image, update the image name below:

          image: "${{ env.GAR_LOCATION }}-docker.pkg.dev/${{ env.PROJECT_ID }}/${{ env.GAR_NAME }}/${{ env.SERVICE }}:${{ github.sha }}"
      # If required, use the Cloud Run URL output in later steps
      - name: Show output
        run: |2-

         
          echo ${{ steps.deploy.outputs.url }}
'''
