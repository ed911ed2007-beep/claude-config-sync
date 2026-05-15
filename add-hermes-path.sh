#!/bin/bash
# 加入 Hermes node 到 PATH
echo '' >> /home/edward/.bashrc
echo '# Hermes node (includes claude, codex, opencode)' >> /home/edward/.bashrc
echo 'export PATH="$HOME/.hermes/node/bin:$PATH"' >> /home/edward/.bashrc
echo 'PATH entry added:'
tail -4 /home/edward/.bashrc
