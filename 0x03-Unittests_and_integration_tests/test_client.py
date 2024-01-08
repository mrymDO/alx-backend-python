#!/usr/bin/env python3
"""Parameterize and patch as decorators"""

import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from client import GithubOrgClient
from parameterized import parameterized


class TestGithubOrgClient(unittest.TestCase):
    """test githubOrgClient"""

    @parameterized.expand(["google", "abc"])
    @patch("client.get_json")
    def test_org(self, org, mock):
        """test githubOrgClient.org returns the correct value"""
        client = GithubOrgClient(org)
        client.org
        url = "https://api.github.com/orgs/{}".format(org)
        mock.assert_called_once_with(url)

    @parameterized.expand([
        ("random-url", {"repos_url": "http://some_url.com"})
        ])
    def test_public_repos_url(self, name, result):
        """Test method returns correct output"""
        with patch("client.GithubOrgClient.org",
                   PropertyMock(return_value=result)):
            response = GithubOrgClient(name)._public_repos_url
            self.assertEqual(response, result.get("repos_url"))

    @patch("client.get_json")
    def test_public_repos(self, get_json_mock):
        """Test method returns correct output"""
        with patch("client.get_json") as get_json_mock:
            get_json_mock.return_value = [
                {"name": "repo_0"},
                {"name": "repo_1"},
                {"name": "repo_2"},
            ]

            with patch(
                "client.GithubOrgClient._public_repos_url",
                new_callable=PropertyMock
            ) as mock_public_repos_url:

                mock_public_repos_url.return_value = [
                    {"name": "repo_0"},
                    {"name": "repo_1"},
                    {"name": "repo_2"},
                ]

                obj = GithubOrgClient("abc")

                result = obj.public_repos()

                self.assertEqual(result, [repo['name'] for repo in mock_public_repos_url.return_value])
                mock_public_repos_url.assert_called_once()
                get_json_mock.assert_called_once()


if __name__ == '__main__':
    unittest.main()
