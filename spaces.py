#When listing spaces  data will be displayed like this. [[this-ams3-region], [this-nyc3-region], [this-sgp1-region], [this-sfo2-region]]
#array0 - ams3
#array1 - nyc3
#array2 - sgp1
#array3 - sfo2

import boto3
from botocore.client import Config
import os
import time
import fernet
import os
import random
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from datetime import datetime

#your key id
key_id = str("Your-id-or-key")
#your secret key
secret_access_key = str("Your-secret-key")


regions = ['ams3', 'nyc3', 'sgp1', 'sfo2']

def space_connect(region_name):
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name=str(region_name),
                            endpoint_url='https://' + str(region_name) + '.digitaloceanspaces.com',
                            aws_access_key_id=key_id,
                            aws_secret_access_key=secret_access_key)
    return client

def list_spaces():
    regions = ['ams3', 'nyc3', 'sgp1', 'sfo2']
    #array0 - ams3
    #array1 - nyc3
    #array2 - sgp1
    #array3 - sfo2
    available_spaces = [[], [], [], []]
    b = -1
    if b < 5:
        for i in regions:
            b += 1
            # print("checking servers in " + i)
            response = space_connect(i).list_buckets()
            buckets = [bucket['Name'] for bucket in response['Buckets']]
            for space_num in buckets:
                # print(space_num)
                available_spaces[b].append(str(space_num))

    return available_spaces

def list_spaces_in(region):
    spaces_region = []
    if region.lower() in regions:
        response = space_connect(region).list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        for space_num in buckets:
            spaces_region.append(space_num)

        return spaces_region
    else:
        return "Error: Possibly Invalid Region"

def list_files(region_name, space_name, dir):
    #take argument for particular directory file listing
    #Put a try:
    r = space_connect(region_name).list_objects(Bucket=space_name)
    files = r.get('Contents')
    i = 0
    p = str(files)

    if p == "None":
        print("No Data available")
    else:
        for file in files:
            if len(file) > 0:
                i += 1
            else:
                continue
            file_detect = file['Key']
            if file_detect[-1:] == '/':
                file_type = "Folder"
            else:
                file_type = "File"

            print("Object: ")
            print("     Name: " + file['Key'] + " [" + file_type + "]")
            print("     Size: " + str(file['Size']) + " bytes")
            date, time = str(file['LastModified']).split(" ")
            print("     Last Modified: ")
            print("             Date: " + date)
            # later make function that determines from 2018-09-29 09:00:17.235000+00:00
            # to detect date, time, and timezone - GMT, etc.
            # time, date - done already
            timeh, useless = time.split(".")
            print("             Time: " + timeh)

def download_file(space_name, region_name, file_name):
    s3 = space_connect(region_name)
    local_path = file_name #mistake i made so had to fix here :)
    try:
        s3.download_file(space_name, file_name, local_path)
        print("Data written to ->" + local_path)
    except:
        print("Error: Maybe file does not exist, or check the path you are saving to ")
        print("Usage: download file_to_download_from_the_space file_name_to_save_on_disk")
        print("Ex: download mytest-from-cloud docs.txt")
    #USAGE: download_file('space_name', 'nyc3', 'file_in_space.txt', 'file.txt')

def upload_file(space_name, region_name, local_file, upload_name):
    s3 = space_connect(region_name)
    try:
        s3.upload_file(local_file, space_name, upload_name)
        message = "Success"
        return message
        # pass
    except Exception as e:
        message = "Error occured. Check Space name, etc"

    return message
    #upload_file('my-space-name', 'sfo2', 'test.txt', 'me1.txt')

def create_space(name, region):
    region = region.lower()
    if region in regions:
        try:
            client = space_connect(region)
            creation = client.create_bucket(Bucket=str(name))
            print("Success")
            print("https://" + name + "." + region + ".digitaloceanspaces.com is now available")
        except:
            print("Error: Maybe Inavlid Name")
            # create_space("mytestspace", "ams3")


def create_key(key):
    password_provided = key # This is input in the form of a string
    password = password_provided.encode() # Convert to type bytes
    salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once
    return key

def encrypted_upload(space_name, region_name, local_file, upload_name, key):
    if os.path.isfile(local_file):
        file_name = datetime.today().strftime('%Y-%m-%d') + "-" + str(random.randint(1000, 10000)) + local_file + '.tmp'
        fernet.encrypt(local_file, file_name, key)
        local_file = os.getcwd() + '/tmp/' + file_name
        print(local_file)
        upload_file(space_name, region_name, local_file, upload_name + '.enc')
        return "Success"
    else:
        return "Error"

# key = create_key("password")
# encrypted_upload("my-space-name","sfo2","test.txt","testers", key)
