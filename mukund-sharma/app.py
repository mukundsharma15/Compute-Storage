import json, requests, boto3, io
from flask import Flask, request, render_template

app = Flask(__name__)


access_key = 'ASIAQ3S3NHNSOOJZK3VX'
secret_key = '8g07U88enRegnlyC7Ka8niqQyC/hM5xOe9sD9eoA'
token = "FwoGZXIvYXdzEAYaDDgT1XnBSAN1qmqBuyLAAdTHyssDEdHlLfY6KSlEKU+B3Ig6wCSGM2rvpjPxZI/HNwx1AmniXmBTBrt2jMS1jI6LUJXSWAZqbUzeGx7LQGkHqQ5aSLSM5h5eXF5qWYhp8G3I8K20ULn0GZK5+9wkEdflMmBzvDQSnnDnTAzvu7mr8kTondAmJBiKFcl4Oso305o9A1achuL0bGp/L4o0LuTO0Rd1U62F3530nr6offHNwJyvA2aXod4FH5kHOqlYU8uz/EPvJADrfVtN646PpSiVi4iRBjItH466pbxKhicuPg7v6h5qC5l0Wv2aKQV39S1C9OMdEbHXd75ZEvHr4/WcyYF2"

@app.route('/', methods=['POST', 'GET'])
def initiate():
        url = "http://3.88.132.229/begin"
        if request.method == 'POST':
                if request.form.get('action1') == 'INITIATE':
                        ec2_client = boto3.client("ec2", aws_access_key_id=access_key, aws_secret_access_key=secret_key, aws_session_token=token, region_name='us-east-1')
                        reservations = ec2_client.describe_instances(InstanceIds=['i-09bd8672c2657ca44']).get("Reservations")
                        for reservation in reservations:
                                for instance in reservation['Instances']:
                                        aws_ip = instance.get("PublicIpAddress")+":5000"
                        payload = json.dumps({"banner": "B00893013", "ip": aws_ip})
                        print("payload: ", payload)
                        response = requests.request("POST", url, headers={'Content-Type': 'application/json'}, data=payload)
                        return response.text
        elif request.method == 'GET':
                return render_template('index.html')


@app.route('/storedata', methods=['POST'])
def upload():
        if request.method == 'POST':
                s3_client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key, aws_session_token=token, region_name='us-east-1')
                with io.BytesIO() as f:
                        f.write(request.json.get("data").encode())
                        f.seek(0)
                        try:
                                s3_client.upload_fileobj(f, 'assignment-2-bucket', 'data.txt')
                                url = s3_client.generate_presigned_url(ClientMethod='get_object', Params={'Bucket': 'assignment-2-bucket', 'Key': 'data.txt'}, ExpiresIn=360000)
                                return json.dumps({"s3uri": url })
                        except ClientError as e:
                                return json.dumps({"s3uri":" something went wrong "})

app.run(host='0.0.0.0', port=5000)