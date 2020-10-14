import json, boto3, argparse, os

#########################
def main():
    parser = argparse.ArgumentParser(description='post a message to a topic in AWS SNS. It gets the ARN for the AWS TOPIC from the environment variable ARN, the access key from ACCESS_KEY and secret key from SECRET_KEY (also environment variables). Note that the subject is ignored if the subscriber is type SMS.')
    parser.add_argument('sub',action='store',type=str,help='SNS subject')
    parser.add_argument('msg',action='store',type=str,help='SNS message')
    args = parser.parse_args()
    msg = args.msg
    sub = args.sub

    return post(msg,sub)

#########################
def post(msg,subject):

    topic = acc = sec = None
    try:
        topic = os.environ['ARN']
        acc = os.environ['ACCESS_KEY']
        sec = os.environ['SECRET_KEY']
    except: 
        print("Error: ARN, ACCESS_KEY, and SECRET_KEY environment variables must be set")
        return

    client = boto3.client(
        'sns',
        region_name='us-west-1',
        aws_access_key_id=acc,
        aws_secret_access_key=sec
    )
    print(topic,client)
    response = client.publish(
        TopicArn=topic,
        Message=json.dumps({'default': msg,
                            'sms': msg,
                            'email': msg}),
        Subject=subject,
        MessageStructure='json'
    )
    if 'ResponseMetadata' in response:
        res = response['ResponseMetadata']
        if 'HTTPStatusCode' in res:
            status_code = res['HTTPStatusCode']
            if status_code != 200:
                print("postmsg:post Error: non-200 response: {}".format(response))
    return response

#########################
if __name__ == "__main__":
    main()

