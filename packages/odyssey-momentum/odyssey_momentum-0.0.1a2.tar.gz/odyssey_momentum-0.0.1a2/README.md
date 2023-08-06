# Odyssey Momentum

Python library to interact with the Odyssey momentum platform.


[![PyPI - Version](https://img.shields.io/pypi/v/odyssey-momentum.svg)](https://pypi.org/project/odyssey-momentum)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/odyssey-momentum.svg)](https://pypi.org/project/odyssey-momentum)

-----
> :warning: **Work in progress, API of this library has not been stablized.**
-----

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

### Prerequisites

 - Python 3.10 or 3.11
 - x86_64 platform (for now, a c extension is used, not build for other platforms yet)

```console
pip install --pre odyssey-momentum
```
(*pre*, since it is still in development)

## Usage

The python package contains 3 parts:

- `api` - To access the JSON, REST-like API.
- `posbus` - To connect throurh websocket and receive real times updates.
- `bot` - A higher level library build on top of these, providing functionality to build bots.

Library is build around python async/await functionality, particulary async context managers and async generators.
So needs to be used with either [asyncio](https://docs.python.org/3/library/asyncio.html) or [trio](https://trio.readthedocs.io/en/stable/).

### Example

Run from an asyncio shell:

```console
python -m asyncio
```

Example API call:
```python
from odyssey_momentum import api, posbus

url = "https://dev.odyssey.ninja"
auth = await posbus.authenticate_guest(url, cache=False)
client = api.API(url, auth["token"])
me = await client.current_user()
print(me.name)
```

Example websocket connection:

```python
from odyssey_momentum import posbus

url = "https://dev.odyssey.ninja"
auth = await posbus.authenticate_guest(url, cache=False)
async with posbus.connect(url, auth) as (send, stream):
  await send(posbus.teleport_request("00000000-0000-8000-8000-000000000002"))
  async for msg in stream:
    print(msg)
```

See `examples` directory for more 


## Development

Project is managed with [hatch](https://hatch.pypa.io/).

To get a shell for development:
```console
hatch shell
```

Run tests:
```console
hatch run test
```


Run code lint:
```
hatch run lint:all
```

```console
hatch build --hooks-only
```


Build packages (outputs in `dist` directory:

```console
hatch build
```

## License

`odyssey-momentum` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
