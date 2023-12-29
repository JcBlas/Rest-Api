from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import pymysql

app = Flask(__name__)
api = Api(app)

# Define your database connection
db = pymysql.connect(host="localhost", user="root", password="root", database="cse")
cursor = db.cursor()

# Helper function to execute SQL queries
def execute_query(query, params=None, fetchone=False):
    cursor.execute(query, params)
    if fetchone:
        return cursor.fetchone()
    else:
        return cursor.fetchall()

# Resource for first aid kits
class FirstAidKitResource(Resource):
    def get(self, kit_id=None):
        if kit_id:
            # Retrieve a specific first aid kit by ID
            query = "SELECT * FROM first_aid_kit WHERE kit_id = %s"
            result = execute_query(query, (kit_id,), fetchone=True)
            if result:
                return jsonify({"first_aid_kit": result})
            else:
                return jsonify({"message": "First aid kit not found"}), 404
        else:
            # Retrieve all first aid kits
            query = "SELECT * FROM first_aid_kit"
            result = execute_query(query)
            return jsonify({"first_aid_kits": result})

    def post(self):
        # Create a new first aid kit
        data = request.get_json()
        name = data.get('name')
        contents = data.get('contents')

        query = "INSERT INTO first_aid_kit (name, contents) VALUES (%s, %s)"
        execute_query(query, (name, contents))
        db.commit()

        return jsonify({"message": "First aid kit created successfully"}), 201

    def put(self, kit_id):
        # Update a first aid kit by ID
        data = request.get_json()
        name = data.get('name')
        contents = data.get('contents')

        query = "UPDATE first_aid_kit SET name = %s, contents = %s WHERE kit_id = %s"
        execute_query(query, (name, contents, kit_id))
        db.commit()

        return jsonify({"message": "First aid kit updated successfully"})

    def delete(self, kit_id):
        # Delete a first aid kit by ID
        query = "DELETE FROM first_aid_kit WHERE kit_id = %s"
        execute_query(query, (kit_id,))
        db.commit()

        return jsonify({"message": "First aid kit deleted successfully"})

# Add resource to the API
api.add_resource(FirstAidKitResource, '/first_aid_kit', '/first_aid_kit/<int:kit_id>')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
