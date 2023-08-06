# Pystax

The pystax is a Python library that allows you to probe domains and IP addresses to check their status codes. It helps you verify the accessibility of a domain or IP by performing an HTTP request and retrieving the corresponding status code.

## Features

- Supports probing domains using both HTTP and HTTPS protocols.
- Handles various errors such as invalid domains, connection timeouts, and SSL certificate verification failures.
- Includes special handling for the localhost address (`127.0.0.1` or `"localhost"`).

## Installation

You can install the pystax library using pip:

```bash
pip install pystax
