# Release Documentation

## PyPI Publishing Setup

To configure automated publishing to PyPI when a release tag is pushed, follow these steps to set up the necessary API tokens and secrets.

### 1. Create a PyPI API Token
1. Go to [PyPI Account Token Management](https://pypi.org/manage/account/token/).
2. Create a new API token.
3. The token scope should be set for the entire account (or restricted to the specific project once it has been created on PyPI).

### 2. Add Token as a GitHub Repository Secret
1. Go to your repository on GitHub.
2. Navigate to **Settings** → **Secrets and variables** → **Actions**.
3. Click on the **New repository secret** button.
4. Set the **Name** to: `PYPI_API_TOKEN`
5. Set the **Value** to the PyPI API token you generated.
6. Click **Add secret** to save.

### 3. Create and Push a Release Tag
The PyPI publish workflow is configured to trigger automatically when a version Git tag is pushed.

To create and push a release tag, run the following commands:

```bash
git tag v0.0.1
git push origin v0.0.1
```

> [!NOTE]
> The tag version should exactly match the `version` configured in `pyproject.toml` (e.g., `version = "0.0.1"` for the tag `v0.0.1`).
