# Contributing to FoodWise

Thank you for your interest in contributing to FoodWise.

FoodWise is a food-planning and budgeting application that brings together food budgets, savings, food-plan recommendations, food packages, and an assistant interface.

## Before You Start

- Read the root [README](README.md) for the project overview.
- Follow the [development setup guide](docs/development-setup.md) to configure your environment.
- Review the [testing guide](docs/testing.md) before submitting changes.
- For assistant-related work, consult the [N-ATLaS integration guide](docs/n-atlas-integration.md).

## Development Principles

Contributions should aim to:

- Keep changes focused and easy to review.
- Use clear names and maintainable code.
- Validate inputs and handle errors appropriately.
- Avoid exposing credentials, personal data, or other secrets.
- Update documentation when behaviour or setup instructions change.
- Avoid claiming that features are operational without verifying them.

## Suggested Workflow

1. Review the existing implementation before changing it.
2. Create a branch for your work.
3. Make a focused change.
4. Run the relevant tests and checks.
5. Update documentation where necessary.
6. Review your changes for accidental secrets or unrelated files.
7. Submit a pull request with a clear explanation of the change and its verification.

## Branching

Use descriptive branch names, for example:

- `feature/food-plan-improvements`
- `fix/assistant-timeout`
- `docs/setup-instructions`

## Testing Expectations

For backend changes, run the relevant Python tests.

For frontend changes, run the available lint and production-build checks.

For API or assistant changes, test the affected request flow and error handling where possible.

Include the commands you ran and their results when describing a contribution. If a check could not be run, state that clearly.

## Security and Configuration

- Never commit `.env` files, credentials, access tokens, or private keys.
- Do not commit large model-weight files.
- Use placeholder values in examples.
- Report security concerns responsibly rather than publishing sensitive details.

## Documentation

Keep the documentation aligned with the current code. Distinguish between implemented features, tested behaviour, and planned functionality.

## Questions and Suggestions

When reporting a bug or proposing an improvement, provide enough context to understand the issue, the expected behaviour, and the steps needed to reproduce it. Remove secrets and personal information from logs before sharing them.

Thank you for helping improve FoodWise.