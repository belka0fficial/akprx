#!/bin/bash
set -e
echo "Installing akprx (unsigned repo)..."
echo "deb [trusted=yes] https://belka0fficial.github.io/akprx stable main" | sudo tee /etc/apt/sources.list.d/akprx.list
sudo apt-get update
sudo apt-get install -y akprx
echo "Done. Run: akprx status"
