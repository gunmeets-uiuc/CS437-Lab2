################################################### Connecting to AWS
import boto3

import json
################################################### Create random name for things
import random
import string

################################################### Parameters for Thing
thingArn = ''
thingId = ''
#thingName = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(15)])
defaultPolicyName = 'Lab4_Iot_Policy'
Thing_group_name = 'Biplab_IoT_Things_Group_Lab04' 
###################################################

def createThing(ThingName):
	global thingClient
	thingResponse = thingClient.create_thing(
	thingName = ThingName)
	data = json.loads(json.dumps(thingResponse, sort_keys=False, indent=4))
	for element in data: 
		if element == 'thingArn':
			thingArn = data['thingArn']
		elif element == 'thingId':
        		thingId = data['thingId']
        		createCertificate(ThingName)

def createCertificate(ThingName):
	global thingClient
	certResponse = thingClient.create_keys_and_certificate(setAsActive = True)
	data = json.loads(json.dumps(certResponse, sort_keys=False, indent=4))
#	print(data)
	for element in data: 
		if element == 'certificateArn':
			certificateArn = data['certificateArn']
		elif element == 'keyPair':
			PublicKey = data['keyPair']['PublicKey']
			PrivateKey = data['keyPair']['PrivateKey']
		elif element == 'certificatePem':
			certificatePem = data['certificatePem']
		elif element == 'certificateId':
			certificateId = data['certificateId']
							
	with open(ThingName+'_public.key', 'w') as outfile:
		outfile.write(PublicKey)
	with open(ThingName+'_private.key', 'w') as outfile:
		outfile.write(PrivateKey)
	with open(ThingName+'_cert.pem', 'w') as outfile:
		outfile.write(certificatePem)

	response = thingClient.attach_policy(policyName = defaultPolicyName,target = certificateArn)
	try:
		response = thingClient.attach_thing_principal(thingName = ThingName,principal = certificateArn)
		print(f"Successfully attached the certificate to the thing '{ThingName}'.")
	
	except thingClient.exceptions.ResourceNotFoundException:
		print("The specified thing or certificate does not exist.")
	except thingClient.exceptions.InvalidRequestException as e:
    		print("Invalid request:", e)
	except thingClient.exceptions.ThrottlingException:
		print("Request throttled. Try again later.")
	except thingClient.exceptions.InternalFailureException:
    		print("An internal error occurred. Please try again.")
	except Exception as e:
    		print("An unexpected error occurred:", e)

	response = thingClient.add_thing_to_thing_group(thingGroupName=Thing_group_name,thingName=ThingName)

thingClient = boto3.client('iot',
                           aws_access_key_id='XXXXXXXXXXXXX', # Change the access key here
                           aws_secret_access_key='YYYYYYYYYYYYYYYYYYY') # Change the secret key here 


for i in range(50,61):
	ThingName="IotThing"+str(i)
	print("ThingName:", ThingName)
	createThing(ThingName)




































