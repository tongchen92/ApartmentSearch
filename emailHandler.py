import boto3
from botocore.exceptions import ClientError

# Replace sender@example.com with your "From" address.
# This address must be verified with Amazon SES.
SENDER = "Apartment Searcher <tongchen92@gmail.com>"

# Replace recipient@example.com with a "To" address. If your account 
# is still in the sandbox, this address must be verified.
RECIPIENT = "dyr0916@gmail.com"

# Specify a configuration set. If you do not want to use a configuration
# set, comment the following variable, and the 
# ConfigurationSetName=CONFIGURATION_SET argument below.
# CONFIGURATION_SET = "ConfigSet"

# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
AWS_REGION = "us-east-2"

# The subject line for the email.
SUBJECT = "New Apartment"

# The email body for recipients with non-HTML email clients.
BODY_TEXT = ("Amazon SES Test (Python)\r\n"
             "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)."
            )
            
# The character encoding for the email.
CHARSET = "UTF-8"

# Create a new SES resource and specify a region.
client = boto3.client('ses',region_name=AWS_REGION)

def sendEmail(apartment):
    BODY_HTML = """
    <html>
    <head></head>
    <body>
    <h1>Salix Junanita New Apartment</h1>
    <p>Apartment Id: {ApartmentId}</p>
    <p>Description: {Description}</p>
    <p>Early available date: {earlyDate}</p>
    <p>Max move in date: {maxDate}</p>
    <p>Description: {Description}</p>
    <p>Rent: {Rent}</p>
    </body>
    </html>
                """.format(ApartmentId = apartment['data-apartment-number'], 
                           earlyDate=apartment['data-internal-available-date'],
                           maxDate=apartment['data-max-move-in-date'],
                           Description = apartment['data-floorplan-description'],
                           Rent = apartment.find('span', {'class':'rent_amount'}).get_text()
                           )
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])