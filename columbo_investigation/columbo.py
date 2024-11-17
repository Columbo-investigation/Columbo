import argparse
from __init__ import __longname__, __shortname__, __version__, __author__
import json
import requests
# ArgumentParser 객체 생성

def get_sites(email: bool, test: str) -> dict:
    if not test:
        if not email:
            with open('resources/investigation_sites_userid.json', 'r') as f:
                sites = json.load(f)
        else:
            with open('resources/investigation_sites_email.json', 'r') as f:
                sites = json.load(f)
    else:
        if not email:
            with open('resources/userid_test.json', 'r') as f:
                sites = json.load(f)
        else:
            with open('resources/email_test.json', 'r') as f:
                sites = json.load(f)

    return sites

def user_found_print(site, site_url):
    print(f' - {site} found!: {site_url}')

def get_headers() -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0"
    }
    return headers

def investigate_with_userid(sites, args):
    header = get_headers()
    for site, info in sites.items():
        # method
        try:
            if args.test != site:
                continue
            if info["method"] == "GET":
                site_url = info["confirm_url"].format(args.user_info)
                request = requests.get(site_url, headers=header)
            elif info["method"] == "POST":
                site_url = info["confirm_url"].format(args.user_info)
                data = info["data"]
                data[info["key"]] = args.user_info
                request = requests.post(site_url, data=data, headers=header)
        except Exception as e:
            print(f"Error occurred: {e}")
            continue
            

        # confirm
        if info["confirm"] == "include":
            if info["success"] == "userid" and args.user_info in request.text:
                user_found_print(site, info["url"].format(args.user_info))
                continue
            elif info["success"] != "userid" and info["success"] in request.text:
                user_found_print(site, info["url"].format(args.user_info))
                continue
        elif info["confirm"] == "status_code" and info["success"] == request.status_code:
            user_found_print(site, info["url"].format(args.user_info))
            continue

def investigate_with_email(sites, args):
    pass
    # for site, info in sites.items():
    #     # method
        
        


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=f'{__longname__}\nversion:{__version__}',
    )

    # 인수 추가
    parser.add_argument(
        'user_info',
        type=str,
        action='store',
        help='User Info should be provided.'
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'{__shortname__} {__version__}',
        help='Show version information.'
    )
    parser.add_argument(
        '--credit',
        action='version',
        version = f'{__longname__} was made by {__author__}.',
        help = 'Show credit information.'
    )
    parser.add_argument(
        '-e', '--email',
        action='store_true',
        help='Enable email mode.',
        default=False
    )
    parser.add_argument(
        '--test','-t',
        action='store_true',
        help='Test mode for testing specific site.',
        default=False
    )

    # 인수 파싱
    args = parser.parse_args()
    print(args)

    sites = get_sites(args.email, args.test)
    if not args.email:
        investigate_with_userid(sites, args)
    else:
        investigate_with_email(sites, args)
