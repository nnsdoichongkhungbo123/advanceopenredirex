


# Dependencies

The script uses the following libraries:

- `argparse` for handling command-line arguments.
- `aiohttp` for making HTTP requests.
- `tqdm` for displaying progress.
- `concurrent.futures` for handling concurrent tasks.
- `asyncio` for managing asynchronous tasks.

You need to install these dependencies before running the script. Most of them are part of the standard Python library. You can install `aiohttp` and `tqdm` using pip:

```sh
pip install aiohttp tqdm
```

You can use this script to check for open redirects in web applications. However, you should only use it on systems that you have been given explicit permission to test.

# Docker Build Command

```sh
cd advanceopenredirex/
sudo docker build -t openredirex .                      
sudo docker run --rm -it openredirex /bin/sh
cd /app
cd /usr/local/bin
python3 /usr/local/bin/openredirex -i /app/live_subdomains.txt
python3 /usr/local/bin/openredirex -i /app/live_subdomains.txt -c 100
```
