import json
from datetime import datetime
import psycopg2
from datetime import datetime, timedelta
import requests
import os 

MONGULU_NUMBER = os.environ.get("MONGULU_NUMBER", '')
API_KEY_HTTPSMS =  os.environ.get("API_KEY_HTTPSMS", '')

def connect_to_db():
    try:

        db_user = os.environ.get("dbUser", "") 
        db_password = os.environ.get("dbPassword", "")
        db_host = os.environ.get("dbHost", "")
        db_port = os.environ.get("dbPort", "")
        db_name = os.environ.get("dbName", "")

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


def get_users_to_notify(connection):
    
    
    try:
        with connection.cursor() as cur:

            # Get the current date and time
            current_time = datetime.now()

            # Define the timedelta for two hours
            delta_hours = timedelta(hours=2)

            # SQL Query to select rows where the datetime column is within +/- 2 hours of the current time
            query = """
            SELECT *
            FROM manzi_mfa.user_events
            WHERE start_date BETWEEN %s AND %s;
            """

            # Calculate the time range
            time_lower_bound = current_time + 1*delta_hours
            time_upper_bound = current_time + 3*delta_hours

            # Execute the query with the time range as parameters
            cur.execute(query, (time_lower_bound, time_upper_bound))

            # Fetch all the results
            users = cur.fetchall()

            # Print the results or process them as needed
            for user in users:
                print(user)


            print(len(users), " persons successfully notify")
            return users     
    except (Exception, psycopg2.Error) as error:
        raise Exception(f"Failed to select from  user_events table: {str(error)}")
    finally:
        if cur:
            cur.close()
        if connection:
            connection.close()    
            
def notify_user(user):
            
        url = 'https://api.httpsms.com/v1/messages/send'

        headers = {
            'x-api-key': API_KEY_HTTPSMS,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        payload = {
            "content": "Hello ,Vous avez une réunion meet pour la revue de votre dans moins de 2h  \n L'équipe Mongulu",
            "from": MONGULU_NUMBER,
            "to": "+"+str(user[-1])
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        print(response.json())
    
def notify_users(users):
        for user in users :
            notify_user(user)


if __name__ == "__main__":
    # Code in this block will only run if this script is executed directly, not when imported as a module
    connection = connect_to_db()
    users_to_notify = get_users_to_notify(connection)
    notify_users(users_to_notify)