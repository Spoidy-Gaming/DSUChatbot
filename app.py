from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3

app = Flask(__name__)

def query_database(query, params=()):
    conn = sqlite3.connect('college_info.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').lower()
    response = MessagingResponse()
    msg = response.message()

    if 'course' in incoming_msg:
        courses = query_database('SELECT name, fees, image_url FROM courses')
        reply = '\n'.join([f'{name}: {fees}\nImage: {image_url}' for name, fees, image_url in courses])
        msg.body(f"Here are the available courses and fees:\n{reply}")
    elif 'hostel' in incoming_msg:
        hostels = query_database('SELECT name, fees, image_url FROM hostels')
        reply = '\n'.join([f'{name}: {fees}\nImage: {image_url}' for name, fees, image_url in hostels])
        msg.body(f"Here are the available hostels and fees:\n{reply}")
    elif 'contact' in incoming_msg or 'support' in incoming_msg:
        info = query_database("SELECT info, image_url FROM general_info WHERE category='contact'")
        msg.body(f"Contact Information:\n{info[0][0]}\nImage: {info[0][1]}")
    # Add more elif blocks for additional queries

    return str(response)

if __name__ == '__main__':
    app.run(debug=True)
