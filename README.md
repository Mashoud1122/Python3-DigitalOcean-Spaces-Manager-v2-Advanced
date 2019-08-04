# Python3-DigitalOcean-Spaces-Manager-v2-Advanced
Simple Pyhon3 module to help manage your spaces / cloud
<h1>DigitalOcean Spaces Made Easier and secured</h1>
<p></p>
<pre>
Most explanations in cloud-manage.py
cloud-manage.py - test of spaces module

<strong>NB: Modify these in spaces.py:
 #Key-ID
 key_id = str("Your-id-or-key")

#your secret key
secret_access_key = str("Your-secret-key")
</strong>

You can create your own amazing code just by importing the space module

Encrypt and Upload
Download files
Upload files
Delete Files
Create Spaces
List spaces / list spaces in particular regions
List files
and more
Hack my script[cloud-manage.py]

Kindly email me for bugs/features
</pre>

<h2>Simple Guide</h2>

firstly,
import the spaces file:
<pre>import spaces</pre>

<pre>
#region or region_name or space_region = the region of the space[nyc3, etc.]
#loca_file = name of file on local disk[Not SPACE. LOCAL DISK(YOUR COMPUTER)]
#name_when_uploaded = the name of file when put/uploaded on the space 

#To List Spaces
spaces.list_spaces_in(region)

#Files
spaces.list_files(region, space_name, "null")

#Upload_File 
spaces.upload_file(space_name, space_region, local_file, name_when_uploaded)

#Download File
spaces.download_file(space_name, region, file)

#Encrypt File And Upload
#key can be created by:
#spaces.create_key("your-password-string")
#so you can just make it
#Kindly make your password string very strong to avoid cracks after a data breach, etc. 

#spaces.encrypted_upload(space_name,region,file,file, spaces.create_key("your-password-string"))
spaces.encrypted_upload(space_name,region,file,file, key)
</pre>


