from flask import Flask, Response, make_response, jsonify, request, send_file, render_template
from flask_mysqldb import MySQL
import dicttoxml

app = Flask(_name_)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "cse"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)
print(mysql)

def generate_xml_response(results):
    xml_data = dicttoxml.dicttoxml(results)
    return Response(xml_data, mimetype='text/xml')

def data_fetch(query):
    try:
        format_requested = request.args.get('format') 
        cur = mysql.connection.cursor()
        cur.execute(query)
        
        results = cur.fetchall()
        
        if format_requested and format_requested.lower() == 'xml':
            xml_data = generate_xml_response(results)
            return xml_data
        else:
            return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()

@app.route('/athlete', methods=['GET'])
def get_employees():
    query = "SELECT * FROM mydb.athlete"
    result = data_fetch(query)
    return result

@app.route('/athlete/<int:id>', methods=['GET'])
def get_athlete__by_id(id):
    query = f"SELECT * FROM mydb.athlete WHERE athlete_id = {id}"
    result = data_fetch(query)
    return result

@app.route('/club', methods=['GET'])
def get_club():
    query = "SELECT * FROM mydb.club"
    result = data_fetch(query)
    return result

@app.route('/club/<int:id>', methods=['GET'])
def get_club__by_id(id):
    query = f"SELECT * FROM mydb.club WHERE club_id = {id}"
    result = data_fetch(query)
    return result

@app.route('/event_series', methods=['GET'])
def get_event_series():
    query = "SELECT * FROM mydb.event_series"
    result = data_fetch(query)
    return result

@app.route('/club/<int:id>', methods=['GET'])
def get_event_series__by_id(id):
    query = f"SELECT * FROM mydb.event_series WHERE series_number = {id}"
    result = data_fetch(query)
    return result

