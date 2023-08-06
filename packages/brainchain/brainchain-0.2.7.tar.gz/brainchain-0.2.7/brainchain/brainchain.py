import os
import sys
import json
import requests
from urllib.parse import quote
from . import SalesIntel, FactCheck

class Brainchain:
    def __init__(self, env: str = "prod", api_key: str = os.environ["BRAINCHAIN_API_KEY"], service_url="https://brainchain--agent.modal.run/", salesintel_api_key=os.environ["SALESINTEL_API_KEY"]):
        self.api_key = api_key
        self.env = env
        self.fact_check_instance = FactCheck(environment=env)
        self.sales_intel_client = SalesIntel(salesintel_api_key)
        self.search
        self.environments = ["prod", "dev"]
        self.services = {
            "agent": {
                "prod": "https://brainchain--agent.modal.run/",
                "dev": "https://brainchain--agent-dev.modal.run/"
            },
            "prompting": {
                "prod": "https://brainchain--prompting.modal.run/",
                "dev": "https://brainchain--prompting-dev.modal.run/"
            },
            "pdf_title": {
                "prod": "https://brainchain--pdf-title.modal.run/",
                "dev": "https://brainchain--pdf-title-dev.modal.run/"
            },
            "pdf_authors": {
                "prod": "https://brainchain--pdf-authors.modal.run/",
                "dev": "https://brainchain--pdf-authors-dev.modal.run/"
            },
            "search": {}
        }

    def fact_check(self, statement):
        return self.fact_check_instance.fact_check(statement)

    def search(self, query):
        endpoint = self.services["search"]

    def prompt(self, q, history=[], top_p=0.0, system="You are a multi-disciplinary research assistant who formulates, validates, and figures out correct answers. Your insights are ferocious and undeniable. You expand and digest new concepts and relate them to what you already know.", model="gpt-3.5-turbo-16k", presence_penalty=0.0, frequency_penalty=0.0, n=1):
        endpoint = self.services["prompting"][self.env]
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {"user_prompt": q, "history": history, "system_prompt": system, "model": model, "presence_penalty": float(
            presence_penalty), "frequency_penalty": float(frequency_penalty), "top_p": float(top_p)}
        response = requests.get(endpoint, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    # Only use text_first_page - MUCH faster! url_link provided for testing across link types
    def obtain_title(self, text_first_page: str = None, url_link: str = None):
        endpoint = self.services["pdf_title"][self.env]
        params = {}

        if text_first_page:
            params["document_text"] = text_first_page

        if url_link:
            params["url_link"] = url_link

        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(endpoint, headers=headers, params=params)
        return json.loads(json.dumps(response.content))

    # Only use text_first_page - MUCH faster! url_link provided for testing across link types
    def obtain_authors(self, text_first_page: str = None, url_link: str = None):
        endpoint = self.services["pdf_authors"][self.env]
        params = {}

        if text_first_page:
            params["document_text"] = text_first_page

        if url_link:
            params["url_link"] = url_link

        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.post(endpoint, headers=headers, params=params)
        return json.loads(json.dumps(response.content))

    def summon(self, prompt, agent_type="CCR", model="gpt-4-0613", max_tokens=2048, temperature=0.18, top_p=0.15, top_k=0.0, presence_penalty=1.0, frequency_penalty=1.0):
        endpoint = self.services["agent"][self.env]
        headers = {"Authorization": f"Bearer {self.api_key}"}
        params = {
            "prompt": prompt,
            "env": self.env,
            "agent_type": agent_type,
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty
        }
        response = requests.get(endpoint, headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_company(self, **kwargs):
        return self.sales_intel_client.get_company(**kwargs)

    def get_people(self, **kwargs):
        return self.sales_intel_client.get_people(**kwargs)

    def get_technologies(self, **kwargs):
        return self.sales_intel_client.get_technologies(**kwargs)

    def get_news(self, **kwargs):
        return self.sales_intel_client.get_news(**kwargs)
