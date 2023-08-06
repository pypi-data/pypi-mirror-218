import asyncio
from bs4 import BeautifulSoup
import aiohttp
import urllib.parse as encode
import argparse
import os

try:
    # https://reverse-whois.whoisxmlapi.com
    whoisxmlapi_key = os.environ['WHOISXMLAPI']
except Exception:
    pass


async def whoisxmlapi(company: str, key: str) -> set[str]:
    payload = {
        "apiKey": key,
        "searchType": "current",
        "mode": "purchase",
        "punycode": True,
        "basicSearchTerms": {"include": [company]}
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post('https://reverse-whois.whoisxmlapi.com/api/v2',
                                headers=headers, json=payload) as response:
            response_json = await response.json()

    domains = set(response_json["domainsList"])
    return domains


async def viewDNS(company: str) -> set[str]:
    domains = set()
    query_encode = encode.quote(company)
    search_url = f"https://viewdns.info/reversewhois/?q={query_encode}"

    headers = {
        'Host': 'viewdns.info',
        'Sec-Ch-Ua': '"Not:A-Brand";v="99", "Chromium";v="112"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.50 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(search_url, headers=headers) as response:
            text = await response.text()

            soup = BeautifulSoup(text, 'lxml')
            table = soup.find('table', {'border': '1'})
            if table:
                rows = table.find_all('tr')
                for row in rows[1:]:
                    columns = row.find_all('td')
                    domain = columns[0].text.strip()
                    domains.add(domain)

    return domains


async def reverse_whois(company: str) -> None:
    tasks = [whoisxmlapi(company, whoisxmlapi_key), viewDNS(company)]
    domains_sets: list = await asyncio.gather(*tasks)
    domains_list = [list(domains) for domains in domains_sets]
    domains = '\n'.join('\n'.join(domain) for domain in domains_list)
    print(domains)


parser = argparse.ArgumentParser()
parser.add_argument('company', metavar='Organization', help='e.g. "Wal-Mart Stores, Inc."')
args = parser.parse_args()
asyncio.run(reverse_whois(args.company))