#Athlete CRUD
@app.route("/athlete", methods=["POST"])
def add_athlete():
   
        cur = mysql.connection.cursor()
        info = request.get_json()
        athlete_id = info["athlete_id"]
        athlete_firstname = info["athlete_firstname"]
        athlete_surname = info["athlete_surname"]
        athlete_otherdetails = info["athlete_otherdetails"]
        gender_gender_code = info["gender_gender_code"]
        club_club_id = info["club_club_id"]
        event_series_series_number = info ["event_series_series_number"]
        category_category_code = info ["category_category_code"]

        cur.execute(
            """ INSERT INTO athlete (athlete_id, athlete_firstname, athlete_surname, athlete_otherdetails, gender_gender_code, club_club_id, event_series_series_number, category_category_code) 
            VALUE (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (athlete_id, athlete_firstname, athlete_surname, athlete_otherdetails, gender_gender_code, club_club_id, event_series_series_number, category_category_code),
        )
        mysql.connection.commit()
        print("row(s) affected :{}".format(cur.rowcount))
        rows_affected = cur.rowcount
        cur.close()
        return make_response(
            jsonify(
                {"message": "athlete added successfully", "rows_affected": rows_affected}
            ),
            201,
        )

@app.route("/athlete/<int:id>", methods=["PUT"])
def update_athlete(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    athlete_id = info["athlete_id"]
    athlete_firstname = info["athlete_firstname"]
    athlete_surname = info["athlete_surname"]
    athlete_otherdetails = info["athlete_otherdetails"]
    gender_gender_code = info["gender_gender_code"]
    club_club_id = info["club_club_id"]
    event_series_series_number = info ["event_series_series_number"]
    category_category_code = info ["category_category_code"]
    cur.execute(
        """ UPDATE athlete SET athlete_id = %s, athlete_firstname = %s, athlete_surname = %s, athlete_otherdetails = %s, gender_gender_code = %s
         club_club_id = %s, event_series_series_number = %s, category_category_code = %s WHERE athlete_id = %s """,
        (athlete_id, athlete_firstname, athlete_surname, athlete_otherdetails, gender_gender_code, club_club_id, event_series_series_number, category_category_code),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "athlete updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )

@app.route("/athlete/<int:id>", methods=["DELETE"])
def delete_athlete(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM athlete where athlete_id = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "athlete deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )
#Club CRUD
@app.route("/club", methods=["POST"])
def add_club():
   
        cur = mysql.connection.cursor()
        info = request.get_json()
        club_id = info["club_id"]
        club_name = info["club_name"]
        club_location = info["club_location"]
        
        cur.execute(
            """ INSERT INTO club (first_name, last_name) VALUE (%s, %s, %s)""",
            (club_id, club_name, club_location, ),
        )
        mysql.connection.commit()
        print("row(s) affected :{}".format(cur.rowcount))
        rows_affected = cur.rowcount
        cur.close()
        return make_response(
            jsonify(
                {"message": "club added successfully", "rows_affected": rows_affected}
            ),
            201,
        )

@app.route("/club/<int:id>", methods=["PUT"])
def update_club(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    club_id = info["club_id"]
    club_name = info["club_name"]
    club_location = info["club_location"]
    
    cur.execute(
        """ UPDATE club SET club_id = %s, club_name = %s, club_location = %s WHERE club_id = %s """,
        (club_id, club_name, club_location,),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "club updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )
@app.route("/club/<int:id>", methods=["DELETE"])
def delete_club(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM club where club_id = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "club deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )

#event_series CRUD
@app.route("/event_series", methods=["POST"])
def add_event_series():
   
        cur = mysql.connection.cursor()
        info = request.get_json()
        series_number = info["series_number"]
        series_date_time = info["series_date_time"]
        series_name = info["series_name"]
        event_event_id = info["event_event_id"]
        
        cur.execute(
            """ INSERT INTO event_series (series_number, series_date_time, series_name, event_event_id) VALUE (%s, %s, %s, %s)""",
            (series_number, series_date_time, series_name, event_event_id),
        )
        mysql.connection.commit()
        print("row(s) affected :{}".format(cur.rowcount))
        rows_affected = cur.rowcount
        cur.close()
        return make_response(
            jsonify(
                {"message": "series added successfully", "rows_affected": rows_affected}
            ),
            201,
        )
@app.route("/club/<int:id>", methods=["PUT"])
def update_event_series(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    series_number = info["series_number"]
    series_date_time = info["series_date_time"]
    series_name = info["series_name"]
    event_event_id = info["event_event_id"]
    
    cur.execute(
        """ UPDATE event_series SET series_number = %s, series_date_time = %s, series_name = %s, event_event_id = %s WHERE club_id = %s """,
        (series_number, series_date_time, series_name, event_event_id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "series updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )
@app.route("/event_series/<int:id>", methods=["DELETE"])
def delete_event_series(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM event_series where series_number = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "series deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )
#Queries
@app.route('/query_join', methods=['GET'])
def get_query_join():
    query = "SELECT athlete.athlete_firstname, athlete.athlete_surname, club.club_name FROM athlete INNER JOIN club ON athlete.athlete_id = club.club_id INNER JOIN event_series ON athlete.athlete_id = event_series.series_number"
    result = data_fetch(query)
    return result


@app.route('/query_sort', methods=['GET'])
def get_query_sort():
    query = "SELECT athlete.athlete_firstname, athlete.athlete_surname, club.club_name FROM athlete INNER JOIN club ON athlete.athlete_id = club.club_id INNER JOIN event_series ON athlete.athlete_id = event_series.series_number ORDER BY athlete.athlete_surname ASC"
    result = data_fetch(query)
    return result

@app.route('/query_group', methods=['GET'])
def get_query_group():
    query = "SELECT event_name, COUNT(*) AS participant_count FROM athlete INNER JOIN club ON athlete.athlete_id = club.club_id INNER JOIN event_series ON athlete.athlete_id = event_series.series_number INNER JOIN event ON athlete.athlete_id = event.event_id GROUP BY event.event_name"
    result = data_fetch(query)
    return result

if _name_ == "_main_":
    app.run(debug=True)