

import json
from openai import OpenAI


client = OpenAI(api_key = "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")

Vision_postProcessed= """ Here is the breakdown of the flow:

1. It starts from the left side, checking whether an array pertaining to `data.cmp.data.aggregatedMemberInfo.redflags` is populated. 
   
2. If the array is not populated, the flow directly leads to "Pass," indicating no red flags were found in the member information.

3. If the array is populated, the flow continues to check the `redflags.status`. If the status equals "CONFIRMED," the process leads to the right part of the chart.

4. Then, it examines the `redflags.flagtype`. If the type includes "DECEASED," "LEGAL," or "AML" (which typically stands for Anti-Money Laundering), the process results in a "Hard Fail."

5. If the flag types are none of the above, the process moves down to check `redflags.category`. If the category equals "CARD_TRANSACTION_NOT_FRAUD," it suggests that there is no fraud detected related to card transactions, leading back to "Pass."

6. If the category is not "CARD_TRANSACTION_NOT_FRAUD," the process would presumably lead to a fail or some further action, but this part of the flow is not visible in the image provided.

7. There are comments in the yellow boxes."""





response = client.chat.completions.create(
  model="gpt-4-1106-preview",
#   response_format={ "type": "json_object" },
  messages=[
    {"role": "system", "content": "You are a helpful assistant designed to read a list and write down everything that is being tested"},
    {"role": "user", "content": """I am going to give you a workflow that is going to be described.
    I want you to go through each numbered line and for each line give me what is being tested the value it can have. If there is
    multiple things being tested I want you to split it up and write it in a new line. For exmaple if something is called data.cmp.data.aggregatedMemberInfo.redflags
     and it can be populated or not populated I want to see 1. tested: data.cmp.data.aggregatedMemberInfo.redflags, expected value: populated. 2. tested: data.cmp.data.aggregatedMemberInfo.redflags,expected value:not populated.
    """ + Vision_postProcessed 
     }
  ])
# I am going to give you a workflow that is going to be described.
#     You are an expert note taker, who is writing a document . 
#     Each line is going to have what you are checking for, and then 1 possible value and then its expected value.  
#     You will output it in 4 different lines with its expected value so it would be tested: redflags, value:" legal", expected value: " hard fail". This is the format each line
#     should have 3 attributes- tested, value and expected value as well as what it is testing. If there is multiple values I want you to output
#     the same tested attribute again in another line but with a different value. There should only be 1 element in each value attribute
  
print (response)
print ("testing content")
content2 = response.choices[0].message.content.replace('\n', '')
print(content2)
print(type(content2))
print ("testing content done")
file_path = "PostVision_PostProcessed.txt"

# Open the file in write mode and write the content
with open(file_path, "w") as file:
    file.write(content2)

print(f"Output has been saved to {file_path}")




# parsed_list = json.loads(response.choices[0].message.content)
# print (parsed_list) 
result = []

                                # for level in parsed_list['workflow']:
                                #     for scenario_data in parsed_list['workflow'][level].get('scenarios')
                                #         scenario = scenario_data['scenarios']
                                #         value = scenario_data['value']
                                #         result.append(f"{scenario}: {value}")

                                # # Print the result array
                                # for item in result:
                                #     print(item)

