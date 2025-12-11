# PR AI Assistant

An automated GitHub Actions bot that uses OpenAI's GPT models to generate intelligent pull request summaries. The bot analyzes git diffs and provides concise, high-signal code reviews focusing on behavior changes, architecture decisions, and potential risks.

## Features

- 🤖 **Automated PR Reviews**: Automatically comments on pull requests with AI-generated summaries
- 📊 **Smart Analysis**: Focuses on behavior changes, architecture decisions, and risks
- 🔍 **Structured Feedback**: Provides summary of changes, potential risks, and suggested validation steps
- ⚡ **GitHub Actions Integration**: Runs automatically on PR open, reopen, and synchronize events

## Setup

### Prerequisites

- Python 3.11 or higher
- OpenAI API key
- GitHub repository with Actions enabled

### Local Development Setup

1. **Clone the repository**:

   ```bash
   git clone <your-repo-url>
   cd pr-ai-assistant
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Upgrade pip**:

   ```bash
   pip install --upgrade pip
   ```

4. **Install dependencies**:

   ```bash
   pip install -r .github/pr-bot/requirements.txt
   ```

5. **Set up environment variables** (for local testing):
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export GITHUB_TOKEN="your-github-token"
   export PR_NUMBER="123"
   export BASE_SHA="base-commit-sha"
   export HEAD_SHA="head-commit-sha"
   export GITHUB_REPOSITORY="owner/repo"
   ```

### GitHub Repository Setup

1. **Add OpenAI API Key as a GitHub Secret**:

   - Go to your repository Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `OPENAI_API_KEY`
   - Value: Your OpenAI API key

2. **Enable GitHub Actions**:

   - The workflow is already configured in `.github/workflows/pr-ai-summary.yml`
   - It will automatically run on pull requests

3. **Verify Permissions**:
   - The workflow already has the necessary permissions configured:
     - `contents: read` - to read repository code
     - `pull-requests: write` - to post comments on PRs

## Usage

### Automatic Mode (Recommended)

Once set up, the bot automatically runs on:

- Pull request opened
- Pull request reopened
- Pull request synchronized (new commits pushed)

The bot will:

1. Fetch the git diff between base and head commits
2. Send the diff to OpenAI for analysis
3. Post a comment on the PR with the AI-generated summary

### Manual Testing

To test the bot locally:

```bash
# Ensure you're in the virtual environment
source venv/bin/activate

# Set required environment variables (see Setup section)
export OPENAI_API_KEY="..."
export GITHUB_TOKEN="..."
export PR_NUMBER="..."
export BASE_SHA="..."
export HEAD_SHA="..."
export GITHUB_REPOSITORY="..."

# Run the script
python .github/pr-bot/pr_summary.py
```

## Configuration

### Customizing the AI Model

Edit `.github/pr-bot/pr_summary.py` to change the OpenAI model:

```python
payload = {
    "model": "gpt-4o",  # Change this to your preferred model
    "messages": [...],
    "temperature": 0.2,
}
```

Available models:

- `gpt-4o` - Most capable, higher cost
- `gpt-4.1-mini` - Balanced (default)
- `gpt-3.5-turbo` - Faster, lower cost

### Adjusting Diff Size Limit

By default, diffs are truncated at 15,000 characters. To change this:

```python
def run_git_diff(base_sha: str, head_sha: str, max_chars: int = 15000) -> str:
    # Change max_chars to your preferred limit
```

### Customizing the Review Prompt

Edit the `system_message` and `user_message` in the `call_openai_chat()` function to adjust the review style and focus areas.

## Project Structure

```
pr-ai-assistant/
├── .github/
│   ├── pr-bot/
│   │   ├── pr_summary.py      # Main bot script
│   │   └── requirements.txt   # Python dependencies
│   └── workflows/
│       └── pr-ai-summary.yml  # GitHub Actions workflow
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## Dependencies

- `requests==2.32.3` - For making HTTP requests to OpenAI and GitHub APIs

## Environment Variables

| Variable            | Description                             | Required |
| ------------------- | --------------------------------------- | -------- |
| `OPENAI_API_KEY`    | Your OpenAI API key                     | ✅ Yes   |
| `GITHUB_TOKEN`      | GitHub token (auto-provided by Actions) | ✅ Yes   |
| `PR_NUMBER`         | Pull request number                     | ✅ Yes   |
| `BASE_SHA`          | Base commit SHA                         | ✅ Yes   |
| `HEAD_SHA`          | Head commit SHA                         | ✅ Yes   |
| `GITHUB_REPOSITORY` | Repository in format `owner/repo`       | ✅ Yes   |

## Troubleshooting

### Bot not posting comments

- Verify `OPENAI_API_KEY` is set in repository secrets
- Check that the workflow has `pull-requests: write` permission
- Review the Actions logs for error messages

### API errors

- Ensure your OpenAI API key is valid and has sufficient credits
- Check the model name is correct and available to your API key
- Verify network connectivity to OpenAI and GitHub APIs

### Diff too large

- Increase the `max_chars` parameter in `run_git_diff()`
- Consider breaking large PRs into smaller ones

## Contributing

1. Create a feature branch
2. Make your changes
3. Test locally
4. Submit a pull request (and watch the bot review it! 🤖)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues or questions, please open an issue in the GitHub repository.
