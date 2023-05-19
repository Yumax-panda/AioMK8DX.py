# AioMK8DX

An API wrapper for MK8DX 150cc Lounge written in Python.

## Key Features

- Easy to use
- Asynchronous
- Supports all endpoints available to the general user

## Installation

```sh
pip install git+https://github.com/Yumax-panda/AioMK8DX.py.git
```

## Example

```py

from aiomk8dx import AioMKClient
import asyncio

async def main():
    async with AioMKClient() as client:
        player = await client.get_player(name="player_name")
    print(player.name)

    # if you want to get raw data, use the following
    data = player.to_dict()
    print(data)


asyncio.run(main())
```