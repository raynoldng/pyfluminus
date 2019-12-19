from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import re
import socket
from threading import Thread
import os

from urllib.parse import urlparse, parse_qsl
import requests

FIXTURES_PATH = os.path.join(os.path.dirname(__file__), "fixtures")
API_FIXTURES_PATH = os.path.join(FIXTURES_PATH, "api")
AUTH_FIXTURES_PATH = os.path.join(FIXTURES_PATH, "authorization")

MOCK_CONSTANTS = {
    "AUTH_URL": "http://localhost:8081",
    "CLIENT_ID": "E10493A3B1024F14BDC7D0D8B9F649E9-234390",
    "REDIRECT_URI": "https://luminus.nus.edu.sg/auth/callback",
    "RESOURCE": "sg_edu_nus_oauth",
    "OCP_SUBSCRIPTION_KEY": "6963c200ca9440de8fa1eede730d8f7e",
    "API_BASE_URL": "http://localhost:8082",
}

# load all of the json files
api_fixtures = []
auth_fixtures = []

for root, _subdirs, files in os.walk(API_FIXTURES_PATH):
    for file in files:
        if not file.endswith(".json"):
            continue
        with open(os.path.join(root, file)) as json_file:
            api_fixtures.append(json.load(json_file))

for root, _subdirs, files in os.walk(AUTH_FIXTURES_PATH):
    for file in files:
        if not file.endswith(".json"):
            continue
        with open(os.path.join(root, file)) as json_file:
            auth_fixtures.append(json.load(json_file))


class MockServerRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        def match(request_handler: BaseHTTPRequestHandler, fixture) -> bool:
            parsed_url = urlparse(request_handler.path)
            query_params = dict(parse_qsl(parsed_url.query))

            request = fixture["request"]

            return (
                request_handler.command == request["method"] and
                parsed_url.path == request['request_path'] and
                query_params == request.get('query', {})
            )


        # DEBUGGING
        # parsed_url = urlparse(self.path)
        # query_params = dict(parse_qsl(parsed_url.query))
        # print(self.command, parsed_url.path, query_params)

        response = next(fix["response"] for fix in api_fixtures if match(self, fix))

        # Add response content.
        self.send_response(response["status_code"])
        # Add response headers.
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        response_content = response["body"]
        self.wfile.write(response_content.encode("utf-8"))
        return


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(("localhost", 0))
    address, port = s.getsockname()
    s.close()
    return port


def start_mock_server(port):
    mock_server = HTTPServer(("localhost", port), MockServerRequestHandler)
    mock_server_thread = Thread(target=mock_server.serve_forever)
    mock_server_thread.setDaemon(True)
    mock_server_thread.start()

    return mock_server
