from flask import Flask, jsonify
import psycopg2
import random
from flask_cors import CORS, cross_origin

app = Flask(__name__)

app.config.from_object(__name__)
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": "Access-Control-Allow-Origin"}})
# CORS(app, resources={r"/*": {"origins": "http://localhost:8080", "allow_headers": "Access-Control-Allow-Origin"}})

db_connection_details = {
    'dbname': 'anime_app',
    'user': 'maruan',
    'password': 'maruan99',
    'host': 'localhost',
    'port': '5432'
}

@app.route('/get_random_anime_character', methods=['GET'])
@cross_origin()
def get_random_anime_character():
    try:
        # Connect to the PostgreSQL database
        connection = psycopg2.connect(**db_connection_details)
        cursor = connection.cursor()

        # Get the total number of rows in the "anime_characters" table
        cursor.execute('SELECT COUNT(*) FROM anime_characters')
        total_rows = cursor.fetchone()[0]

        # Generate a random row number between 1 and the total number of rows
        random_row_number = random.randint(1, total_rows)

        # Fetch the random anime character record
        cursor.execute('SELECT image_url, correct_answer FROM anime_characters WHERE id = %s', (random_row_number,))
        image_url, correct_answer = cursor.fetchone()

        # Close the database connection
        cursor.close()
        connection.close()

        # Create a JSON response
        response = {
            'image_url': image_url,
            'correct_answer': correct_answer
        }

        return jsonify(response), 200

    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL:", error)
        return jsonify({'error': 'Something went wrong'}), 500

if __name__ == '__main__':
    app.run(debug=True)
