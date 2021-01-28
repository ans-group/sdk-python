# sdk-python
Python interface for the UKFast APIs.

## Documentation
[sdk-python Documentation](https://ukfast.github.io/sdk-python/)<br>
[UKFast API Documentation](https://developers.ukfast.io/getting-started)

## Quick Start
```python
from UKFast.SafeDNS import SafeDns

safedns = SafeDns('TOKEN') # Can instead be automatically retrieved from an environment variable named UKF_API_KEY.

print(safedns.zones.list())
```

## Building Package
```bash
pip install wheel
python setup.py bdist_wheel
pip install dist/UKFastAPI*
```

## Currently Supported APIs
* SafeDNS