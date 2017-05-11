# Tests for JSON Dictionary Parsing Program
# Copyright 2017 Allan LeSage

import unittest
from unittest import mock

import configparser

import parsdict


class GetJsonLocationTestCase(unittest.TestCase):

    def test_jsonkey_gibberish_returns_10(self):
        with self.assertRaises(parsdict.JsonLocationKeyError):
            parsdict.get_json_location('gibberish', 'fake_config')

    @mock.patch.object(configparser.ConfigParser, 'has_option')
    def test_datasources_missing(self, has_option):
        has_option.return_value = False
        mock_config = configparser.ConfigParser()
        with self.assertRaises(parsdict.JsonKeyMissingError):
            parsdict.get_json_location('url', mock_config)

    @mock.patch.object(configparser.ConfigParser, 'get')
    @mock.patch.object(configparser.ConfigParser, 'has_option')
    def test_datasources_vanilla(self, has_option, get):
        has_option.return_value = True
        get.return_value = 'fake_location'
        mock_config = configparser.ConfigParser()
        result = parsdict.get_json_location('url', mock_config)
        self.assertEqual('fake_location', result)
