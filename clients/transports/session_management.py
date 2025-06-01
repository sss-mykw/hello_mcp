import asyncio
import os

from fastmcp import Client

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, '..', '..', 'my_server.py')
# Client with keep_alive=True (default)
client = Client(file_path)

async def example():
    # First session
    async with client:
        first_session = client.session
        print(f"First session: {first_session}")
        await client.ping()

    # Second session - uses the same subprocess
    async with client:
        second_session = client.session
        print(f"Second session: {second_session}")
        await client.ping()

    # check same sessions
    assert first_session == second_session, "Sessions should be same."

    # Manually close the session
    await client.close()

    # Third session - will start a new subprocess
    async with client:
        third_session = client.session
        print(f"Third session: {third_session}")
        await client.ping()

    # check different sessions
    assert first_session != third_session, "Sessions should be different."

asyncio.run(example())
