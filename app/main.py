import os
import datetime
import socket
import secrets
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify, render_template, g, redirect

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_NAME", "roster"),
        user=os.environ.get("DB_USER", "roster_user"),
        password=os.environ.get("DB_PASSWORD"),
        port=os.environ.get("DB_PORT", "5432"),
        cursor_factory=RealDictCursor
    )

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS shifts (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            shift_date DATE NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            claimed_by TEXT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

with app.app_context():
    try:
        init_db()
    except Exception as e:
        print(f"DB init error: {e}")

@app.before_request
def generate_nonce():
    g.nonce = secrets.token_hex(16)

@app.after_request
def set_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    return response

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, title, shift_date AS date, start_time AS start,
                   end_time AS end, claimed_by
            FROM shifts
            ORDER BY shift_date, start_time;
        """)
        shifts = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"DB error: {e}")
        shifts = []

    return render_template('index.html',
        shifts=shifts,
        environment=os.environ.get('ENVIRONMENT', 'production'),
        hostname=socket.gethostname(),
        version=os.environ.get('APP_VERSION', '1.1.0')
    )

@app.route('/shifts', methods=['GET'])
def get_shifts():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, title, shift_date AS date, start_time AS start,
               end_time AS end, claimed_by
        FROM shifts
        ORDER BY shift_date, start_time;
    """)
    shifts = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify({"shifts": shifts})

@app.route('/shifts', methods=['POST'])
def create_shift():
    if request.content_type and 'application/json' in request.content_type:
        data = request.get_json()
    else:
        data = request.form

    if not data or not all(k in data for k in ['title', 'date', 'start', 'end']):
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO shifts (title, shift_date, start_time, end_time, claimed_by)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, title, shift_date AS date, start_time AS start,
                  end_time AS end, claimed_by;
    """, (data['title'], data['date'], data['start'], data['end'], None))

    cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

@app.route('/shifts/<int:shift_id>/claim', methods=['POST'])
def claim_shift(shift_id):
    if request.content_type and 'application/json' in request.content_type:
        data = request.get_json()
    else:
        data = request.form

    if not data or 'employee' not in data:
        return jsonify({"error": "Employee name required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT claimed_by FROM shifts WHERE id = %s;", (shift_id,))
    shift = cur.fetchone()

    if not shift:
        cur.close()
        conn.close()
        return jsonify({"error": "Shift not found"}), 404

    if shift['claimed_by']:
        cur.close()
        conn.close()
        return jsonify({"error": "Shift already claimed"}), 409

    cur.execute("""
        UPDATE shifts SET claimed_by = %s WHERE id = %s
        RETURNING id, title, shift_date AS date, start_time AS start,
                  end_time AS end, claimed_by;
    """, (data['employee'], shift_id))

    cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/')

@app.route('/shifts/<int:shift_id>', methods=['DELETE'])
def delete_shift(shift_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM shifts WHERE id = %s RETURNING id;", (shift_id,))
    deleted_shift = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if deleted_shift:
        return jsonify({"message": "Shift deleted"}), 200
    return jsonify({"error": "Shift not found"}), 404

@app.route('/health')
def health():
    return jsonify({
        "status": "ok",
        "app": "roster",
        "version": os.environ.get('APP_VERSION', '1.1.0'),
        "env": os.environ.get('ENVIRONMENT', 'dev'),
        "host": socket.gethostname(),
        "time": datetime.datetime.utcnow().isoformat() + 'Z',
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
