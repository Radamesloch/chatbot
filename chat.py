import random
import json
import torch
import re
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from openai import OpenAI
from typing import Dict, Optional
import redis


#configurations for torch model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)
FILE = "data.pth"
data = torch.load(FILE)
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]
model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

# variable configuration 
required_fields = ['budget', 'size', 'type', 'city', 'purpose']
user_data: Dict[str, Optional[str]] = {field: None for field in required_fields}

#redis instance
r = redis.Redis(host='redis', port=6379, decode_responses=True)
#for testing a mock redis session will be created.
#later implementation would be session Id for every client to save its information for the chatbot for some rational time
user_session = "abc123"

# Test connection
try:
    r.ping()
    print("Connected to Redis!")
except redis.exceptions.ConnectionError as e:
    print(f"Failed to connect: {e}")

#MAIN PROCESS
def get_Chat_response(text):
    bot_name = "Sam"

    while True:
        sentence = text
        if sentence == "quit":
            break

        sentence = tokenize(sentence)
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        output = model(X)
        _, predicted = torch.max(output, dim=1)

        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        
        #SIMPLE INTERACTIONS WITH MANUAL TRAINING FOR QUICK RESPONSES AS FAR AS IT IS GREETINGS, THANKING AND GOODBYE INPUT
        if prob.item() > 0.90 and len(text) < 30:
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    return(f"{bot_name}: {random.choice(intent['responses'])}")
        else:            
            #USING LLM MODEL FOR BETTER RESPONSES WHEN DEALING WITH REQUIRED DATA
            llm_data = llm_Call(text)
            print(llm_data)
            user_data = update_user_data(llm_data, False)
            missing_fields = get_missing_fields(user_data)

            ## there is a response for some of the missing fields leght, so the responses should be more human.
            if missing_fields:
                # If all the fields are missing                
                if len(missing_fields) == 5: 
                    return f"To help you best, please provide the following information: " + ", ".join(missing_fields)
                # if there is just one field missing
                elif len(missing_fields) == 1:
                    return f"One more thing, please provide the {missing_fields[0]}."
                else:
                    #if there is 2-4 fields missing.
                    return "We still need the following information: " + ", ".join(missing_fields)
            else:
                return f"""I got it! I will look for an available {user_data['purpose']} to {user_data['type']}, in {user_data['city']}. Close to ${user_data['budget']} USD,  with {user_data['size']} m2. """
    ## while state exit
    return "Bye Bye!"     
       
##AUXILIAR METHODS
def llm_Call(user_input):
        print("enter llm")
        print(user_input)

        
                #for testing this key will be here. When changing for a paid key or producction, this should be moved to a .env file
             
        try:            
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key="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",
            )

            completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
                "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
            },
            extra_body={},
            model="nvidia/llama-3.3-nemotron-super-49b-v1:free",
            messages=[
                {
                "role": "user",
                "content": "Extract the following information from this customer query:" + \
                        "budget (numeric value),size (text m2 descrition), type (buy/rent/leasing), city (location), purpose (apartment/office/house)" +\
                        "if a field has no value, return null."+\
                        "dont return a message, Return ONLY a JSON in this form "+\
                        '"{"budget": "", "size": "", "type": "", "city": "", "purpose": ""} "'+\
                        "with the extracted fields." +\
                        f"Query:  {user_input}"
                }
            ]
            )
            raw_data = re.sub(r'^.*?{', '{', completion.choices[0].message.content)       
            extracted_data = json.loads(raw_data)        
            return extracted_data
        except:
            return {'result pattern can be created for errors'}   

def update_user_data(extracted_data, flagClean):
    """cleaning user data"""
    if flagClean:
        for key, value in extracted_data.items():                            
            user_data[key] = None
    """Update the user's data with newly extracted fields"""
    for key, value in extracted_data.items():
        if value and key in required_fields:            
            if value != "null":
                user_data[key] = value
    return user_data


def get_missing_fields(user_data):
        """Return list of fields still needing to be filled"""
        missing = []
        for key, value in user_data.items():
            if value is None:
                missing.append(key)            
        return missing



## redis methods
def save_session(user_id, data):
    r.set(f'session:{user_id}', json.dumps(data), ex=3600)  # 1 hour TTL

def load_session(user_id):
    raw = r.get(f'session:{user_id}')
    print(raw)
    return json.loads(raw) if raw else {}