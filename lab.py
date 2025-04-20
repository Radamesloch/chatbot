import re
i = 'Here is the extracted information in the requested JSON format: {"budget": "200000", "size": "200m2", "type": "buy", "city": "Chicago", "purpose": "office"}'

raw_data = re.sub(r'^.*?{', '{', i)
print(raw_data)
k = "hey, i am looking to buy a office, with 200m2, i have 200.000 dollars and i am looking ere in chicago"

l = "Extract the following information from this customer query:" + \
                        "budget (numeric value),size (text m2 descrition), type (buy/rent/leasing), city (location), purpose (apartment/office/house)" +\
                        "if a field has no value, return null."+\
                        "dont return a message, Return ONLY a JSON in this form "+\
                        '"{"budget": "", "size": "", "type": "", "city": "", "purpose": ""} "'+\
                        "with the extracted fields." +\
                        f"Query:  {k}"
print(type(l))