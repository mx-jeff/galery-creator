import os
import requests
import dotenv
import json
import concurrent.futures
import logging
import shutil

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')


def make_requests(search_parameters:str, url:str) -> json:
    """create a request

    Args:
        search_parameters (str): query parameters

    Returns:
        (json): json object
    """

    logging.info(f"> making request to {url} with parameters {search_parameters}")
    querystring = {"query": search_parameters}

    headers = {
        "Autorization": os.getenv("PEXELS_API_KEY"),
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        logging.error(
            f"Error making request, Code: {response.status_code}")
        return

    return response


def parse_image_link(data):
    logging.info("> Parsing image...")
    for photo in data['photos']:
        data = {
            "url": photo["src"]["original"],
            "alt": photo["alt"]
        }
        logging.debug(f"Got {data}")
        yield data 


def download_image(image_data):
    try:
        url = image_data["url"]
        alt = image_data["alt"]
        logging.info(f"downloading image '{alt}' ")

        response = requests.get(url, stream=True)
        if response.status_code != 200:
            logging.error(
                f"Error downloading image, Code: {response.status_code}")
            return

        with open(f'images/{alt}.png', "wb") as f:
            shutil.copyfileobj(response.raw, f)

    except Exception as e:
        logging.error(e)
        raise


def create_image_dir(image_dir="images"):
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)


def main():
    data = make_requests(search_parameters="cars", url="https://api.pexels.com/v1/search")

    photos = list(parse_image_link(data.json()))
    logging.info(f"Got {len(photos)} photos")
    create_image_dir()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_image, photos)


if __name__ == "__main__":
    main()
