# sdk-python
Python interface for the UKFast APIs.

## Documentation
[sdk-python Documentation]()
[UKFast API Documentation](https://developers.ukfast.io/getting-started)

## Quick Start
```python
from UKFast.SafeDNS import SafeDns

safedns = SafeDns('TOKEN') # Can instead be automatically retrieved from an environment variable named UKF_API_KEY.

print(safedns.zones.list())
```

## Currently Supported APIs
* SafeDNS