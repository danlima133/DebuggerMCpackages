echo "Setting up environment"

python -m venv env
source env/bin/activate

echo "Installing dependencies"

pip install -r requirements.txt

pip install pip-autoremove

