import json, requests, boto3, io
from flask import Flask, request, render_template

app = Flask(__name__)


access_key = ''
secret_key = ''
token = ""

@app.route('/', methods=['POST', 'GET'])
def initiate():
        url = "http://IP/begin"
        if request.method == 'POST':
                if request.form.get('action1') == 'INITIATE':
                        ec2_client = boto3.client("ec2", aws_access_key_id=access_key, aws_secret_access_key=secret_key, aws_session_token=token, region_name='us-east-1')
                        reservations = ec2_client.describe_instances(InstanceIds=['i-']).get("Reservations")
                        for reservation in reservations:
                                for instance in reservation['Instances']:
                                        aws_ip = instance.get("PublicIpAddress")+":5000"
                        payload = json.dumps({"banner": "", "ip": aws_ip})
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
