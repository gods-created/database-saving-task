from boto3 import client
from botocore.exceptions import (
    ClientError,
    ConnectionError,
    CredentialRetrievalError,
    ValidationError,
    BotoCoreError
)
from os import getenv
from os.path import basename
from exceptions import ValidationError as CustomValidationError
from loguru import logger
from io import BytesIO
from dotenv import load_dotenv
from SMTPEmail import SMTP
from smtplib import SMTPAuthenticationError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def lambda_handler(event = None, context = None) -> bool:
    load_dotenv()

    s3_client = None 
    response = False 

    try:
        environments = (
            getenv('AWS_ACCESS_KEY_ID'),
            getenv('AWS_SECRET_ACCESS_KEY'),
            getenv('S3_REGION_NAME'),
            getenv('BUCKET_NAME'),
            getenv('S3_BUCKET_PREFIX'),
            getenv('SMTP_SERVER'),
            getenv('SMTP_USERNAME'),
            getenv('SMTP_PASSWORD'),
            getenv('EMAIL')
        )

        if not all(environments):
            raise CustomValidationError('The some environment variables are absent.')
        
        s3_client = client(
            's3',
            aws_access_key_id=environments[0],
            aws_secret_access_key=environments[1],
            region_name=environments[2]
        )
    
        bucket_name = environments[3]
        prefix = environments[4]

        objects = s3_client.list_objects(
            Bucket=bucket_name,
            Prefix=prefix
        )

        contents = objects.get('Contents', [])
        if not contents:
            logger.warning(f'No files in {prefix}.')

        keys = [obj['Key'] for obj in contents]
        files = []
        
        for key in keys:
            file = BytesIO()
            s3_client.download_fileobj(bucket_name, key, file)
            file.seek(0)
            files.append((key, file))

        smtp_client = SMTP(
            SMTP_server=environments[5],
            SMTP_account=environments[6],
            SMTP_password=environments[7],
            SMTP_port=587
        )

        email = environments[8]

        mime = MIMEMultipart()
        mime['From'] = email
        mime['To'] = email
        mime['Subject'] = 'DATABASE COPIES'
        mime.attach(MIMEText('You have to download this files and replace in the project', 'plain'))
        
        for obj in files:
            key, file = obj
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{basename(key)}"')
            mime.attach(part)

        smtp_client.msg = mime
        smtp_client.send_msg()

        response = not response

    except (
        ClientError,
        ConnectionError,
        CredentialRetrievalError,
        ValidationError,
        BotoCoreError,
        CustomValidationError,
        SMTPAuthenticationError,
        Exception,
    ) as e:
        class_name = e.__class__.__name__
        exc = str(e)
        logger.error(
            f'Executing error ({class_name}): {exc}'
        )

    finally:
        if s3_client:
            s3_client.close()

    return response

if __name__ == '__main__':
    lambda_handler()