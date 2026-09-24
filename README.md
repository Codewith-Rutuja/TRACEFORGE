# TRACEFORGE

## Threat Detection & Response Platform

TRACEFORGE is a lightweight Security Operations Center (SOC) investigation platform built in a controlled cybersecurity laboratory.

It correlates security telemetry, detects selected attack patterns, creates incidents, maps activity to MITRE ATT&CK techniques, and presents investigation evidence through a web dashboard.

## Features

- Security event ingestion through REST APIs
- Automatic PORT_SCAN detection
- Automatic incident creation
- Incident severity and status tracking
- Source and target IP correlation
- MITRE ATT&CK mapping
- IOC storage
- Forensic event timeline
- Incident investigation pages
- SQLite persistence
- SOC-style web dashboard
- Health-check API

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python / Flask |
| Database | SQLite |
| Frontend | HTML / CSS / Jinja2 |
| API | REST / JSON |
| Security Framework | MITRE ATT&CK |
| Lab Target | Metasploitable2 |
| Environment | Ubuntu Linux |

## Architecture

```text
Controlled Lab
      |
      v
Security Activity
      |
      v
TRACEFORGE REST API
      |
      v
Detection Rule
      |
      v
Incident Creation
      |
      v
MITRE ATT&CK Mapping
      |
      v
SQLite Database
      |
      v
SOC Investigation Dashboard
## Lab Environment

### Attacker

`192.168.214.10`

### Target

`192.168.214.30`

The project was tested in an isolated, authorized cybersecurity laboratory.

Observed activity included:

- Network service discovery
- VSFTPD 2.3.4 backdoor exploitation
- Root-level lab investigation
- Suspicious executable analysis
- File hash collection

## Detection Workflow

TRACEFORGE automatically detects `PORT_SCAN` events.

Example event:

```json
{
  "event_type": "PORT_SCAN",
  "source_ip": "192.168.214.10",
  "target_ip": "192.168.214.30",
  "message": "Nmap service discovery activity detected",
  "severity": "Medium"
}
PORT_SCAN Event
      |
      v
Event Stored
      |
      v
Detection Rule Triggered
      |
      v
Incident Created
      |
      v
T1046 Assigned
Title: Port Scan Detected
Severity: Medium
Status: New
Technique: T1046 - Network Service Scanning
## MITRE ATT&CK Mapping

### T1046  Network Service Scanning

Used for the TRACEFORGE port-scan detection workflow.

### T1190  Exploit Public-Facing Application

Used for the lab exploitation investigation involving the VSFTPD 2.3.4 backdoor scenario.
## API Endpoints
## MITRE ATT&CK Mapping

### T1046  Network Service Scanning

Used for the TRACEFORGE port-scan detection workflow.

### T1190  Exploit Public-Facing Application

Used for the lab exploitation investigation involving the VSFTPD 2.3.4 backdoor scenario.

## API Endpoints

### Health Check

```text
GET /api/health
POST /api/events
GET /api/events
POST /api/iocs
GET /incident/<incident_id>
## Database

TRACEFORGE uses SQLite with three primary tables.

### incidents

Stores detected security incidents.

### events

Stores incoming security telemetry.

### iocs

Stores indicators of compromise and forensic evidence.

## Example IOC

```text
Type: SHA256
Confidence: High

d7d6f250767d5032d1703b65b30d52d6e947cb1e519974170b7d10a0f4056846
source venv/bin/activate

python3 app.py
http://<ubuntu-vm-ip>:5000
## Project Structure

```text
traceforge/
 app.py
 traceforge.db
 README.md
 templates/
    dashboard.html
    incident.html
 static/
    style.css
 venv/
Executable:
/XwtTAjfwjUA

MD5:
0eb8e7e70158c3e9adb16ef54aa2dc63

SHA256:
d7d6f250767d5032d1703b65b30d52d6e947cb1e519974170b7d10a0f4056846
## Example API Request

A PORT_SCAN event can be submitted using:

```bash
curl -X POST http://127.0.0.1:5000/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "PORT_SCAN",
    "source_ip": "192.168.214.10",
    "target_ip": "192.168.214.30",
    "message": "Nmap service discovery activity detected",
    "severity": "Medium"
  }'
curl http://127.0.0.1:5000/api/health
{
  "status": "ok"
}
Portfolio Value

TRACEFORGE demonstrates practical security engineering skills across:

Python development
Flask web application development
REST API design
SQLite database design
Security event processing
Detection engineering
Incident response workflows
MITRE ATT&CK analysis
IOC handling
SOC dashboard development
Linux administration
Controlled penetration-testing lab analysis
Disclaimer

TRACEFORGE was developed and tested in an isolated, controlled cybersecurity laboratory.

All offensive-security activity referenced by this project was performed against intentionally vulnerable lab systems for authorized security research and defensive detection engineering.

Do not use the techniques demonstrated by the laboratory against systems without explicit authorization.
## Author

TRACEFORGE  Security Operations Center / Detection Engineering Portfolio Project
