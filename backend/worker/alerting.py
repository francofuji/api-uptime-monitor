async def send_alert(monitor, result):
    # Placeholder for sending alert (email/webhook)
    print(f"ALERT: Monitor {monitor.name} is DOWN. Reason: {result['error_message'] or result['status_code']}")

async def send_recovery_alert(monitor):
    # Placeholder for sending recovery alert
    print(f"RECOVERY: Monitor {monitor.name} is UP again.")
