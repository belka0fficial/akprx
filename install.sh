#!/bin/bash
set -e
echo "Installing akprx..."
curl -fsSL https://belka0fficial.github.io/akprx/KEY.gpg | sudo tee /usr/share/keyrings/akprx.gpg > /dev/null
echo "deb [signed-by=/usr/share/keyrings/akprx.gpg] https://belka0fficial.github.io/akprx stable main" | sudo tee /etc/apt/sources.list.d/akprx.list
sudo apt-get update
sudo apt-get install -y akprx
echo "Done. Run: akprx status"
