from __future__ import annotations

import asyncio
import os

from temporalio.client import Client
from temporalio.worker import Worker

from vibe_ai_ops.temporal.activities.agent_activity import (
    run_validation_agent,
    run_deep_dive_agent,
)

TASK_QUEUE = "vibe-ai-ops"


async def create_client() -> Client:
    """Create a Temporal client from environment variables."""
    address = os.environ.get("TEMPORAL_ADDRESS", "localhost:7233")
    namespace = os.environ.get("TEMPORAL_NAMESPACE", "default")

    tls_cert_path = os.environ.get("TEMPORAL_TLS_CERT_PATH")
    tls_key_path = os.environ.get("TEMPORAL_TLS_KEY_PATH")

    if tls_cert_path and tls_key_path:
        with open(tls_cert_path, "rb") as f:
            cert = f.read()
        with open(tls_key_path, "rb") as f:
            key = f.read()
        from temporalio.client import TLSConfig
        tls = TLSConfig(client_cert=cert, client_private_key=key)
        return await Client.connect(address, namespace=namespace, tls=tls)

    return await Client.connect(address, namespace=namespace)


async def run_worker():
    """Start the Temporal worker."""
    client = await create_client()
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        activities=[run_validation_agent, run_deep_dive_agent],
    )
    print(f"Worker started on task queue: {TASK_QUEUE}")
    await worker.run()


def main():
    asyncio.run(run_worker())


if __name__ == "__main__":
    main()
