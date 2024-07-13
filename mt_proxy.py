from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    if "payments.braintree-api.com" in flow.request.pretty_host:
        flow.request.host = "localhost"
        flow.request.port = 8080
        flow.request.scheme = "http"
        print(f"Redirecting {flow.request.pretty_url} to localhost:8080")
    else:
        print(f"Forwarding request: {flow.request.pretty_url}")