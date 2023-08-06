from asyncio import coroutines
import base64
from typing import Coroutine, Optional
import attr

from langfuse.client import Client
from langfuse.langfuse import client
from langfuse.models.create_trace_request import CreateTraceRequest
from langfuse.api.trace import trace_create

@attr.s(auto_attribs=True)
class ApiClient:
    """A Client which has been authenticated for use on secured endpoints"""

    client: Client
    promises: list[Coroutine] = attr.ib(factory=list)

    def __init__(self, public_key: str, secret_key: str, base_url: Optional[str]):
        self.base_url = base_url if base_url else 'https://cloud.langfuse.com'
        

        auth = base64.b64encode(f"{public_key}:{secret_key}".encode()).decode()
        headers = {
            'Authorization': 'Basic ' + auth,
            'X-Langfuse-Sdk-Name': 'langfuse-js',
            'X-Langfuse-Sdk-Version': 'version',
            'X-Langfuse-Sdk-Variant': 'Server',
        }
        self.client = Client(
            base_url=self.base_url,
            headers=headers,
            verify_ssl=True,
            raise_on_unexpected_status=False,
            follow_redirects=False,
        )
    
    def trace(self, body: CreateTraceRequest):
        trace_promise = trace_create.asyncio(self.client, body)
        self.promises.append(trace_promise)

    def flush(self):
        coroutines.all_tasks()
        coroutines.run(coroutines.wait(self.promises))
        

