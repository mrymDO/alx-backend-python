#!/usr/bin/env python3
"""Parameterize a unit test"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """test access nested map"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])

    def test_access_nested_map(self, nested_map, path, expected_result):
        """test access nested map"""
        self.assertEqual(access_nested_map(nested_map, path), expected_result)

    @parameterized.expand([
        ({}, ("a",), KeyError, "'a'"),
        ({"a": 1}, ("a", "b"), KeyError, "'b'"),
    ])

    def test_access_nested_map_exception(self, nested_map, path, expected_exception, expected_message):
        """Test that a KeyError is raised with the expected message"""
        with self.assertRaises(expected_exception) as context:
            access_nested_map(nested_map, path)

        self.assertEqual(str(context.exception), expected_message)

class TestGetJson(unittest.TestCase):
    """Test for utils.get_json"""

    @parameterized.expand([
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ])

    def test_get_json(self, url, expected):
        """Test that utils.get_json returns the expected result"""
        mock_response = Mock()
        mock_response.json.return_value = expected
        with patch('requests.get', return_value=mock_response):
            self.assertEqual(get_json(url), expected)
            mock_response.json.assert_called_once()

class TestMemoize(unittest.TestCase):
    """Test for utils.memoize"""

    def test_memoize(self):
        """test memoize function"""

        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        mocked_a_method = Mock(return_value=42)

        test_instance = TestClass()
        test_instance.a_method = mocked_a_method

        result_1 = test_instance.a_property
        result_2 = test_instance.a_property

        mocked_a_method.assert_called_once()

        self.assertEqual(result_1, 42)
        self.assertEqual(result_2, 42)


if __name__ == '__main__':
    unittest.main()
