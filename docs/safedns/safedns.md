# SafeDNS
Wrapper around the UKFast SafeDNS API.<br>
[API Documentation](https://developers.ukfast.io/documentation/safedns)

## Heirarchy

```mermaid
graph TD
    SafeDns --> Zone
    SafeDns --> Template
    Template --> Record
    Zone --> Record
    Zone --> Note
    SafeDns --> Settings
    style SafeDns fill:#ffbbad
```
<br>
## Getting Started

Creating the SafeDNS object:
```python
from UKFastAPI.SafeDNS import SafeDns
safedns = SafeDns('API_TOKEN')
```