import modal
from modal import Stub, web_endpoint, Image, Secret, asgi_app
from fastapi import Depends, HTTPException, status, Request
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from brainchain import Brainchain
from modal import web_endpoint
import os

image = (
    Image.debian_slim(python_version="3.11")
    .apt_install(["python3-dev", "gcc", "git"])
    .apt_install("libmagic-dev")
    .pip_install(["brainchain", "bs4", "redis", "numpy", "flask", "typing", "requests", "modal", "psycopg2-binary", "sqlalchemy", "promptlayer", "openai"])
)

app = FastAPI()
stub = Stub("arthur-example-client-usage", image=image)


@stub.function(secret=Secret.from_name("brainchain-prompt-eng"))
@web_endpoint(method="POST", label="spawn-working-2min")
async def summon_agent(request: Request):
    # Get JSON data from the request
    data = await request.json()

    # Extract the 'prompt' field from the JSON data
    prompt = data.get('prompt')
    # Create an instance of the Brainchain client
    brainchain_client = Brainchain(
        salesintel_api_key=os.getenv('SALESINTEL_API_KEY'))

    # Check if the 'prompt' field exists in the JSON data
    if not prompt:
        return {"error": "No prompt provided in the request body."}, 400

    # Use the Brainchain client to summon an agent with the given prompt
    result = brainchain_client.summon(prompt)

    # Return the result from the Brainchain agent
    return result
