from flask import Flask, Response, render_template,send_file
import subprocess
import time
from datetime import datetime
import RPi.GPIO as GPIO
from notification import Notification  # Import the Notification class
from threading import Thread
import jsonify
import sqlite3
import statistics
import matplotlib.pyplot as plt
from io import BytesIO
from collections import Counter
import base64  # Make sure base64 is imported
import pandas as pd
from sklearn.linear_model import LinearRegression
app = Flask(__name__)

# Initialize Notification and Buzzer
notif = Notification()

# Function to generate the video feed
def generate_video_feed():
    while True:
        # Capture a single frame using libcamera-still
        subprocess.run(
            [
                'libcamera-still',
                '--width', '640',  # Reduce resolution for better performance
                '--height', '480',
                '--output', '/tmp/frame.jpg',
                '--timeout', '1',  # Capture a frame as quickly as possible
                '--nopreview'
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        # Read the captured image
        with open('/tmp/frame.jpg', 'rb') as img_file:
            img_data = img_file.read()

        # Yield the image as a part of the MJPEG stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + img_data + b'\r\n')

        # Adjust the frame rate if needed
        time.sleep(0.1)

# Flask route to serve the video feed
@app.route('/video_feed')
def video_feed():
    return Response(generate_video_feed(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Function to add a notification with the current timestamp

def calculate_statistics(notifications):
    # Initialize a dictionary with default value 0 for each hour (0-23)
    hour_counts = {hour: 0 for hour in range(24)}

    # Loop through the notifications and count how many notifications occurred for each hour
    for notification in notifications:
        timestamp = datetime.strptime(notification[1], "%Y-%m-%d %H:%M:%S")
        hour = timestamp.hour
        hour_counts[hour] += 1

    # Calculate the mean as total notifications divided by 24
    total_notifications = sum(hour_counts.values())
    mean = total_notifications / 24

    # Calculate median and mode based on notification counts
    counts = list(hour_counts.values())

    try:
        median = statistics.median(counts)
    except statistics.StatisticsError:
        median = None

    try:
        mode = statistics.mode(counts)
    except statistics.StatisticsError:
        mode = None

    # Calculate the number of hours that had at least one notification
    active_hours = sum(1 for count in counts if count > 0)

    # Return mean, median, mode, active hours, and hour counts
    return mean, median, mode, active_hours, hour_counts

# Function to create a graph of notifications per hour and return it as an image
def create_notifications_graph(hour_counts):
    # Extract the count of notifications for each hour (0-23)
    hour_labels = list(hour_counts.keys())  # hours (0-23)
    hour_values = list(hour_counts.values())  # number of notifications per hour

    # Create a bar graph
    plt.bar(hour_labels, hour_values, color='skyblue')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Notifications')
    plt.title('Notifications per Hour')
    plt.xticks(hour_labels)

    # Save the figure to a BytesIO object and return it as an image
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image as base64 and return the encoded string
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    return img_base64

def add_notification():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    notification_message = f"Doorbell pressed at {current_time}"

    # Append the notification to the file (or keep track in memory if needed)
    notif.add_notification()

def get_notifications():
    # Connect to the SQLite database
    conn = sqlite3.connect('notifications.db')
    cursor = conn.cursor()

    # Retrieve all notifications ordered by timestamp
    cursor.execute('SELECT message, timestamp FROM notifications ORDER BY timestamp DESC')
    notifications = cursor.fetchall()

    # Close the connection
    conn.close()

    # Return the list of notifications
    return notifications

@app.route('/notifications', methods=["GET"])
def route_get_notifications():
    # Get the list of notifications from the database
    notifications = get_notifications()
    print(notifications)
    # Prepare the notifications data as a list of dictionaries
    

    # Return the notifications as JSON
    return jsonify(notifications)

# Main page with camera feed and notifications
@app.route('/')
def index():
    # Read the notifications from the file
    notifications = notif.get_notifications()
    mean, median, mode, hours, hour_counts = calculate_statistics(notifications)
    graph_img_base64 = create_notifications_graph(hour_counts)
    recent_notifications = notifications[:5]  # Get the last 5 notifications
    
    df = pd.DataFrame(list(hour_counts.items()), columns=['hour', 'notifications'])

    # Linear Regression Model
    X = df[['hour']]
    y = df['notifications']

    model = LinearRegression()
    model.fit(X, y)

    # Get the current hour
    current_hour = datetime.now().hour

    # Predict total notifications by the end of the day (24 hours)
    predicted_total_notifications = int(model.predict([[24]])[0])

    # Predict notifications based on the current hour
    current_prediction = int(model.predict([[current_hour]])[0])
    print(current_prediction)
    return render_template(
        'index.html',
        recent_notifications=recent_notifications,
        all_notifications=notifications,
        mean=round(mean, 2),
        median=round(median, 2),
        mode=round(mode, 2),
        graph_img_base64=graph_img_base64,
        prediction=current_prediction
        )

# Buzzer class to handle doorbell press

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
