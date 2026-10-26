import httpx
from django.conf import settings


class FastAPIError(Exception):
    def __init__(self, message, status_code=None, details=None):
        super().__init__(message)
        self.status_code = status_code
        self.details = details


class FastAPIClient:
    def __init__(self):
        # Configure automatic retries for fault tolerance
        transport = httpx.HTTPTransport(retries=3)
        
        self.client = httpx.Client(
            base_url=settings.FASTAPI_BASE_URL,
            timeout=5.0,
            transport=transport
        )

    def request(self, method, path, headers=None, **kwargs):
        try:
            response = self.client.request(method, path, headers=headers, **kwargs)
            response.raise_for_status()
            if response.status_code == 204 or not response.content:
                return None
            return response.json()

        except httpx.HTTPStatusError as e:
            # Capture FastAPI's validation error details (like 422 Unprocessable Entity)
            try:
                error_detail = e.response.json()
            except Exception:
                error_detail = e.response.text

            raise FastAPIError(
                f"FastAPI returned status {e.response.status_code}",
                status_code=e.response.status_code,
                details=error_detail
            ) from e

        except httpx.TimeoutException as e:
            raise FastAPIError("FastAPI service timed out", status_code=504) from e

        except httpx.RequestError as e:
            raise FastAPIError(f"Cannot connect to FastAPI service: {str(e)}", status_code=502) from e

    def get(self, path, params=None, headers=None):
        return self.request("GET", path, params=params, headers=headers)

    def post(self, path, json=None, headers=None):
        return self.request("POST", path, json=json, headers=headers)

    def put(self, path, json=None, headers=None):
        return self.request("PUT", path, json=json, headers=headers)

    def delete(self, path, headers=None):
        return self.request("DELETE", path, headers=headers)


fastapi_client = FastAPIClient()