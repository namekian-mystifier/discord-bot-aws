# Discord Summarizing Bot for AWS EC2 Hosting
## What it is
This bot uses the Discord Gateway API and (freely available) LLMs to summarize the chat.

## How to install it
1. Clone the repo on a Ubuntu EC2 instance with an open HTTPS (443) port. It should run on any linux distro, but the setup steps in `setup.sh` would change.
2. Follow the setup script `setup.sh` to install the dependencies.
4. Set the parameters as a StringList in SSM Parameter Store. The order and formatting required can be found near the top of `main.py`. If you do not want to use Parameter Store, replace this part e.g. with environment variables or hard coded values. The important thing is that the variables in `config.py` get set near the top of `main.py`.
5. If using Parameter Store, you must set the required environment variables for AWS Region and parameter name. You can find their name near the top of `main.py`.
6. Run it with `python main.py`.
7. Make sure you have everything set up on the Discord Developer Portal and that you invite the bot on the server. The command is `/summarize`.

## Is it a cryptominer?
Perhaps??
