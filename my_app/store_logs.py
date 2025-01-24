import os
import requests
import psycopg2
import json


# Function to get OAuth token
def get_oauth_token(client_id, client_secret, token_url):
    response = requests.post(
        token_url,
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
    )
    response.raise_for_status()
    return response.json()["access_token"]


# Function to fetch log data from the API
def fetch_log_data(api_url, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    return response.json()


# Function to process and store log data
def process_and_store_log(log_entry):
    try:
        conn = psycopg2.connect(
            database=os.environ.get("DB_URL").split("/")[-1],
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            host=os.environ.get("DB_HOST"),
            port=os.environ.get("DB_PORT"),
        )
        cur = conn.cursor()

        sql = """
            INSERT INTO auth0_logs (date, type, description, client_id, user_id, ip_address, user_agent, details)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        data = (
            log_entry["date"],
            log_entry["type"],
            log_entry["description"],
            log_entry["client_id"],
            log_entry.get("user_id"),  # Handle potential missing user_id
            log_entry["ip"],
            log_entry["user_agent"],
            json.dumps(log_entry["details"]),
        )

        cur.execute(sql, data)
        conn.commit()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)

    finally:
        if conn:
            cur.close()
            conn.close()


# Main function to get OAuth token, fetch log data, and store it
def main():
    client_id = os.environ.get("AUTH0_CLIENT_ID")
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
    token_url = f'https://{os.environ.get("AUTH0_DOMAIN")}/oauth/token'
    api_url = f'https://{os.environ.get("AUTH0_DOMAIN")}/api/v2/logs'

    token = get_oauth_token(client_id, client_secret, token_url)
    log_data = fetch_log_data(api_url, token)

    if log_data:
        for log_entry in log_data:
            process_and_store_log(log_entry)
    else:
        print("No log data found.")


if __name__ == "__main__":
    main()
