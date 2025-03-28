pip freeze | xargs pip uninstall -y
pip install pip-autoremove
rm requirements.txt