import asyncio
import json
import aiohttp



global loop

async def get_json(name):
    url = f'http://csgobackpack.net/api/GetItemPrice/?currency=USD&id={name}&time=7&icon=1'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()

def get_price(resp):
    try:
        result = json.loads(resp)['average_price']
    except KeyError:
        result = 0
    return result

async def get_task_range(rd_full_name):
    global rd_price
    rd_price = []
    tasks = []
    for name in rd_full_name:
        tasks.append((rd_full_name.index(name), loop.create_task(get_json(name))))

    for name, t in tasks:
        json_resp = await t
        price = get_price(json_resp)
        rd_price.append(float(price))

def call_price(rd_full_name):
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(get_task_range(rd_full_name))
    return rd_price