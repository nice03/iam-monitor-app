from flask import Flask, request, jsonify
from controllers.iam_controller import IAMController
from services.iam_service import IAMService
import boto3

app = Flask(__name__)

# Create a boto3 client for IAM
aws_client = boto3.client('iam')

# Create an instance of IAMService
iam_service = IAMService(aws_client)

# Create an instance of IAMController with the IAMService instance
iam_controller = IAMController(iam_service)

@app.route('/iam/users', methods=['GET'])
def get_iam_users():
    n_hours = request.args.get('n', default=24, type=int)
    users = iam_controller.get_iam_users_with_old_keys(n_hours)
    return jsonify(users)

@app.route('/iam/unused-keys', methods=['GET'])
def get_unused_keys():
    days_unused = request.args.get('days', default=30, type=int)
    users = iam_controller.get_iam_users_with_unused_keys(days_unused)
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)