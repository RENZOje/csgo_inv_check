import asyncio
import json
import aiohttp


global loop

async def get_json(url):
    url = f'https://api.csgofloat.com/?url={url}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()

def get_price(resp):
    try:
        result = json.loads(resp)['iteminfo']['floatvalue']
    except KeyError:
        result = 0
    return result

async def get_task_range(rd_inspect_url):
    global floats_items
    floats_items = []
    tasks = []
    for name in rd_inspect_url:
        tasks.append((rd_inspect_url.index(name), loop.create_task(get_json(name))))

    for name, t in tasks:
        json_resp = await t
        price = get_price(json_resp)
        floats_items.append(price)

def call_float(rd_inspect_url):
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(get_task_range(rd_inspect_url))

    return floats_items
