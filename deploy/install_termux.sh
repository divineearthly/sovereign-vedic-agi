#!/data/data/com.termux/files/usr/bin/bash

echo "🕉️ Installing Vedic AGI on Termux..."

# Update and install dependencies
pkg update -y
pkg install -y python clang libxml2 libxslt

# Install Python packages
pip install torch numpy

# Clone Vedic AGI
cd ~
git clone https://github.com/divineearthly/sovereign-vedic-agi
cd sovereign-vedic-agi

# Install Vedic package
pip install -e .

# Create launcher
cat > ~/../usr/bin/vedic-agi << 'LAUNCHER'
#!/data/data/com.termux/files/usr/bin/bash
cd ~/sovereign-vedic-agi
python -m vedic_agi.cli.main "$@"
LAUNCHER

chmod +x ~/../usr/bin/vedic-agi

echo "✅ Vedic AGI installed!"
echo "Run: vedic-agi --attention --seq-len 4096"
