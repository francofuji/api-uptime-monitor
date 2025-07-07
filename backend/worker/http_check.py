import httpx
import ssl
import time
from typing import Dict, Any, Optional

async def perform_check(
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    body: Optional[str] = None,
    timeout: int = 10,
    verify_ssl: bool = True
) -> Dict[str, Any]:
    start = time.monotonic()
    try:
        async with httpx.AsyncClient(timeout=timeout, verify=verify_ssl) as client:
            response = await client.request(method, url, headers=headers, content=body)
            elapsed = (time.monotonic() - start) * 1000
            return {
                "success": True,
                "status_code": response.status_code,
                "response_time_ms": elapsed,
                "response_size": len(response.content),
                "error_message": None,
                "ssl_expiry_date": None  # TODO: implement SSL expiry check
            }
    except Exception as e:
        elapsed = (time.monotonic() - start) * 1000
        return {
            "success": False,
            "status_code": None,
            "response_time_ms": elapsed,
            "response_size": 0,
            "error_message": str(e),
            "ssl_expiry_date": None
        }
