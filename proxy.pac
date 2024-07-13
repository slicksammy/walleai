function FindProxyForURL(url, host) {
    if (shExpMatch(url, "https://payments.braintree-api.com/graphql")) {
        return "PROXY 127.0.0.1:8080";
    }
    return "DIRECT";
}