import json
import unittest

import click.exceptions
from drb.drivers.http import HTTPOAuth2

from pygssearch.utility import (
    parse_config_file, init_conf,
    slice_file, Chunk,
    compute_md5, footprint_extract
)


class TestConf(unittest.TestCase):
    conf_path = 'tests/resources/conf.ini'
    conf_auth2 = 'tests/resources/auth2.ini'
    geo_path = 'tests/resources/geo.json'
    md5 = "c9c8d3decde410c38a094b0c418f8656"
    expected = {'service': 'https://my_gss_catalogue.com',
                'username': 'user', 'password': 'pwd'}

    def test_load_conf(self):
        no_conf = parse_config_file(None)
        self.assertIsNone(no_conf)

        conf = parse_config_file(self.conf_path)
        self.assertIsInstance(conf, dict)
        self.assertEqual(conf, self.expected)

    def test_init_conf(self):
        conf = init_conf(None, None, None, None, None, None,
                         self.conf_path)
        self.assertEqual(conf[0], self.expected['service'])

        conf = init_conf(None, 'Toto', 'Tata', None, None, None,
                         self.conf_path)
        self.assertEqual(conf[1].username, 'Toto')
        self.assertEqual(conf[1].password, 'Tata')

        conf = init_conf(None, None, None, None, None, None, self.conf_auth2)
        self.assertEqual(conf[0], self.expected['service'])
        self.assertIsInstance(conf[1], HTTPOAuth2)

        with self.assertRaises(click.exceptions.BadParameter):
            init_conf(None, None, None, None, None, None, None)

    def test_slice_file(self):
        chunks = slice_file(3, 1)
        self.assertIsInstance(chunks, list)
        self.assertIsInstance(chunks[0], Chunk)
        self.assertEqual(len(chunks), 3)

        chunks = slice_file(7, 5)
        self.assertIsInstance(chunks, list)
        self.assertIsInstance(chunks[0], Chunk)
        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[1].start, 5)
        self.assertEqual(chunks[1].end, 6)

    def test_geojson_load(self):
        with open(self.geo_path) as f:
            geo = json.load(f)
        geo = footprint_extract(geo)
        self.assertIsNotNone(geo)
        self.assertIsInstance(geo, list)
        self.assertEqual(len(geo), 5)

    def test_md5(self):
        self.assertEqual(
            compute_md5(self.conf_path),
            self.md5
        )
