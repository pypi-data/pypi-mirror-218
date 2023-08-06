# aioarp

[![PyPI - Version](https://img.shields.io/pypi/v/aioarp.svg)](https://pypi.org/project/aioarp)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aioarp.svg)](https://pypi.org/project/aioarp)
[![coverage](https://img.shields.io/codecov/c/github/karosis88/aioarp/master)](https://app.codecov.io/gh/karosis88/aioarp)
![license](https://img.shields.io/github/license/karosis88/aioarp)

-----

**Table of Contents**

- [Installation](#installation)
- [Documentation](#documentation)
- [ARP Spoofing](#arp-spoofing)
- [ARP requests](#how-to-send-arp-requests)
- [License](#license)

## Installation

```console
pip install aioarp
```

## Documentation
[Click here](https://karosis88.github.io/aioarp/)

## Arp spoofing

Using this command, you can disable internet access for any device on your local network.

```shell
$ aioarp disable 192.168.0.81 192.168.0.1 enp0s3 --seconds 10
```

or 

```shell
$ aioarp spoof 192.168.0.81 192.168.0.1 11:11:11:11:11:11  enp0s3 --seconds 10
```

`spoof` can be used to specify the fake mac address.

Where...
- `192.168.0.81` is a target IP address for which we are blocking internet access.
- `192.168.0.1` is a gateway for our target IP address.
- `enp0s3` is an optional interface used to send ARP requests. if not specified, the default interface is used.
- `seconds` is an option that specifies how long we want to disable internet access for the target IP address.

## How to send ARP requests

### Sync
```py
import aioarp
response = aioarp.request('10.0.2.2', 'enp0s3')
print(response.sender_mac)
# ee:xx:aa:mm:pp:le mac address
```

### Async [trio or asyncio]
```py
import trio
import aioarp
response = trio.run(aioarp.arequest, '10.0.2.2', 'enp0s3')
```

```py
import asyncio
import aioarp
response = asyncio.run(aioarp.arequest('10.0.2.2', 'enp0s3'))
```

Or without specifying an `interface` parameter

```
response = aioarp.request('10.0.2.2')
```

## License

`aioarp` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

