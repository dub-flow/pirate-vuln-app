from flask import Flask, request, send_from_directory, jsonify, render_template
from werkzeug.utils import safe_join
import os
import subprocess

app = Flask(__name__)

files_dir = './pirates'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pirates', defaults={'filename': ''})
@app.route('/pirates/<path:filename>')
def serve_files(filename):
    # Check if filename is not provided, show directory contents
    if not filename:
        try:
            # List directory contents
            files = os.listdir(files_dir)
            return jsonify(files)
        except OSError as e:
            # Handle error if directory is not found or other OS errors
            return jsonify({"error": str(e)}), 404
    else:
        # Serve the file from directory
        try:
            # Ensure the filename is safe to use
            safe_filename = safe_join(files_dir, filename)
            if not os.path.isfile(safe_filename):
                return jsonify({"error": "File not found"}), 404
            return send_from_directory(files_dir, filename)
        except FileNotFoundError:
            return jsonify({"error": "File not found"}), 404

@app.route('/reset-password', methods=['POST'])
def reset_password():
    # Simulating a password reset by email (vulnerable to host header attack)
    host_header = request.headers['Host']
    reset_link = f'http://{host_header}/reset-confirm'
    return f'Password reset link (check your email!): {reset_link}'

@app.route('/reset-confirm')
def reset_confirm():
    return 'Password reset confirmed!'

@app.route('/loot')
def loot():
    # Get the 'id' query parameter from the request
    loot_id = request.args.get('id')

    # Hardcoded loot IDs with pirate language responses
    loot_ids = {
        '123456789': 'Ye got not loot',
        '1adsasgvagdad31asdart1235112412515113123123': 'Ye be rich!'
    }

    # Check if the loot_id exists in the loot_ids dictionary
    if loot_id in loot_ids:
        return loot_ids[loot_id]
    else:
        return "No loot here, try 123456789"


@app.route('/admin')
def admin():
    # Check if sessionId is provided in the query parameters
    session_id = request.args.get('sessionId')
    if session_id == '12345':
        return 'Arrrr welcome aboard, Cap'
    else:
        return 'Provide \'?sessionId\' or ye be walkin\' the plank! Access be denied! Arrrr!'

@app.route('/admin-cmd', methods=['POST'])
def admin_cmd():
    # Check if sessionId is provided in the query parameters
    session_id = request.args.get('sessionId')
    
    # Check if the session ID is valid
    if session_id == '12345':
        # Get the command from the request data
        data = request.json
        command = data.get('command')
        print(f"Executing command: {command}")

        try:
            # Execute the command
            result = subprocess.check_output(command, shell=True)
            if result is not None:
                return result.decode('utf-8')
            else:
                return "Command executed successfully, but no output."
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {str(e)}"
        except Exception as e:
            return f"Unknown error: {str(e)}"
    else:
        return 'Access denied'
    
@app.route('/change-password', methods=['POST'])
def change_password():
    # Check if sessionId is provided in the query parameters
    session_id = request.args.get('sessionId')
    
    # Check if the session ID is valid
    if session_id == '12345':
        # Get the new password from the request data
        new_password = request.form.get('new_password')

        # Logic to change the password (you may implement your own logic here)
        # For example, you can store the password securely in a database
        # or update the password for the user associated with the session ID
        # For demonstration purposes, let's just print the new password
        print(f"New password: {new_password}")

        return 'Password changed successfully'
    else:
        return 'Access denied'

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')