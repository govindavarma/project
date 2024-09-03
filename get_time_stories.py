import urllib.request
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

def fetch_latest_stories():
    base_url = "https://time.com"
    with urllib.request.urlopen(base_url) as response:
        content = response.read().decode('utf-8')
    
    # Updated regular expression pattern
    pattern = re.compile(r'<a href="(.*?)"[^>]*>.*?<h3[^>]*>(.*?)</h3>', re.DOTALL)
    matches = pattern.findall(content)
    
    stories = []
    for match in matches:
        full_url = base_url + match[0]
        headline = re.sub('<.*?>', '', match[1]).strip()
        stories.append({"title": headline, "link": full_url})
        if len(stories) >= 6:
            break
    
    return stories

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/fetchLatestStories':
            data = fetch_latest_stories()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(data, indent=4), "utf8"))
        else:
            self.send_response(404)
            self.end_headers()

def start_server(server_class=HTTPServer, handler_class=MyRequestHandler, port=8080):
    server_address = ('', port)
    server = server_class(server_address, handler_class)
    print(f'Server is running on port {port}...')
    server.serve_forever()

if __name__ == "__main__":
    start_server()
