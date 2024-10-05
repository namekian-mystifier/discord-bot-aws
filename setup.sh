sudo yum groupinstall -y "Development Tools"
sudo dnf install -y virtualenv
git clone https://github.com/namekian-mystifier/discord-summarizer-bot
cd discord-summarizer-bot
git checkout lambda-deployment
virtualenv venv --python=3.9
source venv/bin/activate
pip install -r requirements.txt
python