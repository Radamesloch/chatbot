from chat import update_user_data, get_Chat_response, get_missing_fields
import json
import unittest
import pytest
from typing import Dict, Optional



def MOCK_llm_Call(user_input):
        
        #Mock completion response
        completion = user_input
        try:      
            data = json.loads(completion)       
            return data
        except:
            return {}   
def mock_response(missing_fields,user_data):
    if missing_fields:
        # Prompt for missing information
        if len(missing_fields) == 5:
            return f"To help you best, please provide the following information: " + ", ".join(missing_fields)
        elif len(missing_fields) == 1:
            return f"To help you best, please provide your {missing_fields[0]}."
        else:
            return "We still need the following information: " + ", ".join(missing_fields)
    else:
        
        return f"""I got it! I will look for an available {user_data['purpose']} to {user_data['type']}, in {user_data['city']}. Close to {user_data['budget']} and with {user_data['size']} m2. """
    

def MOCK_get_Chat_response(text):
    bot_name = "Sam"    
    while True:
        if text == "quit":
            break
        llm_data = MOCK_llm_Call(text)
        user_data = update_user_data(llm_data, False)
        missing_fields = get_missing_fields(user_data)
        if missing_fields:            
            # Prompt for missing information
            if len(missing_fields) == 5:
                return f"To help you best, please provide the following information: " + ", ".join(missing_fields)
            elif len(missing_fields) == 1:
                return f"To help you best, please provide your {missing_fields[0]}."
            else:
                return "We still need the following information: " + ", ".join(missing_fields)
        else:
            
            return f"""I got it! I will look for an available {user_data['purpose']} to {user_data['type']}, in {user_data['city']}. Close to {user_data['budget']} and with {user_data['size']} m2. """
       


