from flask import Flask, jsonify
from flask_restful import Resource, Api
import pymysql

app = Flask(__name__)
api = Api(app)

# Define your database connection
db = pymysql.connect(host="localhost", user="root", password="root", database="cse")
cursor = db.cursor()

# Define your resources
class FirstAidKitResource(Resource):
    def get(self):
        # Implement your logic to fetch data from the first_aid_kit table
        return jsonify({"message": "This is the First Aid Kit resource"})

# Add resources to the API
api.add_resource(FirstAidKitResource, '/first_aid_kit')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
