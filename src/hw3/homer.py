from argparse import ArgumentParser
import asyncio
from concurrent.futures import ThreadPoolExecutor
from shutil import copyfileobj
from urllib.request import urlopen
from bs4 import BeautifulSoup

URL = "https://www.thisfuckeduphomerdoesnotexist.com/"

# we don't want to ddos the site (and ourselves)
executor = ThreadPoolExecutor(4)


def get_image_url_from_site_source(page: bytes) -> str:
    soup = BeautifulSoup(page, "html.parser")
    img = soup.find("img", id="image-payload")
    return img["src"]


def download_file(url: str, filename: str):
    with urlopen(url) as src, open(filename, "wb") as file:
        copyfileobj(src, file)


def download_random_homer() -> str:
    "Download a random Homer pic into the work directory and return its filename"

    page = urlopen(URL).read()
    image_url = get_image_url_from_site_source(page)
    filename = image_url.split("/")[-1]
    print(f"Downloading {filename}")
    download_file(image_url, filename)
    return filename


async def main():
    parser = ArgumentParser()
    parser.add_argument("-n", dest="pics", type=int, default=1, help="Number of pictures to download.")
    args = parser.parse_args()
    pics_number = args.pics

    loop = asyncio.get_running_loop()
    tasks = [loop.run_in_executor(executor, download_random_homer) for _ in range(pics_number)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
