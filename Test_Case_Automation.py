import openai 
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import re
from googleapiclient.errors import HttpError
import string

# Set up OpenAI API key
openai.api_key = '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'
scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
credentials_path = 'credentials.json'

def get_chatgpt_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150
    )
    return response['choices'][0]['text']

def create_copy(service, file_id, copy_title):
    body = {'name': copy_title}
    new_file = service.files().copy(fileId=file_id, body=body).execute()
    return new_file['id']

def read_column_names(file_path):
    # Read column names from a text file
    with open(file_path, 'r') as file:
        column_names_line = file.readline().strip()
        column_names = column_names_line.split(',')
        print(column_names)
    return column_names

def read_row_names(file_path):
    file_path = '/Users/aadhikari/Desktop/main-main/PostVision_PostProcessed.txt'

    # Open the file in read mode
    with open(file_path, 'r') as file:
    # Read the entire contents of the file into a string
        file_contents = file.read()

    # Now, you can work with the file_contents variable, which contains the file's content as a string
    print(file_contents)
    # Read column names from a text file
    tested_lines = []
    expected_value_lines = []

    # Split the input text into lines
    lines = re.split(r'\d+\.\s', file_contents)
    tested_pattern = re.compile(r"Tested: `([^`]+)`")
    expected_value_pattern = re.compile(r"Expected value: (.+)")


    for pair in lines:
        # Find 'Tested' part
        tested_match = tested_pattern.search(pair)
        if tested_match:
            tested_lines.append(tested_match.group(1))
        # Find 'Expected value' part
        expected_value_match = expected_value_pattern.search(pair)
        if expected_value_match:
            expected_value_lines.append(expected_value_match.group(1))
    print("EV is " + str(expected_value_lines) +"TL is " + str(tested_lines))
    return tested_lines, expected_value_lines

def get_column_letter(index):
    uppercase_letters = string.ascii_uppercase
    return uppercase_letters[index % 26 - 1] if index <= 26 else uppercase_letters[int(index / 26) - 1] + uppercase_letters[index % 26 - 1]


def add_columns(worksheet,text_being_added):
    column_names = read_column_names(text_being_added)

    # Find the first empty row in the first row
    empty_column_index = 2
    while worksheet.cell(1, empty_column_index).value:
            empty_column_index += 1
            print("the first column empty cell is " + str(empty_column_index))

    # Update the first column starting from the first empty row
    for i, column_name in enumerate(column_names, start=empty_column_index):
        worksheet.update_cell(1, i, column_name)
        print ("Adding column_name to position " + column_name + " at position " + str(i))
        print("New columns have been added to spreadsheet")        
                
def add_rows(worksheet,text_being_added):
    Rows1,Rows2 = read_row_names(text_being_added)
    print ("this is Rows1" + str(Rows1))
    print ("this is Rows2" + str(Rows2))

    # Find the first empty row in the first column
    empty_row_index = 2
    while worksheet.cell(empty_row_index, 2).value:
        empty_row_index += 1
        print(" the first row empty cell is " + str(empty_row_index))
    

    
    # Update the first row starting from the first empty row
    for i ,( row1_name,row2_name) in enumerate(zip(Rows1,Rows2) ,start=empty_row_index):
        print("empty_row_index" + str(empty_row_index))
        worksheet.update_cell(i, 2, row1_name)  #Update first column with Rows1
        worksheet.update_cell(i, 3, row2_name)  # Update second column with Rows2


        first_row_values = worksheet.row_values(1)
        row_being_compared= worksheet.row_values(i)
        print ("Adding row_name to position " + row1_name + " at position " + str(i))
        print ("Adding row_name to position " + row2_name + " at position " + str(i))
        
        target_element= row1_name
        print(" target element" + target_element)
        for index, value in enumerate(first_row_values, start=1):
        # Check if the cell contains the target element
            if target_element in str(value):
                print(f"Element '{target_element}' found in cell A{index}")
                #filling out new sheet
                worksheet.update_cell(i, index , row2_name)
            # else:
            #     worksheet.update_cell(i,index,)
        row_being_compared= worksheet.row_values(i)
        print ("completed row is " + str(row_being_compared)+ " length is " + str(len(row_being_compared)))

        second_row_values = worksheet.row_values(2)
        print (" second_row_value is "  + str(second_row_values))
        for y in range(len(second_row_values)):
            if not row_being_compared[y]:
                if first_row_values[y] != "scenario":
                    row_being_compared[y] = second_row_values[y]
                    
                    

        print ("new row is " + str(row_being_compared))

        # for z,value1 in enumerate(row_being_compared):
        #     print (" i is " + str(i)  + " z is "+ str(z)+ "value is "+ value1)
        #     worksheet.update_cell(i,z+1,value1)
        end_column = get_column_letter(len(row_being_compared))
        print("end column is" + end_column)

        worksheet.update(f'A{i}:{end_column}{i}', [row_being_compared])



        

        

            # for index2,value2 in enumerate(row_being_compared, start=1):
            #     print (" In here")
            #     print("value is" + str(value2))
            #     if (value2 == " "  or worksheet.cell(i, index).value != "scenario"):
            #         print ("In here2 " )
            #         worksheet.update_cell(i,index2, value2)


        
        
        # if worksheet.cell(i,)


        # default_row=worksheet.row_values(0)
        # print ("default comparison row is " + str(default_row))
        # row_beingFilled=worksheet.row_values(i)      
        # print ("compared row is " + str(row_beingFilled))
        
        # for i in range(default_row):
        #     if row_beingFilled.cell().value()= " "
        #         row_beingFilled.cell().value()= default_row.cell.value()
        # filling out rest of row


        
    

