#!/usr/bin/env python3
"""Parameterize and patch as decorators"""

import unittest
from unittest.mock import patch, MagicMock, PropertyMock, Mock
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class

from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


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

    @classmethod
    def setUpClass(cls):
        """Set up the class"""
        cls.get_patcher = patch("requests.get")

        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = cls.mock_requests_get_json

    @classmethod
    def tearDownClass(cls):
        """Tear down the class"""
        cls.get_patcher.stop()

    @staticmethod
    def mock_requests_get_json(url):
        """Mock requests.get(url).json() based on the provided fixtures"""
        if url == "https://api.github.com/orgs/example_org":
            return org_payload
        elif url == "https://api.github.com/orgs/example_org/repos":
            return repos_payload
        elif url == "https://api.github.com/orgs/example_org/repos/apache2":
            return apache2_repos
        else:
            raise ValueError(f"Unexpected URL: {url}")

    def test_public_repos_integration(self):
        """Integration test for GithubOrgClient.public_repos"""

        obj = GithubOrgClient("example_org")

        result = obj.public_repos(license="MIT")

        self.assertEqual(result, expected_repos)

    def test_public_repos(self):
        """Test GithubOrgClient.public_repos"""
        obj = GithubOrgClient("example_org")

        expected_result = expected_repos

        result = obj.public_repos()

        self.assertEqual(result, expected_result)

    def test_public_repos_with_license(self):
        """Test GithubOrgClient.public_repos with license argument"""
        obj = GithubOrgClient("example_org")

        expected_result = apache2_repos

        result = obj.public_repos(license="apache-2.0")

        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
