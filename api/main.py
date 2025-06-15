from flask import *
from datetime import * 
import pymysql

# Application Default Config
app = Flask(__name__)

# DB Instance
def db_connect():
    conn = pymysql.connect(
            host='localhost',
            user='flaskuser',
            password='goqudeo1!',
            db='monkfish',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
            )
    return conn

# common API
@app.route('/api/startup/submit', methods=['POST'])
def submit_startup():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    name = data.get('name')
    telno = data.get('telno')
    email = data.get('email')
    area = data.get('area')
    description = data.get('description')

    if not all([name, telno]):
        return jsonify({'error': 'name and telno are required'}), 400

    conn = db_connect()
    cur = conn.cursor()
    sql = 'INSERT INTO franchise (name, telno, email, area, description) VALUES (%s, %s, %s, %s, %s)'
    cur.execute(sql, (name, telno, email, area, description))
    conn.commit()
    conn.close()

    return jsonify({'message':'Happy:)'}), 200

# Dashboard
@app.route('/api/data', methods=['GET'])
def get_submission_data():
    page = request.args.get('page', default=1, type=int)
    per_page = 20
    offset = (page - 1) * per_page

    conn = db_connect()
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) AS cnt FROM franchise")
        total_count = cur.fetchone()['cnt']

        cur.execute("SELECT * FROM franchise ORDER BY input_time DESC LIMIT %s OFFSET %s", (per_page, offset))
        rows = cur.fetchall()
    conn.close()

    total_pages = (total_count + per_page - 1) // per_page

    return jsonify({
        'data': rows,
        'page': page,
        'per_page': per_page,
        'total_pages': total_pages,
        'total_count': total_count
    })


@app.route('/admin/api/delete-startup-request', methods=['POST'])
def delete_franchise():
    submission_id = request.json.get('id')
    if not submission_id:
        return jsonify({'error': 'ID가 필요합니다.'}), 400

    conn = db_connect()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM franchise WHERE id = %s", (submission_id,))
        conn.commit()
        deleted_count = cur.rowcount
    conn.close()

    if deleted_count == 0:
        return jsonify({'error': '해당 ID가 없습니다.'}), 404

    return jsonify({'message': '삭제되었습니다.', 'id': submission_id})


@app.route('/admin/api/update-startup-request-status', methods=['POST'])
def update_status():
    data = request.json
    submission_id = data.get('id')
    new_status = data.get('status')

    if not submission_id or not new_status:
        return jsonify({'error': 'ID와 상태 값이 필요합니다.'}), 400

    if new_status not in ['접수완료', '처리중', '처리완료']:
        return jsonify({'error': '잘못된 상태 값입니다.'}), 400

    conn = db_connect()
    with conn.cursor() as cur:
        cur.execute("UPDATE franchise SET status = %s WHERE id = %s", (new_status, submission_id))
        conn.commit()
        updated_count = cur.rowcount
    conn.close()

    if updated_count == 0:
        return jsonify({'error': '해당 ID가 없습니다.'}), 404

    return jsonify({'message': '상태가 업데이트 되었습니다.', 'id': submission_id, 'status': new_status})


# health check
@app.route('/api/health', methods=['GET'])
def health():
    return 'API Server is Health :)'


# application run
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
