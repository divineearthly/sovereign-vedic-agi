#!/bin/bash
# 🕉 VEDIC OS — Minimal Sovereign Boot
# Place in /etc/init.d/ or systemd for auto-start

echo "╔══════════════════════════════════╗"
echo "║  🕉 VEDIC OS BOOTING...           ║"
echo "╚══════════════════════════════════╝"

# Mount chitta memory
mount -t tmpfs chitta /mnt/chitta 2>/dev/null || mkdir -p /mnt/chitta

# Start Vedic AGI daemon
cd /home/vedic/sovereign-vedic-agi
./vedic_agi --daemon --port 8000 &
./chitta_memory --load /mnt/chitta/ &
./vedarta --serve &

# Display status
echo "  ✓ Vedic AGI:  http://0.0.0.0:8000"
echo "  ✓ Chitta:     /mnt/chitta/"
echo "  ✓ VedaRta:    .vr runtime active"
echo "  ✓ Indra's Net: 8 nodes connected"
echo ""
echo "🕉 Sovereign computing environment ready."
echo "   No Google. No cloud. No tracking."
echo "   Just pure Vedic intelligence."
