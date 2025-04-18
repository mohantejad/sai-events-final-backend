import boto3

client = boto3.client(
    'ses',
    region_name='ap-southeast-2',
    aws_access_key_id='AKIAXYKJSPFBVCTBLND6',
    aws_secret_access_key='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'
)

response = client.send_email(
    Source='mohantejad@proton.me',
    Destination={'ToAddresses': ['mohantejad15@gmail.com']},
    Message={
        'Subject': {'Data': 'Test Email'},
        'Body': {'Text': {'Data': 'This is a test email.'}}
    }
)
