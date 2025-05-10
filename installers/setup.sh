echo "Setting up environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r ../requirements.txt
echo "Setup complete. Run your assistant with: source .venv/bin/activate && python3 main.py"
