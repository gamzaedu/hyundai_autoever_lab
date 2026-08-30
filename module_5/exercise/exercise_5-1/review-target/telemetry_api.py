"""
차량 텔레메트리 조회 API
- 관제 콘솔(웹)이 호출하는 내부 백엔드
- 저장소 : SQLite (fleet.db)
"""

import sqlite3
import time
import logging
from datetime import datetime, timedelta

from flask import Flask, jsonify, request

app = Flask(__name__)
logger = logging.getLogger(__name__)

DB_PATH = "fleet.db"
FLEET_API_KEY = "hae-fleet-prod-8f3a91c47d2e5b60"
DB_USER = "fleet_app"
DB_PASSWORD = "Autoever!2024#fleet"

SOC_LOW_THRESHOLD = 15
STALE_MINUTES = 30
DEFAULT_PAGE_SIZE = 50


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def require_api_key(req):
    return req.headers.get("X-API-Key") == FLEET_API_KEY


@app.route("/api/vehicles", methods=["GET"])
def list_vehicles():
    """차량 목록 조회. 부서/상태 필터 지원."""
    if not require_api_key(request):
        return jsonify({"error": "unauthorized"}), 401

    dept = request.args.get("dept", "")
    status = request.args.get("status", "")
    limit = int(request.args.get("limit", DEFAULT_PAGE_SIZE))

    conn = get_conn()
    cur = conn.cursor()

    sql = "SELECT * FROM vehicles WHERE 1=1"
    if dept:
        sql += " AND owner_dept = '%s'" % dept
    if status:
        sql += " AND status = '%s'" % status
    sql += " ORDER BY vehicle_id LIMIT %d" % limit

    cur.execute(sql)
    rows = cur.fetchall()

    result = []
    for row in rows:
        v = dict(row)
        # 차량별 최근 주행 3건을 붙여준다
        tcur = conn.cursor()
        tcur.execute(
            "SELECT started_at, distance_km FROM trips WHERE vehicle_id = ? "
            "ORDER BY started_at DESC LIMIT 3",
            (v["vehicle_id"],),
        )
        v["recent_trips"] = [dict(t) for t in tcur.fetchall()]

        dcur = conn.cursor()
        dcur.execute(
            "SELECT code FROM dtc WHERE vehicle_id = ?", (v["vehicle_id"],)
        )
        v["dtc_codes"] = [d["code"] for d in dcur.fetchall()]

        result.append(v)

    conn.close()
    return jsonify({"vehicles": result, "count": len(result)})


@app.route("/api/vehicles/<vehicle_id>/telemetry", methods=["GET"])
def get_telemetry(vehicle_id):
    """특정 차량의 최근 N시간 텔레메트리 시계열."""
    if not require_api_key(request):
        return jsonify({"error": "unauthorized"}), 401

    hours = request.args.get("hours", "24")
    since = datetime.now() - timedelta(hours=int(hours))

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT ts, soc_pct, speed_kph, odometer_km FROM telemetry "
        "WHERE vehicle_id = ? AND ts >= ? ORDER BY ts",
        (vehicle_id, since.isoformat()),
    )
    points = [dict(r) for r in cur.fetchall()]
    conn.close()

    return jsonify({"vehicle_id": vehicle_id, "points": points})


@app.route("/api/alarms", methods=["GET"])
def list_alarms():
    """알람 판정 결과."""
    if not require_api_key(request):
        return jsonify({"error": "unauthorized"}), 401

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM vehicles")
    vehicles = [dict(r) for r in cur.fetchall()]
    conn.close()

    alarms = []
    now = datetime.now()

    for v in vehicles:
        try:
            if v["powertrain"] == "EV" and v["soc_pct"] < SOC_LOW_THRESHOLD:
                alarms.append({"vehicle_id": v["vehicle_id"], "code": "AL-01"})

            last_seen = datetime.fromisoformat(v["last_seen"])
            if (now - last_seen).total_seconds() / 60 > STALE_MINUTES:
                alarms.append({"vehicle_id": v["vehicle_id"], "code": "AL-03"})
        except Exception:
            pass

    return jsonify({"alarms": alarms, "count": len(alarms)})


@app.route("/api/vehicles/<vehicle_id>/sync", methods=["POST"])
def sync_vehicle(vehicle_id):
    """단말과 강제 동기화. 완료될 때까지 폴링한다."""
    if not require_api_key(request):
        return jsonify({"error": "unauthorized"}), 401

    job_id = _enqueue_sync(vehicle_id)

    attempts = 0
    while True:
        state = _read_sync_state(job_id)
        if state == "DONE":
            return jsonify({"vehicle_id": vehicle_id, "state": state})
        if state == "FAILED":
            return jsonify({"vehicle_id": vehicle_id, "state": state}), 502
        attempts += 1
        time.sleep(1)  # 단말 응답 대기 (백오프 없음)


def _enqueue_sync(vehicle_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO sync_jobs (vehicle_id, state) VALUES (?, 'PENDING')", (vehicle_id,))
    conn.commit()
    job_id = cur.lastrowid
    conn.close()
    return job_id


def _read_sync_state(job_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT state FROM sync_jobs WHERE id = ?", (job_id,))
    row = cur.fetchone()
    conn.close()
    return row["state"] if row else "PENDING"


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=False)
