import asyncio
from backend_py.repositories.monitor_repository import MonitorRepository
from backend_py.worker.http_check import perform_check
from backend_py.repositories.monitor_result_repository import MonitorResultRepository
from backend_py.repositories.incident_repository import IncidentRepository
from backend_py.worker.alerting import send_alert, send_recovery_alert
from datetime import datetime

async def run_monitoring():
    # Fetch all active monitors (implement multi-region logic as needed)
    # For demo, fetch for a single org (replace with your logic)
    org_id = "demo-org"
    monitors = await MonitorRepository.find_by_organization(org_id, is_active=True)
    for monitor in monitors:
        result = await perform_check(
            url=monitor.url,
            method=monitor.method,
            headers=monitor.headers,
            body=monitor.body,
            timeout=monitor.timeout
        )
        # Save result
        result_id = await MonitorResultRepository.create(type('Result', (), {
            'monitor_id': monitor.id,
            'response_time_ms': int(result['response_time_ms']),
            'status_code': result['status_code'] or 0,
            'success': result['success'],
            'error_message': result['error_message'],
            'response_size': result['response_size'],
            'location': 'default',
            'checked_at': datetime.utcnow(),
            'ssl_expiry_date': result['ssl_expiry_date']
        })())
        # Incident logic
        if not result['success'] or (result['status_code'] not in monitor.expected_status_codes):
            # Check for open incident
            active_incidents = await IncidentRepository.find_active_by_monitor(monitor.id)
            if not active_incidents:
                await IncidentRepository.create(type('Incident', (), {
                    'monitor_id': monitor.id,
                    'started_at': datetime.utcnow(),
                    'status': 'open'
                })())
                await send_alert(monitor, result)
        else:
            # If there is an open incident, resolve it
            active_incidents = await IncidentRepository.find_active_by_monitor(monitor.id)
            for incident in active_incidents:
                await IncidentRepository.resolve(incident.id, datetime.utcnow())
                await send_recovery_alert(monitor)

# Lambda handler

def lambda_handler(event, context):
    asyncio.run(run_monitoring())
    return {"status": "ok"}
