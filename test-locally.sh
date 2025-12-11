#!/bin/bash

# Local testing script for PR AI Assistant
# This script sets up environment variables and runs the PR summary bot locally

set -e  # Exit on error

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}PR AI Assistant - Local Test Script${NC}"
echo "===================================="
echo ""

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo -e "${YELLOW}Warning: Virtual environment not detected.${NC}"
    echo "Activate it with: source venv/bin/activate"
    echo ""
fi

# Required environment variables with prompts
if [[ -z "$OPENAI_API_KEY" ]]; then
    echo -e "${RED}Error: OPENAI_API_KEY is not set${NC}"
    echo "Set it with: export OPENAI_API_KEY='your-key-here'"
    exit 1
fi

if [[ -z "$GITHUB_TOKEN" ]]; then
    echo -e "${YELLOW}Warning: GITHUB_TOKEN is not set${NC}"
    echo "Enter your GitHub token (or press Enter to use a default test value):"
    read -r token_input
    if [[ -n "$token_input" ]]; then
        export GITHUB_TOKEN="$token_input"
    else
        export GITHUB_TOKEN="test-token"
        echo -e "${YELLOW}Using test token (posting comment will fail)${NC}"
    fi
fi

# Set default test values if not provided
export PR_NUMBER="${PR_NUMBER:-1}"
export GITHUB_REPOSITORY="${GITHUB_REPOSITORY:-ogilvieg/pr-ai-assistant}"

# Prompt for commit SHAs
if [[ -z "$BASE_SHA" ]]; then
    echo ""
    echo "Enter BASE_SHA (the commit to compare from):"
    echo "Tip: Use 'git log --oneline -10' to see recent commits"
    read -r BASE_SHA
    if [[ -z "$BASE_SHA" ]]; then
        echo -e "${RED}Error: BASE_SHA is required${NC}"
        exit 1
    fi
    export BASE_SHA
fi

if [[ -z "$HEAD_SHA" ]]; then
    echo ""
    echo "Enter HEAD_SHA (the commit to compare to):"
    read -r HEAD_SHA
    if [[ -z "$HEAD_SHA" ]]; then
        echo -e "${RED}Error: HEAD_SHA is required${NC}"
        exit 1
    fi
    export HEAD_SHA
fi

# Display configuration
echo ""
echo -e "${GREEN}Configuration:${NC}"
echo "  OPENAI_API_KEY: ${OPENAI_API_KEY:0:8}..."
echo "  GITHUB_TOKEN: ${GITHUB_TOKEN:0:8}..."
echo "  PR_NUMBER: $PR_NUMBER"
echo "  GITHUB_REPOSITORY: $GITHUB_REPOSITORY"
echo "  BASE_SHA: $BASE_SHA"
echo "  HEAD_SHA: $HEAD_SHA"
echo ""

# Confirm before running
read -p "Proceed with test? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

echo ""
echo -e "${GREEN}Running PR summary bot...${NC}"
echo ""

# Run the Python script
python .github/pr-bot/pr_summary.py

echo ""
echo -e "${GREEN}✓ Script completed successfully!${NC}"