def basic_credentials():
    print("in here")
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json",scope)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow= InstalledAppFlow.from_client_secrets_file("credentials2.json",scope,redirect_uri="urn:ietf:wg:oauth:2.0:oob")
            credentials = flow.run_local_server(port=0) 
        with open("token.json", "w") as token:
            token.write(credentials.to_json())
    
    print("OAuth 2.0 credentials obtained with scopes:", credentials.scopes)
    
    try:
        # Attempt to load credentials
        
        flow= InstalledAppFlow.from_client_secrets_file("credentials2.json",scope)
        print("Credentials loaded successfully.")
    except Exception as e:
        print("Error loading credentials:", e)
        raise  # This will terminate the program and show the full error
    print ("gotcredentials")
    return credentials
    
def main():
    
    Rows1,Rows2=read_row_names('/Users/aadhikari/Desktop/main-main/PostVision_PostProcessed.txt')
    


    credentials=basic_credentials()

    gc = gspread.authorize(credentials)
    sheet_to_copy=input("what sheet do you want to copy? ")
    new_sheet_name= input("What do you want your new sheet to be called? ")
    
    
    try:
        #Opening sheet, creating new sheet and taking its id so I can edit it
        sheet = gc.open(sheet_to_copy)
        service = build('drive', 'v3', credentials=credentials)
        new_sheet_id = create_copy(service, sheet.id, new_sheet_name)
        new_sheet_being_changed=gc.open(new_sheet_name)
        
        #Going from spreadsheet to worksheet of new file
        worksheet = new_sheet_being_changed.sheet1
        #Adding column names to spreadsheet from first empty column
        text_files_columns=input("Do you have a txt file with columns? Answer yes/no ")
        if (text_files_columns == "yes"):
            column_names_file_path = 'columns.txt'
            add_columns(worksheet, column_names_file_path)
                
        #Adding row names to spreadsheet from first empty row
        text_files_rows=input("Do you have a txt file with rows? Answer yes/no ")
        #parsing file from txt

        if (text_files_rows == "yes"):
            rows_names_file_path = '/Users/aadhikari/Desktop/main-main/PostVision_PostProcessed.txt'

            add_rows(worksheet,Rows1)
            print ("just showed row1")

            

    except (gspread.exceptions.SpreadsheetNotFound,Exception) as e:
        print("Error: Spreadsheet not found. Check the name or ID:", e)

 
    # Example ChatGPT interaction
    try:
        request= input("What do you want us to do? ")
        chatgpt_response=get_chatgpt_response(request)
        
    except Exception as e:
        print("Error in ChatGPT interaction:", e)
        return  # Terminate the program
    
    if worksheet is not None:
        worksheet.update_cell(6, 1, chatgpt_response)
        print("Worksheet successfully obtained. Do more operations if needed.")
        print("Google Sheet updated with ChatGPT response:", chatgpt_response)
    else:
        print("Worksheet is None. Check for errors in the try block.")
   
if __name__== "__main__":
    main()