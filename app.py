from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import pymysql

app = Flask(__name__)
api = Api(app)

# Define your database connection
db = pymysql.connect(host="localhost", user="root", password="root", database="cse", autocommit=True)
cursor = db.cursor()

# Helper function to execute SQL queries
def execute_query(query, params=None, fetchone=False):
    try:
        cursor.execute(query, params)
        if fetchone:
            return cursor.fetchone()
        else:
            return cursor.fetchall()
    except pymysql.IntegrityError as e:
        # Handle integrity constraint violations (e.g., unique constraint)
        return {"error": f"Database error: {str(e)}"}, 400
    except Exception as e:
        # Handle other database errors
        return {"error": f"Database error: {str(e)}"}, 500

# Resource for first aid kits
class FirstAidKitResource(Resource):
    def get(self, kit_id=None):
        page = request.args.get('page', default=1, type=int)
        page_size = 20  # Adjust as needed

        if kit_id:
            # Retrieve a specific first aid kit by ID
            query = "SELECT * FROM first_aid_kit WHERE kit_id = %s"
            result = execute_query(query, (kit_id,), fetchone=True)
            if result:
                return jsonify({"first_aid_kit": result})
            else:
                return jsonify({"message": "First aid kit not found"}), 404
        else:
            # Retrieve all first aid kits with pagination
            offset = (page - 1) * page_size
            query = "SELECT * FROM first_aid_kit LIMIT %s OFFSET %s"
            result = execute_query(query, (page_size, offset))
            return jsonify({"first_aid_kits": result})

    def post(self):
        # Create a new first aid kit
        data = request.get_json()
        name = data.get('name')
        contents = data.get('contents')

        if not name or not contents:
            return jsonify({"error": "Name and contents are required fields"}), 400

        query = "INSERT INTO first_aid_kit (name, contents) VALUES (%s, %s)"
        execute_query(query, (name, contents))

        return jsonify({"message": "First aid kit created successfully"}), 201

    def put(self, kit_id):
        # Update a first aid kit by ID
        data = request.get_json()
        name = data.get('name')
        contents = data.get('contents')

        if not name or not contents:
            return jsonify({"error": "Name and contents are required fields"}), 400

        # Check if the first aid kit exists before updating
        existing_kit = execute_query("SELECT * FROM first_aid_kit WHERE kit_id = %s", (kit_id,), fetchone=True)
        if not existing_kit:
            return jsonify({"message": "First aid kit not found"}), 404

        query = "UPDATE first_aid_kit SET name = %s, contents = %s WHERE kit_id = %s"
        execute_query(query, (name, contents, kit_id))

        return jsonify({"message": "First aid kit updated successfully"})

    def delete(self, kit_id):
        # Delete a first aid kit by ID
        # Check if the first aid kit exists before deleting
        existing_kit = execute_query("SELECT * FROM first_aid_kit WHERE kit_id = %s", (kit_id,), fetchone=True)
        if not existing_kit:
            return jsonify({"message": "First aid kit not found"}), 404

        query = "DELETE FROM first_aid_kit WHERE kit_id = %s"
        execute_query(query, (kit_id,))

        return jsonify({"message": "First aid kit deleted successfully"})

# Add resource to the API
api.add_resource(FirstAidKitResource, '/first_aid_kit', '/first_aid_kit/<int:kit_id>')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
