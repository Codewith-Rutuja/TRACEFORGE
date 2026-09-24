from flask import Flask, render_template, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB = "traceforge.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT NOT NULL,
            source_ip TEXT,
            target_ip TEXT,
            technique TEXT,
            description TEXT,
            created_at TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            source_ip TEXT,
            target_ip TEXT,
            message TEXT,
            severity TEXT,
            created_at TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS iocs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ioc_type TEXT NOT NULL,
            value TEXT NOT NULL,
            source TEXT,
            confidence TEXT,
            created_at TEXT NOT NULL
        )
    """)

    if conn.execute("SELECT COUNT(*) FROM incidents").fetchone()[0] == 0:

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn.execute("""
            INSERT INTO incidents
            (title, severity, status, source_ip, target_ip,
             technique, description, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "VSFTPD 2.3.4 Backdoor Exploitation",
            "Critical",
            "Investigating",
            "192.168.214.10",
            "192.168.214.30",
            "T1190 - Exploit Public-Facing Application",
            "Controlled penetration-test activity detected against the Metasploitable2 target.",
            now
        ))

        conn.execute("""
            INSERT INTO events
            (event_type, source_ip, target_ip, message, severity, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "EXPLOIT",
            "192.168.214.10",
            "192.168.214.30",
            "VSFTPD 2.3.4 backdoor exploitation observed",
            "Critical",
            now
        ))

        conn.execute("""
            INSERT INTO iocs
            (ioc_type, value, source, confidence, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "SHA256",
            "d7d6f250767d5032d1703b65b30d52d6e947cb1e519974170b7d10a0f4056846",
            "/XwtTAjfwjUA",
            "High",
            now
        ))

    conn.commit()    
    conn.close()


@app.route("/")
def dashboard():

    conn = get_db()

    incidents = conn.execute(
        "SELECT * FROM incidents ORDER BY id DESC"
    ).fetchall()

    events = conn.execute(
        "SELECT * FROM events ORDER BY id DESC LIMIT 10"
    ).fetchall()

    iocs = conn.execute(
        "SELECT * FROM iocs ORDER BY id DESC"
    ).fetchall()

    stats = {
        "incidents": conn.execute(
            "SELECT COUNT(*) FROM incidents"
        ).fetchone()[0],

        "critical": conn.execute(
            "SELECT COUNT(*) FROM incidents WHERE severity='Critical'"
        ).fetchone()[0],

        "events": conn.execute(
            "SELECT COUNT(*) FROM events"
        ).fetchone()[0],

        "iocs": conn.execute(
            "SELECT COUNT(*) FROM iocs"
        ).fetchone()[0]
    }

    conn.close()

    return render_template(
        "dashboard.html",
        incidents=incidents,
        events=events,
        iocs=iocs,
        stats=stats
    )


@app.route("/incident/<int:incident_id>")
def incident(incident_id):

    conn = get_db()

    incident = conn.execute(
        "SELECT * FROM incidents WHERE id=?",
        (incident_id,)
    ).fetchone()

    if incident is None:
        conn.close()
        return "Incident not found", 404

    events = conn.execute("""
        SELECT * FROM events
        WHERE source_ip=? OR target_ip=?
        ORDER BY id DESC
    """, (
        incident["source_ip"],
        incident["target_ip"]
    )).fetchall()

    iocs = conn.execute(
        "SELECT * FROM iocs ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "incident.html",
        incident=incident,
        events=events,
        iocs=iocs
    )


@app.route("/api/health")
def health():

    return jsonify({
        "status": "online",
        "service": "TRACEFORGE",
        "timestamp": datetime.now().isoformat()
    })


@app.route("/api/events", methods=["POST"])
def create_event():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "JSON body required"
        }), 400

    required = [
        "event_type",
        "source_ip",
        "target_ip",
        "message",
        "severity"
    ]

    missing = [
        field for field in required
        if field not in data
    ]

    if missing:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing
        }), 400

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db()

    cursor = conn.execute("""
        INSERT INTO events
        (event_type, source_ip, target_ip, message, severity, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["event_type"],
        data["source_ip"],
        data["target_ip"],
        data["message"],
        data["severity"],
        now
    ))

    conn.commit()
    # TRACEFORGE detection rule
    if data["event_type"] == "PORT_SCAN":
        conn.execute("""
            INSERT INTO incidents
            (title, severity, status, source_ip, target_ip, technique, description, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "Port Scan Detected",
            "Medium",
            "New",
            data["source_ip"],
            data["target_ip"],
            "T1046 - Network Service Scanning",
            "TRACEFORGE detected network service discovery activity from the lab attacker.",
            now
        ))
        conn.commit()

    event_id = cursor.lastrowid

    conn.close()

    return jsonify({
        "status": "accepted",
        "event_id": event_id,
        "created_at": now
    }), 201


@app.route("/api/events", methods=["GET"])
def get_events():

    conn = get_db()

    events = conn.execute("""
        SELECT * FROM events
        ORDER BY id DESC
        LIMIT 50
    """).fetchall()

    conn.close()

    return jsonify([
        dict(event)
        for event in events
    ])


@app.route("/api/iocs", methods=["POST"])
def create_ioc():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "JSON body required"
        }), 400

    required = [
        "ioc_type",
        "value",
        "source",
        "confidence"
    ]

    missing = [
        field for field in required
        if field not in data
    ]

    if missing:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing
        }), 400

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_db()

    cursor = conn.execute("""
        INSERT INTO iocs
        (ioc_type, value, source, confidence, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data["ioc_type"],
        data["value"],
        data["source"],
        data["confidence"],
        now
    ))

    conn.commit()

    ioc_id = cursor.lastrowid

    conn.close()

    return jsonify({
        "status": "accepted",
        "ioc_id": ioc_id,
        "created_at": now
    }), 201


init_db()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
