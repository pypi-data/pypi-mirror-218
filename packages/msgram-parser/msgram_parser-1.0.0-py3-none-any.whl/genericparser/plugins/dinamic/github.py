import os
from genericparser.plugins.domain.generic_class import GenericStaticABC
import requests


class ParserGithub(GenericStaticABC):
    token = None

    def __init__(self, token=None):
        self.token = token

    def _make_request(self, url, token=None):
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if token:
            headers["Authorization"] = (f"Bearer {token}",)
        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            print("error making request to github api in url: ", url, e)
        return response.json() if response.status_code == 200 else {}

    # Get statistics metrics functions
    def _get_statistics_weekly_code_frequency(self, base_url, token=None):
        values = [0] * 7
        metrics = [
            "commits_on_sunday",
            "commits_on_monday",
            "commits_on_tuesday",
            "commits_on_wednesday",
            "commits_on_thursday",
            "commits_on_friday",
            "commits_on_saturday",
        ]
        url = f"{base_url}/stats/punch_card"
        response = self._make_request(url, token)
        for commit_count in response or []:
            values[commit_count[0]] += commit_count[2]

        return {"metrics": metrics, "values": values}

    # Get statistics metrics functions
    def _get_statistics_weekly_commit_activity(self, base_url, token=None):
        values = [0] * 7
        metrics = [
            "commits_on_sunday",
            "commits_on_monday",
            "commits_on_tuesday",
            "commits_on_wednesday",
            "commits_on_thursday",
            "commits_on_friday",
            "commits_on_saturday",
        ]
        url = f"{base_url}/stats/code_frequency"
        response = self._make_request(url, token)
        for commit_count in response or []:
            values[commit_count[0]] += commit_count[2]

        return {"metrics": metrics, "values": values}

    def _get_pull_metrics_by_threshold(self, base_url, token=None):
        values = []
        metrics = [
            "issue_url",
            "commits_url",
            "state",
            "open_issues",
            "closed_issues",
            "created_at",
            "updated_at",
            "closed_at",
            "merged_at",
        ]
        url = f"{base_url}/pulls"
        response = self._make_request(url, token)
        pull_requests = response if isinstance(response, list) else []
        total_issues = len(pull_requests)
        resolved_issues = sum(1 for pr in pull_requests if pr["state"] == "closed")

        values.extend(
            [
                total_issues,
                resolved_issues,
                resolved_issues / total_issues if total_issues > 0 else 0,
            ]
        )

        return {
            "metrics": metrics + ["total_issues", "resolved_issues", "resolved_ratio"],
            "values": values,
        }

        # Get pull metrics

    def _get_pull_metrics(self, base_url, token=None):
        values = []
        metrics = [
            "issue_url",
            "commits_url",
            "state",
            "open_issues",
            "closed_issues",
            "created_at",
            "updated_at",
            "closed_at",
            "merged_at",
        ]
        url = f"{base_url}/pulls"
        response = self._make_request(url, token)
        pull_requests = response if isinstance(response, list) else []

        for pull_request in pull_requests:
            values.extend([pull_request.get(metric, None) for metric in metrics])
        return {"metrics": metrics, "values": values}

    # Get statistics metrics
    def _get_statistics_metrics(self, base_url, token=None):
        return {
            **self._get_statistics_weekly_code_frequency(base_url),
        }

    def _get_all_pull_metrics(self, base_url, token=None):
        values = []
        metrics = [
            "issue_url",
            "commits_url",
            "state",
            "open_issues",
            "closed_issues",
            "created_at",
            "updated_at",
            "closed_at",
            "merged_at",
        ]
        url = f"{base_url}/pulls?state=all"  # Fetch all pull requests (open and closed)
        response = self._make_request(url, token)
        pull_requests = response if isinstance(response, list) else []

        for pull_request in pull_requests:
            metric_values = [pull_request.get(metric, None) for metric in metrics]
            values.append(metric_values)

        return {"metrics": metrics, "values": values}

    # Get comunity metrics
    def _get_comunity_metrics(self, base_url, token=None):
        values = []
        metrics = [
            "health_percentage",
            "updated_at",
            "created_at",
            "watchers_count",
            "forks_count",
            "open_issues_count",
            "forks",
            "open_issues",
            "watchers",
            "subscribers_count",
            "size",
        ]
        url = f"{base_url}/community/profile"
        response = {
            **self._make_request(base_url, token),
            **self._make_request(url, token),
        }
        for metric in metrics:
            values.append(response.get(metric, None))

        return {"metrics": metrics, "values": values}

    def extract(self, input_file):
        token_from_github = (
            input_file.get("token", None)
            if type(input_file) == dict
            else None or os.environ.get("GITHUB_TOKEN", None) or self.token
        )
        repository = (
            input_file.get("repository", None)
            if (type(input_file) == dict)
            else input_file
        )
        metrics = []
        keys = repository
        values = []
        owner, repository_name = repository.split("/")
        url = f"https://api.github.com/repos/{owner}/{repository_name}"

        # Get comunity metrics
        return_of_comunity_metrics = self._get_comunity_metrics(url, token_from_github)
        metrics.extend(return_of_comunity_metrics["metrics"])
        values.extend(return_of_comunity_metrics["values"])

        # Get statistics metrics
        return_of_statistics_metrics = self._get_statistics_metrics(
            url, token_from_github
        )
        metrics.extend(return_of_statistics_metrics["metrics"])
        values.extend(return_of_statistics_metrics["values"])

        return_of_pull_metrics = self._get_pull_metrics(url, token_from_github)
        metrics.extend(return_of_pull_metrics["metrics"])
        values.extend(return_of_pull_metrics["values"])

        return_of_get_all_pull_metrics = self._get_all_pull_metrics(
            url, token_from_github
        )
        metrics.extend(return_of_get_all_pull_metrics["metrics"])
        values.extend(return_of_get_all_pull_metrics["values"])

        return_of_get_statistics_weekly_commit_activity = (
            self._get_statistics_weekly_commit_activity(url, token_from_github)
        )
        metrics.extend(return_of_get_statistics_weekly_commit_activity["metrics"])
        values.extend(return_of_get_statistics_weekly_commit_activity["values"])

        return_of_get_pull_metrics_by_threshold = self._get_pull_metrics_by_threshold(
            url, token_from_github
        )
        metrics.extend(return_of_get_pull_metrics_by_threshold["metrics"])
        values.extend(return_of_get_pull_metrics_by_threshold["values"])

        return {"metrics": metrics, "values": values, "file_paths": keys}


def main():
    return ParserGithub()
