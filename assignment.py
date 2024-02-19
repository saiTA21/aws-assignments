from flask import Flask, jsonify
import boto3
import logging

app = Flask(__name__)

# AWS S3 Configuration
bucket_name = 'tiger-devops-pg1'  # The name of your bucket

# Enable logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/home/<user_name>/<folder_name>/')
def list_files_in_folder(user_name, folder_name):
    # Log the request for debugging purposes
    app.logger.debug(f'Request to list files in folder: {folder_name}')

    # Set up AWS S3 client
    s3 = boto3.client('s3')

    try:
        # Combine user name and folder name to form the prefix
        prefix = f"home/{user_name}/{folder_name}/"

        # Use the list_objects_v2 method to get objects in the specified folder
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

        filenames = []
        # Check if 'Contents' key is in the response
        if 'Contents' in response:
            # Extract file names from the objects in the specified folder
            for obj in response['Contents']:
                key = obj['Key']
                # Extract filename by splitting the key by '/' and getting the last part
                filename = key.split('/')[-1]
                if filename:  # Ensure we don't add empty filenames (which can happen if the key ends with '/')
                    filenames.append(filename)
        
        # Log the response for debugging
        app.logger.debug(f'Response from S3: {response}')

        # Return the list of filenames as a JSON response
        return jsonify(filenames)
    except Exception as e:
        app.logger.error(f"Error listing files in folder '{folder_name}': {e}")
        return jsonify({"error": f"Error listing files in folder: {e}"}), 500

if __name__ == "__main__":
    # Start the Flask app on port 80 (HTTP standard port)
    app.run(host='0.0.0.0', port=8085, debug=True)