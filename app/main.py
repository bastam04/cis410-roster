import os
import datetime
import socket
import secrets
from flask import Flask, request, jsonify, render_template_string, g

app = Flask(__name__)

# ── In-memory data store (replaced by Cloud SQL in production) ────────────────
shifts = [
    {"id": 1, "title": "Morning Shift", "date": "2026-06-10", "start": "08:00", "end": "14:00", "claimed_by": None},
    {"id": 2, "title": "Evening Shift", "date": "2026-06-10", "start": "14:00", "end": "20:00", "claimed_by": None},
    {"id": 3, "title": "Weekend Morning", "date": "2026-06-14", "start": "09:00", "end": "15:00", "claimed_by": None},
]

# ── Security headers ──────────────────────────────────────────────────────────
@app.before_request
def generate_nonce():
    g.nonce = secrets.token_hex(16)

@app.after_request
def set_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    return response

# ── Routes ────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>Roster — Shift Scheduler</title></head>
    <body>
        <h1>Roster</h1>
        <p>Simplifying scheduling so small businesses can focus on what matters most.</p>
        <ul>
            <li><a href="/shifts">View Available Shifts</a></li>
            <li><a href="/health">Health Check</a></li>
        </ul>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/shifts', methods=['GET'])
def get_shifts():
    return jsonify({"shifts": shifts})

@app.route('/shifts', methods=['POST'])
def create_shift():
    data = request.get_json()
    if not data or not all(k in data for k in ['title', 'date', 'start', 'end']):
        return jsonify({"error": "Missing required fields"}), 400
    new_shift = {
        "id": len(shifts) + 1,
        "title": data['title'],
        "date": data['date'],
        "start": data['start'],
        "end": data['end'],
        "claimed_by": None
    }
    shifts.append(new_shift)
    return jsonify(new_shift), 201

@app.route('/shifts/<int:shift_id>/claim', methods=['POST'])
def claim_shift(shift_id):
    data = request.get_json()
    if not data or 'employee' not in data:
        return jsonify({"error": "Employee name required"}), 400
    for shift in shifts:
        if shift['id'] == shift_id:
            if shift['claimed_by']:
                return jsonify({"error": "Shift already claimed"}), 409
            shift['claimed_by'] = data['employee']
            return jsonify(shift)
    return jsonify({"error": "Shift not found"}), 404

@app.route('/shifts/<int:shift_id>', methods=['DELETE'])
def delete_shift(shift_id):
    for i, shift in enumerate(shifts):
        if shift['id'] == shift_id:
            shifts.pop(i)
            return jsonify({"message": "Shift deleted"}), 200
    return jsonify({"error": "Shift not found"}), 404

@app.route('/health')
def health():
    return jsonify({
        "status": "ok",
        "app": "roster",
        "version": os.environ.get('APP_VERSION', '1.0.0'),
        "env": os.environ.get('ENVIRONMENT', 'dev'),
        "host": socket.gethostname(),
        "time": datetime.datetime.utcnow().isoformat() + 'Z',
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