class Test(unittest.TestCase):
    
    def setUp(self):
        self.required_fields = ['budget', 'size', 'type', 'city','purpose']
        self.user_data: Dict[str, Optional[str]] = {field: None for field in self.required_fields}
        with open('intents.json', 'r') as json_data:
            self.intents = json.load(json_data)        
        self.mock_input = '{"budget": "1000", "size": "200", "type": "buy", "city": "NYC", "purpose": "office"}'
        self.mock_input2 = '{"budget": "2000", "size": "200", "type": "buy", "city": null, "purpose": "office"}'
        self.mock_input3 = '{"budget": "3000", "size": "200", "type": null, "city": null, "purpose": "office"}'
        self.mock_input4 = '{"budget": null, "size": null, "type": null, "city": null, "purpose": "office"}'
        self.mock_input5 = '{"budget": null, "size": null, "type": null, "city": null, "purpose": null}'
        self.response_all = f"""I got it! I will look for an available office to buy, in NYC. Close to 1000 and with 200 m2. """
        self.response_1_missing = "To help you best, please provide your city."
        self.response_all_missing = "To help you best, please provide the following information: budget, size, type, city, purpose" 
        self.response_more_missing = "We still need the following information: type, city"
        self.mock_greeting = 'hello'
        self.mock_thanks = 'thank you'
        self.mock_goodbye = 'goodbye'
        self.mock_exit = 'exit'
        self.mock_miss_response1 = '{"budget": null, "size": "200", "type": "buy", "city": "NYC", "purpose": "office"}'
        self.mock_miss_test1 = ['budget']
        self.mock_miss_response2 = '{"budget": "1000", "size": null, "type": "buy", "city": "NYC", "purpose": "office"}'
        self.mock_miss_test2 = ['size']
        self.mock_miss_response3 = '{"budget": "1000", "size": "200", "type": null, "city": "NYC", "purpose": "office"}'
        self.mock_miss_test3 = ['type']
        self.mock_miss_response4 = '{"budget": "1000", "size": "200", "type": "buy", "city": null, "purpose": "office"}'
        self.mock_miss_test4 = ['city']
        self.mock_miss_response5 = '{"budget": null, "size": null, "type": "buy", "city": "NYC", "purpose": "office"}'
        self.mock_miss_test5 = ['budget','size']
        self.mock_miss_response6 = '{"budget": "1000", "size": "200", "type": null, "city": null, "purpose": "office"}'
        self.mock_miss_test6 = ['type','city']
        self.mock_miss_test7 = []
        self.mock_miss_response8 = '{"budget": "1000", "size": "200", "type": "buy", "city": "NYC", "purpose": null}'
        self.mock_miss_test8 = ['purpose']
        self.mock_update1 = '{"budget": "1000", "size": null, "type": null, "city": null, "purpose": null}'
        self.mock_update2 = '{"budget": null, "size": "200", "type": null, "city": null, "purpose": null}'
        self.mock_update3 = '{"budget": null, "size": null, "type": "buy", "city": null, "purpose": null}'
        self.mock_update4 = '{"budget": null, "size": null, "type": null, "city": "NYC", "purpose": null}'
        self.mock_update5 = '{"budget": null, "size": null, "type": null, "city": null, "purpose": "office"}'
        self.mock_conversation = [
            '{"budget": "1000"}',  
            '{"size": "200"}',  
            '{"type":"buy"}',
            '{"city": "NYC"}', 
            '{"purpose": "office"}' 
        ]

    #unit testings
    def test_get_chat_response_hello(self):      
        response = get_Chat_response(self.mock_greeting)                      
        for item in self.intents["intents"][0]["responses"]:
            val = f"""Sam: {item}"""
            if(response == val):
                break
        self.assertEqual(response, val)
                
    def test_get_chat_response_thanks(self):                  
        response = get_Chat_response(self.mock_thanks)          
        for item in self.intents["intents"][2]["responses"]:
            val = f"""Sam: {item}"""
            if(response == val):
                break
        self.assertEqual(response, val)

    def test_get_chat_response_bye(self):                    
        response = get_Chat_response(self.mock_goodbye)            
        for item in self.intents["intents"][1]["responses"]:
            val = f"""Sam: {item}"""
            if(response == val):
                break
        self.assertEqual(response, val)

    def test_mock_llm_call(self):        
        self.assertIsInstance(MOCK_llm_Call(self.mock_input), dict)    
         
    def test_get_missing_fields(self):
        test = MOCK_llm_Call(self.mock_miss_response1)       
        self.assertEqual(get_missing_fields(test), self.mock_miss_test1)
        self.assertNotEqual(get_missing_fields(test), self.mock_miss_test7)

        test = MOCK_llm_Call(self.mock_miss_response2)       
        self.assertEqual(get_missing_fields(test), self.mock_miss_test2)
        self.assertNotEqual(get_missing_fields(test), self.mock_miss_test7)
    
        test = MOCK_llm_Call(self.mock_miss_response3)       
        self.assertEqual(get_missing_fields(test), self.mock_miss_test3)
        self.assertNotEqual(get_missing_fields(test), self.mock_miss_test7)

        test = MOCK_llm_Call(self.mock_miss_response4)       
        self.assertEqual(get_missing_fields(test), self.mock_miss_test4)
        self.assertNotEqual(get_missing_fields(test), self.mock_miss_test7)

        test = MOCK_llm_Call(self.mock_miss_response5)       
        self.assertEqual(get_missing_fields(test), self.mock_miss_test5)
        self.assertNotEqual(get_missing_fields(test), self.mock_miss_test7)
        
        test = MOCK_llm_Call(self.mock_miss_response6)       
        self.assertEqual(get_missing_fields(test), self.mock_miss_test6)
        self.assertNotEqual(get_missing_fields(test), self.mock_miss_test7)

        test = MOCK_llm_Call(self.mock_miss_response8)       
        self.assertEqual(get_missing_fields(test), self.mock_miss_test8)
        self.assertNotEqual(get_missing_fields(test), self.mock_miss_test7)
    
    def test_update_user_data(self):
        test_data = MOCK_llm_Call(self.mock_update1)
        self.user_data = update_user_data(test_data, False)

        test_data = MOCK_llm_Call(self.mock_update2)
        self.user_data = update_user_data(test_data, False)

        test_data = MOCK_llm_Call(self.mock_update3)
        self.user_data = update_user_data(test_data, False)

        test_data = MOCK_llm_Call(self.mock_update4)
        self.user_data = update_user_data(test_data, False)
        test_data = MOCK_llm_Call(self.mock_update5)
        self.user_data = update_user_data(test_data, False)
        
        self.assertEqual(self.user_data,{'budget': '1000', 'size': '200', 'type': 'buy', 'city': 'NYC', "purpose": "office"})
         
    # # integration test

    def test_full_process_completed(self):
        input = MOCK_llm_Call(self.mock_input)
        self.user_data = update_user_data(input, True)
        missing_fields = get_missing_fields(self.user_data)
        response = mock_response(missing_fields, self.user_data)  
        print(self.user_data)     
        self.assertEqual(self.response_all, response)

    def test_full_process_miss_1(self):
        input = MOCK_llm_Call(self.mock_input2)
        data = update_user_data(input, True)
        missing_fields = get_missing_fields(data)
        response = mock_response(missing_fields, self.user_data)
        self.assertEqual(self.response_1_missing, response)

    def test_full_process_miss_more(self):    
        input = MOCK_llm_Call(self.mock_input3)
        data = update_user_data(input, True)
        missing_fields = get_missing_fields(data)
        response = mock_response(missing_fields, self.user_data)
        self.assertEqual(self.response_more_missing, response)
    
    def test_full_process_miss_all(self):
        input = MOCK_llm_Call(self.mock_input5)
        data = update_user_data(input, True)
        missing_fields = get_missing_fields(data)
        response = mock_response(missing_fields, self.user_data)
        self.assertEqual(self.response_all_missing, response)    
       
    def test_full_conversation_flow(self):
        # Mock LLM responses for a complete conversation
        
        # First turn
        response1 =  MOCK_get_Chat_response(self.mock_conversation[0])
        # Second turn
        response2 =  MOCK_get_Chat_response(self.mock_conversation[1])
        # Third turn
        response3 =  MOCK_get_Chat_response(self.mock_conversation[2])
        ## fourth turn
        response4 =  MOCK_get_Chat_response(self.mock_conversation[3])
        # # Final Turn
        response5 =  MOCK_get_Chat_response(self.mock_conversation[4])
        
        self.assertEqual(response1, "We still need the following information: size, type, city, purpose")
        self.assertEqual(response2, "We still need the following information: type, city, purpose")
        self.assertEqual(response3, "We still need the following information: city, purpose")
        self.assertEqual(response4, "To help you best, please provide your purpose.")
        self.assertEqual(response5, self.response_all)


if __name__ == "__main__":
    unittest.main()

