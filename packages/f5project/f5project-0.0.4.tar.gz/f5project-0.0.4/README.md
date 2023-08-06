# F5 Project

Finlab Fugle for financial freedom.

# Install

```
pip install f5project
```

# Why?

This library makes it easier to use Finlab/Fugle with other tools together, such as GCF and Github Action.

When deploying your code on GCF. Some troubles come up and you can't just do it like you do on your local machine. This library helps you to solve these problems. It helps you:

- Read config from json file or environment variables.
- Extract Fugle config and certificate from json file or environment variables, dynamically generate them as needed.
- Login Finlab/Fugle with config, which is a little bit annoying because Fugle SDK asks them as files.
- Provide a decorator to make your function a GCF endpoint, without worrying about the request/response format.
- Simulate GCF request locally.
- Sync Github secrets with local config, make CI/CD easier.

Then you can focus on your trading strategy and iterate faster.

# Usages

main.py

```python
"""Main entrypoint of the project.

- This file is the entrypoint of Google Cloud Function.
- It also provides a CLI to run the function locally.
"""
from pathlib import Path
from typing import cast

from finlab.online.order_executor import OrderExecutor, Position

import my_strategies
from f5project import F5Project, F5ProjectConfig

BASE_DIR = Path(__file__).resolve().parent


# Let `F5Project` handle all the boring stuff.
project = F5Project(config=F5ProjectConfig.from_json_or_env(BASE_DIR / ".secrets" / "index.json"))


# Decorate our `create_orders` function to make it a Google Cloud Function.
@project.gcf_endpoint
def create_orders(view_only: bool = True, fund: int = 30000, odd_lot: bool = True) -> list[dict]:
    # Login project first
    project.login()
    # Get backtest report with some strategy
    report = my_strategies.tibetan_mastiff()
    # Use it to create stock position we should own
    position = Position.from_report(report, fund, odd_lot=odd_lot)
    # Get records with `view_only=True` to return it later
    order_executor = OrderExecutor(position, project.get_fugle_account())
    records = cast(list[dict], order_executor.create_orders(view_only=True))
    # If `view_only=False`, actually create the orders.
    if not view_only:
        order_executor.create_orders(view_only=False)
    return records


if __name__ == "__main__":
    # This makes it possible to develop locally. See the `run` method for more details.
    project.run_locally(with_server=True, params={"view_only": True, "fund": 10000, "odd_lot": True})
```

scripts/sync_github_secrets.py

```python
#!.venv/bin/python
"""Sync secrets from local to GitHub.

Install it as a Git pre-push hook by:
`chmod 755 scripts/sync_github_secrets.py ln -s ../../scripts/sync_github_secrets.py .git/hooks/pre-push`

Notes:
1. When you `git push`, it will sync secrets from local to GitHub.
2. It uses `.venv/bin/python` as interpreter, so make sure you have created a virtual environment.
3. Uninstall it by `rm .git/hooks/pre-push`.
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


if __name__ == "__main__":
    sys.path.insert(0, str(BASE_DIR))
    from main import project

    project.sync_github_secrets()

```

You'll also want a CI/CD pipeline to deploy your function to GCF. Here's an example of Github Actions:

.github/workflows/main.yml

```yaml
on:
  push:
    branches:
      - main

jobs:
  deploy-to-gcf:
    name: "Deploy to Google Cloud Function"
    runs-on: "ubuntu-latest"
    permissions:
      contents: "read"
      id-token: "write"

    steps:
      - id: "checkout"
        uses: "actions/checkout@v3"

      - id: "auth"
        uses: "google-github-actions/auth@v1"
        with:
          credentials_json: "${{ secrets.GCF_SERVICE_ACCOUNT }}"

      - id: "deploy"
        uses: "google-github-actions/deploy-cloud-functions@v1"
        with:
          name: "${{ secrets.GCF_FUNCTION_TARGET }}"
          entry_point: "${{ secrets.GCF_FUNCTION_TARGET }}"
          ingress_settings: "ALLOW_ALL"
          runtime: "python310"
          memory_mb: "2048"
          timeout: 300
          env_vars: >
            FINLAB_API_TOKEN=${{ secrets.FINLAB_API_TOKEN }},
            FUGLE_ACCOUNT=${{ secrets.FUGLE_ACCOUNT }},
            FUGLE_PASSWORD=${{ secrets.FUGLE_PASSWORD }},
            FUGLE_CERT=${{ secrets.FUGLE_CERT }},
            FUGLE_CERT_PASSWORD=${{ secrets.FUGLE_CERT_PASSWORD }},
            FUGLE_API_ENTRY=${{ secrets.FUGLE_API_ENTRY }},
            FUGLE_API_KEY=${{ secrets.FUGLE_API_KEY }},
            FUGLE_API_SECRET=${{ secrets.FUGLE_API_SECRET }},
            FUGLE_MARKET_API_KEY=${{ secrets.FUGLE_MARKET_API_KEY }},
```

# TODO

- Use `pipx` to make it easier to have a quickstart template.
- Dynamically generate `CI/CD` pipeline YAML file, so we can focus on the code.
