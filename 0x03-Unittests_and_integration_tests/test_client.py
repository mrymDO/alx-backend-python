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
    @patch(
        "client.GithubOrgClient._public_repos_url", new_callable=PropertyMock)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """Test GithubOrgClient.public_repos"""

        mock_public_repos_url.return_value = "http://example.com/repos"

        mock_get_json.return_value = [
            {"name": "repo_0", "license": {"key": "MIT"}},
            {"name": "repo_1", "license": {"key": "GPL"}},
            {"name": "repo_2", "license": {"key": "MIT"}},
        ]

        obj = GithubOrgClient("abc")

        result = obj.public_repos(license="MIT")

        self.assertEqual(result, ["repo_0", "repo_2"])
        mock_public_repos_url.assert_called_once_with()
        mock_get_json.assert_called_once_with("http://example.com/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """Test GithubOrgClient.has_license"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
