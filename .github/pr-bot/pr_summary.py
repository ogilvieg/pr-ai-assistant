import json
import os
import subprocess
import textwrap
from typing import Tuple

import requests


def get_env_var(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def run_git_diff(base_sha: str, head_sha: str, max_chars: int = 15000) -> str:
    """Return a unified diff between base and head, truncated if too long."""
    try:
        result = subprocess.run(
            ["git", "diff", "--unified=3", base_sha, head_sha],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"git diff failed: {e.stderr}") from e

    diff = result.stdout.strip()
    if not diff:
        return "No changes detected in this diff (empty diff)."

    if len(diff) > max_chars:
        truncated = diff[:max_chars]
        truncated += "\n\n[diff truncated due to length]"
        return truncated

    return diff


def call_openai_chat(diff_text: str) -> str:
    api_key = get_env_var("OPENAI_API_KEY")

    system_message = textwrap.dedent(
        """
        You are a software engineer helping review a GitHub pull request.
        You are given a git diff. Provide a concise, high-signal review summary:
        - Focus on behavior changes, architecture decisions, and risk.
        - Avoid restating every line; group changes logically.
        """
    ).strip()

    user_message = textwrap.dedent(
        f"""
        Here is the git diff between the base and head commits for this pull request:

        ```diff
        {diff_text}
        ```

        Please respond with:

        1. **Summary of Changes** (3–6 bullet points)
        2. **Potential Risks / Breaking Changes**
        3. **Suggested Tests or Validation Steps**

        Keep it concise but concrete. Reference files or functions when useful.
        """
    ).strip()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # You can change the model if you like (e.g., gpt-4o, gpt-4.1-mini)
    payload = {
        "model": "gpt-4.1-mini",
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.2,
    }

    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=60,
    )
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        raise RuntimeError(f"OpenAI API error: {resp.status_code} {resp.text}") from e

    data = resp.json()
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected OpenAI response format: {data}") from e

    return content.strip()


def post_github_comment(body: str) -> None:
    repo = get_env_var("GITHUB_REPOSITORY")
    pr_number = get_env_var("PR_NUMBER")
    token = get_env_var("GITHUB_TOKEN")

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    payload = {"body": body}

    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        raise RuntimeError(
            f"Failed to post GitHub comment: {resp.status_code} {resp.text}"
        ) from e


def main() -> None:
    base_sha = get_env_var("BASE_SHA")
    head_sha = get_env_var("HEAD_SHA")

    print(f"Base SHA: {base_sha}")
    print(f"Head SHA: {head_sha}")

    diff_text = run_git_diff(base_sha, head_sha)
    print("Collected diff; length =", len(diff_text))

    ai_summary = call_openai_chat(diff_text)

    comment_body = textwrap.dedent(
        f"""
        🤖 **AI-generated PR Summary**

        {ai_summary}

        ---

        _This comment was generated automatically by an AI summary bot._
        """
    ).strip()

    post_github_comment(comment_body)
    print("Posted AI summary comment to GitHub PR.")


if __name__ == "__main__":
    main()
