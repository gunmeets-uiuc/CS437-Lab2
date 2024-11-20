import boto3
import json
import random
import string

################################################### Parameters for Thing
thingArn = 'arn:aws:iot:us-east-2:438465164072:thinggroup/Things_Gr01'
thingGroupName = 'Things_Gr01'
thingId = ''
# thingName = ''.join([random.choice('ThingsWithBoto' + string.digits) for n in range(25)])
defaultPolicyName = 'iot_policy_01'
###################################################


def createThing(thingName):
    global thingClient
    thingResponse = thingClient.create_thing(
      thingName=thingName
      )
    data = json.loads(json.dumps(thingResponse, sort_keys=False, indent=4))
    for element in data: 
        if element == 'thingArn':
            thingArn = data['thingArn']
        elif element == 'thingId':
            thingId = data['thingId']
        createCertificate(thingName)


def createCertificate(thingName):
	global thingClient
	certResponse = thingClient.create_keys_and_certificate(
			setAsActive=True
	)
	data = json.loads(json.dumps(certResponse, sort_keys=False, indent=4))
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
							
	with open(thingName + '_public.key', 'w') as outfile:
			outfile.write(PublicKey)
	with open(thingName + '_private.key', 'w') as outfile:
			outfile.write(PrivateKey)
	with open(thingName + '_cert.pem', 'w') as outfile:
			outfile.write(certificatePem)

	response = thingClient.attach_policy(
			policyName=defaultPolicyName,
			target=certificateArn
	)
	response = thingClient.attach_thing_principal(
			thingName=thingName,
			principal=certificateArn
	)

thingClient = boto3.client(
    'iot',
    aws_access_key_id='AKIAWMFUPOMUFYQENSMI',
    aws_secret_access_key='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',
    region_name = 'us-east-2',
)

for i in range(10,20):
    thingName = "thing_"+str(i)
    createThing(thingName)
    response = thingClient.add_thing_to_thing_group(
    thingGroupName=thingGroupName,
    # thingGroupArn='string',
    thingName=thingName,
    # thingArn=thingArn,
    )
