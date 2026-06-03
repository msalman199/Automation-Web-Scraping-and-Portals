from http.server import HTTPServer, BaseHTTPRequestHandler
import random

class CAPTCHAHandler(BaseHTTPRequestHandler):
    """
    Mock server that randomly presents CAPTCHA challenges.
    """
    
    def do_GET(self):
        """Handle GET requests with random CAPTCHA challenges."""
        # TODO: Implement logic that:
        # - 30% of requests return CAPTCHA page (status 403)
        # - 70% return normal content (status 200)
        # - CAPTCHA page should contain text "CAPTCHA detected"
        # - Normal page should contain "Welcome! Content here."
        pass
    
    def log_message(self, format, *args):
        """Suppress default logging."""
        pass

def run_server(port=8080):
    """Start the mock server."""
    # TODO: Create HTTPServer instance
    # Print server start message
    # Start serving requests
    pass

if __name__ == "__main__":
    run_server()
