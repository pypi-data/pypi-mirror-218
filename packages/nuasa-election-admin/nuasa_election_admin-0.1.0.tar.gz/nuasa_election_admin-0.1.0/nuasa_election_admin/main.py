import typer
import configparser
import requests
import csv
from rich.table import Table
import rich
import time
import os


app = typer.Typer()
configparser = configparser.ConfigParser()
cmd_header = 'ZAnrWvAesvQRNR-EsezBx3uMGsXpQbdcQJ7T2D_V2B4x5wou9N4PFPQoNBQhDxYKeNBPkjt3OavvLPBB'
BASE_URL = 'https://nuasaelection.alwaysdata.net'
cc = 'http://127.0.0.1:8000'


def getToken():
    import configparser
    config_read = configparser.ConfigParser()
    config_read.read("config.ini")
    read_token = config_read.get("UserSettings", "token")
    return read_token


@app.command()
def hello(name:str):
    print(f'Hello and Welcome {name}')

@app.command()
def adminsetup():
    email = input("Input your email: ")
    first_name = input("Input your first name: ")
    last_name = input("Input your last name: ")
    password1 = input("Input your password: ")
    password2 = input("confirm your password: ")

    if password1 != password2:
        print("Passwords do not match")
    #set up payload data  
    URL = BASE_URL + '/api/register/'
    data = {
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'password': password1
    }
    Headers = {
        'Content-Type': 'application/json',
        'token': cmd_header
    }
    # make the request
    api_call = requests.post(URL, json=data, headers=Headers)
    if api_call.status_code == 201:
        response = dict(api_call.json())
        #store the token
        configparser["UserSettings"] = {
            "Token": response['token']
        }
        with open("config.ini", "w") as configfile:
            configparser.write(configfile)
            print('Admin details saved')
        print('set up complete')
    else:
        print(api_call.headers)
        print(f'Admin setup failed code: {api_call.status_code}')



@app.command()
def admin_login():
    email = input('Enter your email: ')
    password = input('Enter your password: ')

    URL = BASE_URL + '/api/login/'
    data = {
        'email': email,
        'password': password
    }
    Headers = {
        'Content-Type': 'application/json',
    }
    api_call = requests.post(URL, json=data, headers=Headers)

    if api_call.status_code == 200:
        response = dict(api_call.json())
        #store the token
        configparser["UserSettings"] = {
            "Token": response['token']
        }
        with open("config.ini", "w") as configfile:
            configparser.write(configfile)
            print('Login details saved')
        print('Login successfull')
    else:
        print(f'Admin login failed code: {api_call.status_code}')




@app.command()
def create_election():
    name = input("Input election name: ")
    election_pid = input("Election short name or tag: ")

    URL = BASE_URL + '/api/create_election/'
    data = {
        'name': name,
        'election_public_id': election_pid
    }
    Token = getToken()
    Headers = {
        'Content-Type': 'application/json',
        'token': Token
    }

    # make the request
    api_call = requests.post(URL, json=data, headers=Headers)
    if api_call.status_code == 201:
        response = dict(api_call.json())
        print("Election private key will be displayed. Keep secret.")
        print(f'Private key: {response["private_key"]}')
    else:
        print(f'Election creation failed, code: {api_call.status_code}')



@app.command()
def create_office():
    name = input("Name of office: ")
    election_id = input("Election Id (get election Id by running 'get-elections')")

    URL = BASE_URL + '/api/create_office/'
    data = {
        'name': name,
        'election_id': election_id
    }
    Token = getToken()
    Headers = {
        'Content-Type': 'application/json',
        'token': Token
    }
    api_call = requests.post(URL, json=data, headers=Headers)
    if api_call.status_code == 201:
        response = dict(api_call.json())
        print("Office successfully created")
    else:
        print(f'Office creation failed, code: {api_call.status_code}')


@app.command()
def get_elections():
    URL = BASE_URL + '/api/get_elections/'
    Token = getToken()
    Headers = {
        'Content-Type': 'application/json',
        'token': Token
    }
    api_call = requests.get(URL, headers=Headers)
    if api_call.status_code == 200:
        response = dict(api_call.json())
        if response.get('elections') != []:
            table = Table('Election name', 'Election ID', 'Election tag')
            for i in response.get('elections'):
                table.add_row(i['election_name'], i['election_id'], i['election_tag'])
            rich.print(table)
            print('Data successfully retrieved')
        else:
            print('No elections found')
    else:
        print(f'API call failed, code: {api_call.status_code}')
    


