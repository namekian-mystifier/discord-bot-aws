git clone https://github.com/namekian-mystifier/discord-bot-aws
cd discord-bot-aws
sudo apt update
sudo apt install -y virtualenv
virtualenv venv --python=3.12
source venv/bin/activate
pip install -r requirements.txt
