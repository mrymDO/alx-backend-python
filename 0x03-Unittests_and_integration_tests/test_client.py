#!/usr/bin/env python3
"""Parameterize and patch as decorators"""

import unittest
from unittest.mock import patch, MagicMock
from client import GithubOrgClient
from parameterized import parameterized


class TestGithubOrgClient(unittest.TestCase):
    """test githubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org, mock):
        """test githubOrgClient.org returns the correct value"""
        client = GithubOrgClient(org)
        client.org
        url = "https://api.github.com/orgs/{}".format(org)
        mock.assert_called_once_with(url)


if __name__ == '__main__':
    unittest.main()
