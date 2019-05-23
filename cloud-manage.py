
import spaces
import os

regions = ['ams3', 'nyc3', 'sgp1', 'sfo2']
# try:
print("Type help for more")
print("ctrl + c to exit")
def line():
    print("+------------------------------------+")
while True:
    option = input("$cloud->")
    option = option.lower()
    if option.lower() == "help":
        line()
        print("""+------------------------------------+
list spaces
	-list spaces in all regions

+------------------------------------+
list spaces in a region
list spaces/region-name
	-list spaces in a particular region

+------------------------------------+
list files
files space-name/region
	-list files in a space

+------------------------------------+
upload files
upload my-file.txt name-when-uploaded.txt space/region
	-upload files to a space

+------------------------------------+
download file
download file_on_space space_name/region
	-download file from a space

+------------------------------------+
::Encrypted Upload::
encrypted-upload filename
	-follow steps
	-encrypt file before/and upload to space
+------------------------------------+""")
        line()

    elif option.lower() == "list spaces":
        line()
        av_spaces = spaces.list_spaces()
        print(av_spaces)
        line()
        print("ams3->" + str(av_spaces[0]))
        print("nyc3->" + str(av_spaces[1]))
        print("sgp1->" + str(av_spaces[2]))
        print("sfo2->" + str(av_spaces[3]))
        line()


    elif option.lower()[:12] == "list spaces/":
        #LIST SPACES IN A PARTICULAR REGION PROVIDED
        random_i_op123 = option.lower()
        cmd, region = random_i_op123.split('/')
        if region in regions:
            line()
            cloud_spaces = spaces.list_spaces_in(region)
            if len(cloud_spaces) == 0:
                print("No Data/Spaces")
            else:
                for space in cloud_spaces:
                    print("['" + str(space) + "']")
                line()
        else:
            print('Region not listed. Available Regions: ' + str(regions))
            print('info: list spaces/region-name')
            print('Usage: list spaces/nyc3')

    elif option.lower()[:5] == 'files':
        try:
            rand_option_var = option
            cmd, rest =  rand_option_var.split(" ")
            space_name, region = rest.split("/")
            if region in regions:
                print(spaces.list_files(region, space_name, "null"))
            else:
                print("Invalid Region selected")
        except:
            print("Error. Usage: files space_name/region")
            print("Usage: files my-secure-space/nyc3")

    elif option.lower()[:3] == 'use':
        #spaces Shell
        print("Not available at the moment")


    elif option.lower()[:6] == "upload":
        #usage: upload my-file.txt space/region
        try:
            cmd, local_file, name_when_uploaded, space_info = option.split(" ")
            space_name, space_region = space_info.split("/")
            if space_region in regions:
                if os.path.isfile(local_file):
                    #space_name, region_name, local_file, upload_name
                    print(spaces.upload_file(space_name, space_region, local_file, name_when_uploaded))
                else:
                    print("File to be upload not found.")
            else:
                print("Invalid region name")
                print("Valid regions: " + regions)

        except:
            print("Error: ")
            print("Usage: upload my-file.txt name-when-uploaded.txt space/region")

    elif option[:8] == 'download':
        #usage: download file_on_space space_name/region
        try:
            cmd, file, space_info = option.split(" ")
            space_name, region = space_info.split("/")
            #space_name, file_name, local_path
            print(spaces.download_file(space_name, region, file))
        except:
            print("usage: download file_on_space space_name/region")

    elif option[:16] == 'encrypted-upload':
        try:
            cmd, file = option.split(" ")
            if os.path.isfile(file):
                # try:
                while True:
                    print(":: This file will be encrypted and uploaded to the server ::")
                    print(":: Kindly use a secure password and store it safe ::")
                    print(":: If you loose your password this software cannot recover it ::")
                    space_name = input("Space Name: ")
                    # sleep(2)
                    print("Type as such: " + str(regions))
                    region = input("Space-Region: ")
                    if region in regions:
                        password = input("Create Password: ")
                        key = spaces.create_key(password)
                        print("Uploaded and saved locally to ->")
                        print(spaces.encrypted_upload(space_name.lower(),region.lower(),file,file, key))
                        break

                    else:
                        print("Invalid Region")
                        print("Available region: " + str(regions))
            else:
                print("File not found")
        except:
            print("[Error]")
            print("Usage: encrypted-upload file")
            print("Files with spaces in file-name might cause problems")

# except Exception as e:
#     print("Error occured. Maybe connection was not established :(")
