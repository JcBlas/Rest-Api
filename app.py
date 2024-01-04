from flask import Flask, jsonify, request, make_response
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'cse'

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Route to get all first aid kits
@app.route('/api/first_aid_kits', methods=['GET'])
def get_first_aid_kits():
    try:
        # Connect to the database
        cur = mysql.connection.cursor()

        # Execute the query to fetch all first aid kits
        cur.execute("SELECT * FROM first_aid_kit")

        # Fetch all results
        result = cur.fetchall()

        # Close the cursor
        cur.close()

        # Return the result in JSON format
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})       

# Route to create a new first aid kit
@app.route('/api/first_aid_kits', methods=['POST'])
def create_first_aid_kit():
    try:
        info = request.get_json()
        First_Aid_Kit_details = info.get("First_Aid_Kit_details")
        Location_id = info.get("Location_id")
        cur = mysql.connection.cursor()
        cur.execute(
            """INSERT INTO cse.first_aid_kit
            (First_Aid_Kit_details, Location_id) 
            VALUES (%s, %s)""",
            (First_Aid_Kit_details, Location_id)
        )
        mysql.connection.commit()
        rows_affected = cur.rowcount
        cur.close()

        return make_response(
            jsonify({"message": "New first aid kit created successfully", "rows_affected": rows_affected}),
            201
        )

    except Exception as e:
        print("Error adding first aid kit:", e)
        return jsonify({"error": str(e)}), 500

# Route to update a first aid kit
@app.route('/api/first_aid_kits/<int:first_aid_kit_id>', methods=['PUT'])
def update_first_aid_kit(first_aid_kit_id):
    try:
        cur = mysql.connection.cursor()
        info = request.get_json()
        First_Aid_Kit_details = info.get("First_Aid_Kit_details")
        Location_id = info.get("Location_id")
        cur.execute(
            """ UPDATE first_aid_kit SET 
            First_Aid_Kit_details = %s, Location_id = %s
            WHERE First_Aid_Kit_id = %s """,
            (First_Aid_Kit_details, Location_id, first_aid_kit_id)
        )
        mysql.connection.commit()
        rows_affected = cur.rowcount
        cur.close()
        return make_response(
            jsonify(
                {"message": f"First aid kit {first_aid_kit_id} updated successfully", "rows_affected": rows_affected}
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# Route to delete a first aid kit
@app.route('/api/first_aid_kits/<int:first_aid_kit_id>', methods=['DELETE'])
def delete_first_aid_kit(first_aid_kit_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute(""" DELETE FROM first_aid_kit where First_Aid_Kit_id = %s """, (first_aid_kit_id,))
        mysql.connection.commit()
        rows_affected = cur.rowcount
        cur.close()
        return make_response(
            jsonify(
                {"message": f"First aid kit {first_aid_kit_id} deleted successfully", "rows_affected": rows_affected}
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