@app.command()
def get_offices():
    election_id  = input('Enter election id: ')
    URL = BASE_URL + f'/api/get_offices/{election_id}/'
    Token = getToken()
    Headers = {
        'Content-Type': 'application/json',
        'token': Token
    }
    api_call = requests.get(URL, headers=Headers)
    if api_call.status_code == 200:
        response = dict(api_call.json())
        if response.get('offices') != []:
            table = Table('Office id', 'Office name')
            for i in response.get('offices'):
                table.add_row(i['office_id'], i['office_name'])
            rich.print(table)
            print('Data successfully retrieved')
        else:
            print('No elections found')
    else:
        print(f'API Call failed, code: {api_call.status_code}')



@app.command()
def register_candidates():
    name = input("Name of candidate: ")
    picture_link = input("Candidate picture link: ")
    office_id = input("Office Id: ")

    URL = BASE_URL + '/api/register_candidates/'
    data = {
        'name': name,
        'picture': picture_link,
        'office_id': office_id
    }
    Token = getToken()
    Headers = {
        'Content-Type': 'application/json',
        'token': Token
    }
    api_call = requests.post(URL, json=data, headers=Headers)
    if api_call.status_code == 201:
        response = dict(api_call.json())
        print("Candidate successfully registered")
    else:
        print(f'Candidate registeration failed, code: {api_call.status_code}')



@app.command()
def get_voter():
    reg_number = input("Input student REG No (XXXX): ")
    URL = BASE_URL + '/api/get_voter/'
    data = {
        'reg_number': reg_number
    }
    Token = getToken()
    Headers = {
        'Content-Type': 'application/json',
        'token': Token
    }
    api_call = requests.get(URL, json=data, headers=Headers)
    if api_call.status_code == 200:
        response = dict(api_call.json())
        if response.get('status') == False:
            print(f'Get voter details failed with msg : {response.get("msg")}')
        else:
            print(f'Student voting password: {response.get("password")}')
            time.sleep(15)
            os.system('cls')
    else:
        print(f'API call failed, code: {api_call.status_code}')


#next
@app.command()
def upload_voters():
    file_name = input("File name (ensure file is in the same directory as program): ")
    URL = BASE_URL + '/api/register_voters/'
    Token = getToken()
    Headers = {
        'Content-Type': 'application/json',
        'token': Token
    }
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data = {
                'reg_number': row[0],
                'password': row[1]
            }
            api_call = requests.post(URL, json=data, headers=Headers)
            if api_call.status_code == 201:
                response = dict(api_call.json())
                print(response)
            else:
                print(f'API call failed, code: {api_call.status_code}')
        print("Successfully uploaded data")
    
#get stat
@app.command()
def get_stat():
    URL = BASE_URL + '/api/stat/'
    Token = getToken()
    Headers = {
        'Content-Type': 'application/json',
        'token': Token
    }
    api_call = requests.get(URL, headers=Headers)
    if api_call.status_code == 200:
        response = dict(api_call.json())
        print(f'Number of registered voters: {response.get("registered")}')
        print(f'Number of collected voters: {response.get("collected")}')
        print(f'Number of casted votes: {response.get("casted")}') 
    else:
        print(f'API call failed, code: {api_call.status_code}')

#ACTIVATE ELECTION
@app.command()
def activate_election():
    secret_key = input("Input election secret key: ")
    URL = BASE_URL + '/api/activate_election/'
    data = {
        'secret_key': secret_key
    }
    Token = getToken()
    Headers = {
        'Content-Type': 'application/json',
        'token': Token
    }
    api_call = requests.post(URL, json=data, headers=Headers)
    if api_call.status_code == 200:
        response = dict(api_call.json())
        print(response.get('msg'))
    else:
        print(f'API call failed, code: {api_call.status_code}')

#DEACTIVATE
@app.command()
def deactivate_election():
    secret_key = input("Input election secret key: ")
    URL = BASE_URL + '/api/deactivate_election/'
    data = {
        'secret_key': secret_key
    }
    Token = getToken()
    Headers = {
        'Content-Type': 'application/json',
        'token': Token
    }
    api_call = requests.post(URL, json=data, headers=Headers)
    if api_call.status_code == 200:
        response = dict(api_call.json())
        print(response.get('msg'))
    else:
        print(f'API call failed, code: {api_call.status_code}')


@app.command()
def wipe_off():
    URL = BASE_URL + '/api/wipe_data/'
    Token = getToken()
    Headers = {
        'Content-Type': 'application/json',
        'token': Token
    }
    api_call = requests.get(URL, headers=Headers)
    if api_call.status_code == 200:
        response = dict(api_call.json())
        print(f'Data successfully cleaned off')
        print(response)
    else:
        print(f'API call failed, code: {api_call.status_code}')

