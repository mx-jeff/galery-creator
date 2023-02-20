import unittest
import os
import shutil
import logging

from main import download_image, parse_image_link, make_requests, create_image_dir
from time import sleep


class TestProgram(unittest.TestCase):
    def setUp(self):
        if os.path.exists('images'):
            shutil.rmtree('images')

    def test_execution(self):
        data = make_requests(search_parameters="cars",
                             url="https://api.pexels.com/v1/search")

        photos = list(parse_image_link(data.json()))
        logging.info(f"Got {len(photos)} photos")
        create_image_dir()

        for photo in photos:
            download_image(photo)

    def tearDown(self):
        sleep(5)
        if os.path.exists('images'):
            shutil.rmtree('images')


if __name__ == '__main__':
    unittest.main()
