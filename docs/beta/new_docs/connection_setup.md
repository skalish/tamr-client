## How to connect to Tamr
### The Session Object
```python
import tamr_client as tc
import os

# Best practice:
# Grab credentials from environment variables
username = os.environ['TAMR_USERNAME']
password = os.environ['TAMR_PASSWORD']

# Authenticate with username and password
auth = tc.UsernamePasswordAuth(username, password)

# Create a session
session = tc.session.from_auth(auth)
```
### The Instance Object
```python
# configure your Tamr instance properties
protocol = "http"
host = "localhost"
port = 9100

instance = tc.Instance(host=host, port=port, protocol=protocol)
```
### Calling internal APIs
```python
r = session.get(f"{tc.instance(origin(instance))}/api/versioned/service/version")
```