from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_mysqldb import MySQL

app = Flask(__name__)
api = Api(app)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'cse'

mysql = MySQL(app)

class UserResource(Resource):
    def get(self, user_id):
        # Retrieve user from the database based on user_id
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            # Return user data in JSON format
            return jsonify({'id': user[0], 'username': user[1], 'email': user[2]})
        else:
            return jsonify({'message': 'User not found'}), 404

    def post(self):
        # Create a new user based on data from the request
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (username, email))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'User created successfully'})

    def put(self, user_id):
        # Update user based on user_id and data from the request
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE users SET username = %s, email = %s WHERE id = %s", (username, email, user_id))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'User updated successfully'})

    def delete(self, user_id):
        # Delete user based on user_id
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': 'User deleted successfully'})

api.add_resource(UserResource, '/user/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
