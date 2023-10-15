import json
import psycopg2
import os
import urllib3
import json
##import boto3
from datetime import datetime

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e


    try:
        
        event["body"] = json_object = json.loads(event["body"])

        connection = connect_to_db()
        insert_event_record(connection, event)
        return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
    except Exception as e:
        print(f"Lambda execution failed: {str(e)}")
    finally:
        if connection:
            connection.close()            


def connect_to_db():
    try:

        db_user = os.environ["dbUser"] 
        db_password = os.environ["dbPassword"]#get_parameter("/manzi-mfa/postgrel/password")
        db_host = os.environ["db_host"]
        db_port = os.environ["db_port"] 
        db_name = os.environ["db_name"]

        connection = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )
        return connection
    except psycopg2.Error as e:
        raise Exception(f"Error connecting to the database: {str(e)}")

def retrieve_event_detail(event):
    try:
        http = urllib3.PoolManager()
        api_host = 'https://manzi-mfa.mongulu.cm/index.php/api/v1'
        api_key = os.environ["EASY_APPOINTMENTS_KEY"]
        # Headers
        headers = {
        'Authorization': f'Bearer {api_key}',
        }
        # Appointment ID
        appointment_id = event["body"]["payload"]["id"]
        
        start_date = event["body"]["payload"]["start_datetime"].replace(" ","T")
        end_date = event["body"]["payload"]["end_datetime"].replace(" ","T")
        
        # Get appointment details
        appointment_url = f'{api_host}/appointments/{appointment_id}'
        response = http.request('GET', appointment_url, headers=headers)
        response_data = json.loads(response.data.decode('utf-8'))

        # Get service title
        service_id = response_data['serviceId']
        service_url = f'{api_host}/services/{service_id}'
        response = http.request('GET', service_url, headers=headers)
        service = json.loads(response.data.decode('utf-8'))
        
        # Get provider name
        provider_id = response_data['providerId']
        provider_url = f'{api_host}/providers/{provider_id}'
        response = http.request('GET', provider_url, headers=headers)
        provider = json.loads(response.data.decode('utf-8'))
        
        # Get customer info
        customer_id = response_data['customerId']
        customer_url = f'{api_host}/customers/{customer_id}'
        response = http.request('GET', customer_url, headers=headers)
        customer = json.loads(response.data.decode('utf-8'))


        return {
            "customer_email": customer['email'],
            "customer_name": customer["firstName"] + " " + customer["lastName"],
            "service_name": service["name"],
            "provider_name": provider["firstName"] + " " + provider["lastName"],
            "provider_email": provider["email"],
            "start_date": start_date,
            "end_date": end_date
        }
    except urllib3.exceptions.HTTPError as e:
        return f'HTTPError: {e}'


def insert_event_record(connection, event):
    try:
        current_timestamp = datetime.now()
        cursor = connection.cursor()
        event_details = retrieve_event_detail(event)
        record_to_insert = (
           event["body"]["action"],
           current_timestamp,
           event_details["customer_email"],
           event_details["customer_name"],
           event_details["service_name"],
           event_details["provider_name"],
           event_details["provider_email"],
           event_details["start_date"],
           event_details["end_date"]
        )

        print(record_to_insert)
        # Define the PostgreSQL INSERT query
        postgres_insert_query = """ INSERT INTO manzi_mfa.user_events(
             action,created_at, customer_email, customer_name, service_name, provider_name, provider_email, start_date,end_date)
            VALUES (%s, %s,  %s, %s, %s, %s, %s, %s, %s)"""                         
        print(postgres_insert_query.format(record_to_insert))
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into mobile table")
        
    except (Exception, psycopg2.Error) as error:
        raise Exception(f"Failed to insert record into user_events table: {str(error)}")
    finally:
        if cursor:
            cursor.close()


