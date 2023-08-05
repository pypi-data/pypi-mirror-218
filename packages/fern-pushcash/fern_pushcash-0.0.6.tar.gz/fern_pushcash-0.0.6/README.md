
# Push Cash Python Library

[![pypi](https://img.shields.io/pypi/v/fern-pushcash.svg)](https://pypi.python.org/pypi/fern-pushcash)
[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-SDK%20generated%20by%20Fern-brightgreen)](https://github.com/fern-api/fern)

## Installation

Add this dependency to your project's build file:

```bash
pip install fern-pushcash
# or
poetry add fern-pushcash
```

## Usage

```python
from pushcash.client import PushCash

pushcash_client = PushCash(
  token="MY_API_KEY"
)

account_balance = pushcash_client.balance.get()

print(account_balance)
```

## Async Client

```python
from pushcash.client import AsyncPushCash

import asyncio

pushcash_client = AsyncPushCash(
  token="API_KEY"
)

async def get_balance() -> None:
    account_balance = pushcash_client.balance.get()
    print(account_balance)

asyncio.run(get_balance())
```

## Sandbox Environment
By default, the client will use the Production Environment. Below is an example of how you can specify using the Sandbox Environment:

```python
from moneykit.client import MoneyKit
from moneykit.environment import MoneyKitEnvironment

from pushcash.client import PushCash
from pushcash.environment import PushCashEnvironment

client = PushCash(
  environment=PushCashEnvironment.SANDBOX,
  token="API_KEY"
)
```

## Timeouts
By default, the client is configured to have a timeout of 60 seconds. You can customize this value at client instantiation. 

```python
from pushcash.client import PushCash

client = PushCash(token="API_KEY", timeout=15)
```

## Beta status

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning the package version to a specific version in your pyproject.toml file. This way, you can install the same version each time without breaking changes unless you are intentionally looking for the latest version.

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically. Additions made directly to this library would have to be moved over to our generation code, otherwise they would be overwritten upon the next generated release. Feel free to open a PR as a proof of concept, but know that we will not be able to merge it as-is. We suggest opening an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
