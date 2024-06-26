from flask import Flask, request, send_from_directory, jsonify, render_template
from werkzeug.utils import safe_join
import os
import subprocess
from saxonche import PySaxonProcessor

app = Flask(__name__, static_url_path='/static', static_folder='static')

files_dir = './pirates'

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/xslt')
def xslt_template():
    return render_template('xslt.html')

@app.route('/admin-command')
def admin_command_template():
    return render_template('admin_command.html')

@app.route('/loot-form')
def loot_form_template():
    return render_template('loot_form.html')

@app.route('/password-reset-form')
def password_reset_form_template():
    return render_template('password_reset_form.html')

@app.route('/admin-access')
def admin_access_template():
    return render_template('admin_access.html')

@app.route('/change-password-form')
def change_password_template():
    return render_template('change_password.html')

@app.route('/pirates', defaults={'filename': ''})
@app.route('/pirates/<path:filename>')
def serve_files(filename):
    # If filename is not provided, show the directory listing
    if not filename:
        try:
            files = os.listdir(files_dir)
            return jsonify(files)
        except OSError as e:
            return jsonify({"error": str(e)}), 404
    else:
        try:
            safe_filename = safe_join(files_dir, filename)
            if not os.path.isfile(safe_filename):
                return jsonify({"error": "File not found"}), 404
            return send_from_directory(files_dir, filename)
        except FileNotFoundError:
            return jsonify({"error": "File not found"}), 404

@app.route('/reset-password', methods=['POST'])
def reset_password():
    host_header = request.headers['Host']
    reset_link = f'http://{host_header}/reset-confirm?token=131rasdadsagfafvsbvafdasd'
    return f'Password reset link (check your email!): {reset_link}'

@app.route('/reset-confirm')
def reset_confirm():
    return 'Password reset confirmed!'

@app.route('/loot')
def loot():
    loot_id = request.args.get('id')

    loot_ids = {
        '123456789': 'Ye got not loot',
        '1adsasgvagdad31asdart1235112412515113123123': 'Ye be rich!'
    }

    if loot_id in loot_ids:
        return loot_ids[loot_id]
    else:
        return "No loot here, try 123456789"

@app.route('/admin')
def admin():
    session_id = request.args.get('sessionId')
    if session_id == '12345':
        return 'Arrrr welcome aboard, Cap'
    else:
        return 'Ye be walkin\' the plank! Access be denied! Arrrr!'

@app.route('/admin-cmd', methods=['POST'])
def admin_cmd():
    session_id = request.args.get('sessionId')
    
    #  Simulated login
    if session_id == '12345':
        data = request.json
        command = data.get('command')
        print(f"Executing command: {command}")

        try:
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
    data = request.json
    email = data.get('email')
    new_password = data.get('new_password')
    
    # Check if the email is admin@pirate-bay.com
    if email == 'admin@pirate-bay.com':
        return f'Ye password has been changed to \'{new_password}\', matey!'
    else:
        return 'Access denied. Walk the plank, scallywag!'

@app.route('/parse-xslt', methods=['POST'])
def parse_xslt():
    try:
        # Check if the request contains a file part
        if 'xslt_file' not in request.files:
            return 'No file part', 400
        
        xslt_file = request.files['xslt_file']
        xslt_content = xslt_file.read()

        # Create a Saxon processor
        with PySaxonProcessor(license=False) as proc:
            # Parse the XSLT content
            xsltproc = proc.new_xslt30_processor()
            xsltproc.set_cwd('.')
            transformer = xsltproc.compile_stylesheet(stylesheet_text=xslt_content.decode())

            # Read the XML file to apply the XSLT transformation
            with open('./resources/some.xml', 'rb') as xml_file:
                xml_content = xml_file.read()

            # Parse the XML content
            document = proc.parse_xml(xml_text=xml_content.decode('utf-8'))

            # Apply the XSLT transformation to the XML
            output = transformer.transform_to_string(xdm_node=document)

            if not output:
                return "Successful but no output"

            return output
    except Exception as e:
        print(f"Error processing XSLT: {str(e)}")
        return str(e), 500
    
if __name__ == '__main__':
    # Check if running in Docker
    if os.getenv('DOCKER_ENVIRONMENT') == 'true':
        # If running in Docker, listen on all interfaces
        app.run(debug=True, host='0.0.0.0')
    else:
        # If not running in Docker, listen on localhost
        app.run(debug=True, host='127.0.0.1')
