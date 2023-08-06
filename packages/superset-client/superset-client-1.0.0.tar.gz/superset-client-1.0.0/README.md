<div align="center">
    <img src="./assets/superset-client.jpg" alt="logo" height="60" />
    <br />
    <br />
</div>

# Superset Client

A Python Client for Apache Superset REST API.

This is a Alpha version. Stability is not guaranteed.

## Usage

Setup a superset client:
```python3
from supersetapiclient.client import SupersetClient

client = SupersetClient(
    host="http://localhost:8080",
    username="admin",
    password="admin",
)
```

When developping in local (only), you may need to accept insecure transport (i.e. http).
This is NOT recommanded outside of local development environement, that is requesting `localhost`.

```python3
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
```

## Quickstart

Get all dashboards or find one by name:
```python3
# Get all dashboards
dashboards = client.dashboards.find()

# Get a dashboard by name
dashboard = client.dashboards.find(dashboard_title="Example")[0]
```

Update dashboard colors, some properties and save changes to server:
```python3
# Update label_colors mapping
print(dashboard.colors)
dashboard.update_colors({
    "label": "#fcba03"
})
print(dashboard.colors)

# Change dashboard title
dashboard.dashboard_title = "New title"

# Save all changes
dashboard.save()
```

## Documentation

- [Service of Assets Management](https://confluence.idgcapital.com/pages/viewpage.action?pageId=50725725)
- [Service of Data Building](https://confluence.idgcapital.com/pages/viewpage.action?pageId=50725719)
- [Directory of Data Platform](https://confluence.idgcapital.com/pages/viewpage.action?pageId=46401007)

## Contributing

Before committing to this repository, you must have [pre-commit](https://pre-commit.com) installed, and install
the following pre-commit hooks:

```sh
pre-commit install --install-hooks -t pre-commit -t pre-push
```

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details
