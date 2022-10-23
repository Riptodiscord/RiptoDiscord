from async_hcaptcha import AioHcaptcha
import string, random, time, base64
from aiohttp import web

def get_task_id():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10)).upper()

async def solve(request):
    site_key, host, proxy, task_id, start_time = request.rel_url.query['site_key'], request.rel_url.query['host'],  request.rel_url.query['proxy'], get_task_id(), time.time()

    print(f'[#{task_id}] [{host}@{site_key}] Starting task...')
    while True:
        try:
            solver = AioHcaptcha(site_key, f"https://{host}", {"executable_path": "chromedriver.exe"})
            resp = await solver.solve(retry_count=3, custom_params={
            })

            print(f'[#{task_id}] [{host}@{site_key}] [{round(time.time() - start_time)}s] {resp[:35]}...')
            return web.Response(text=resp)
        except Exception as e:
            print(f'[#{task_id}] [{host}@{site_key}] {e}')
            return f'err|{e}'

if __name__ == '__main__':
    app = web.Application()
    app.add_routes([
        web.get('/solve', solve),
    ])

    web.run_app(app)