# SOL Python ORM Library

## Installation
```
pip install sol-orm-lib
```

## Example usage
```python
from sol_orm_lib.models import TACs, TICs
from sol_orm_lib.database import post_tics_data

tics_data = TICs(
    timestamp=1625779123,
    pvPlannedDown=True,
    stgPlannedDown=True,
    allPlannedDown=True,
    taCs=[
        TACs(k=1, ktic='some_string', n=1, timestamp=1625779123),
        # add more objects if needed
    ]
)

reponse = post_tics_data(tics_data)
print(response)
```

**NOTE**: The library expects the environment variable 'DB_API_URL' to be set.

## Release process
To release a new version of the package, update the version number in the `pyproject.toml` file and publish a release with the same tag. The CI will build and publish the package to PyPI.
