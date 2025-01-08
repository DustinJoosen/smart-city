import sqlite3
import datetime
import requests

class Notification:
    def __init__(self):
        self.db_file = 'notifications.db'
        self.api_url = 'http://localhost:5000/notifications'  # Replace with your API endpoint

    def add_notification(self):
        # Get the current timestamp
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        notification_message = f"Doorbell pressed at {current_time}"
        print('noti')
        # Insert the notification into the database
        self._insert_notification(notification_message, current_time)

        # Call the API endpoint (you can adjust the payload as needed)
        self._call_api(notification_message, current_time)

    def _insert_notification(self, message: str, timestamp: str):
        # Connect to the SQLite database
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Insert the new notification into the database
        cursor.execute('''
            INSERT INTO notifications (message, timestamp)
            VALUES (?, ?)
        ''', (message, timestamp))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

    def _call_api(self, message: str, timestamp: str):
        # Prepare the payload to send to the API
        payload = {
            'message': message,
            'timestamp': timestamp
        }

        try:
            # Send a POST request to the API endpoint
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
        except requests.exceptions.RequestException as e:
            print(f"Error calling API: {e}")

    def get_notifications(self):
        # Connect to the SQLite database
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # Retrieve all notifications
        cursor.execute('SELECT message, timestamp FROM notifications ORDER BY timestamp DESC')
        notifications = cursor.fetchall()

        # Close the connection
        conn.close()

        # Return the list of notifications
        return notifications
