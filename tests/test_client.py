"""
The MIT License (MIT)

Copyright (c) 2023-present Yumax-panda

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from aiomk_api.utils import Search
import aiomk_api
import pytest

@pytest.mark.asyncio
async def test_get_player():
    async with aiomk_api.AioMKClient() as client:
        player = await client.get_player(name="azure_mk")
    assert player.name == "Azure_mk"

@pytest.mark.asyncio
async def test_get_players():
    async with aiomk_api.AioMKClient() as client:
        players = await client.get_players(
            names=("azure_mk", "yumax_panda")
        )
    assert players[0].name == "Azure_mk"
    assert players[1] is None

@pytest.mark.asyncio
async def test_get_player_details():
    async with aiomk_api.AioMKClient() as client:
        player = await client.get_player_details(name="azure_mk")
        player2 = await client.get_player_details(name="yumax_panda")
    assert player.name == "Azure_mk"
    assert player.mmr == 5998
    assert player2 is None

@pytest.mark.asyncio
async def test_get_player_list():
    async with aiomk_api.AioMKClient() as client:
        players = await client.get_player_list(min_mmr=16000)
        players_empty = await client.get_player_list(min_mmr=20000)
    assert len(players) == 11
    assert len(players_empty) == 0

@pytest.mark.asyncio
async def test_get_leaderboard():
    async with aiomk_api.AioMKClient() as client:
        leaderboard = await client.get_leaderboard(8, min_mmr=16000)
        leaderboard_empty = await client.get_leaderboard(8, min_mmr=20000)
        s = Search(discord_id=915185563638833173)
        leaderboard_search = await client.get_leaderboard(8, search=s)
        leaderboard_search2 = await client.get_leaderboard(8, search=s)
    assert len(leaderboard) == 11
    assert len(leaderboard_empty) == 0
    assert leaderboard_search[0].name == "Azure_mk"
    assert leaderboard_search == leaderboard_search2
    assert bool(leaderboard_search)

@pytest.mark.asyncio
async def test_get_table():
    async with aiomk_api.AioMKClient() as client:
        table = await client.get_table(8)
        table2 = await client.get_table(12345)
    assert table is None
    assert table2 is not None

@pytest.mark.asyncio
async def test_get_tables():
    async with aiomk_api.AioMKClient() as client:
        tables = await client.get_tables(after=datetime.utcnow()- timedelta(hours=1))
        tables[0].to_dict()
    assert tables is not None

@pytest.mark.asyncio
async def test_get_table_unverified():
    async with aiomk_api.AioMKClient() as client:
        table = await client.get_table_unverified(8)
        table2 = await client.get_table_unverified(12345)
    assert table is None
    assert table2 is not None

@pytest.mark.asyncio
async def test_get_bonus():
    async with aiomk_api.AioMKClient() as client:
        bonus = await client.get_bonus(12345)
        bonus2 = await client.get_bonus(10000000)
    assert bonus is  not None
    assert bonus2 is None

@pytest.mark.asyncio
async def test_get_penalty():
    async with aiomk_api.AioMKClient() as client:
        penalty = await client.get_penalty(12345)
        penalty2 = await client.get_penalty(10000000)
    assert penalty is  not None
    assert penalty2 is None

@pytest.mark.asyncio
async def test_get_penalties():
    async with aiomk_api.AioMKClient() as client:
        penalties = await client.get_penalties(name="sukuna", include_deleted=True)
    assert penalties is not None