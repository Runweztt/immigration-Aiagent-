#!/bin/bash
# Diagnostic script for OpenClaw VPS
apt-get install -y sshpass > /dev/null 2>&1

OUTPUT_FILE="/mnt/c/Users/Amari/healthcare-aigent/vps_diagnostic.txt"

sshpass -p 'Emma5//cheta##' ssh -o StrictHostKeyChecking=no root@72.61.213.67 bash <<'REMOTE'
echo "=== DOCKER CONTAINERS ==="
docker ps -a 2>&1
echo ""
echo "=== ROOT HOME ==="
ls -la /root/ 2>&1
echo ""
echo "=== FIND OPENCLAW ==="
find / -maxdepth 4 -type d -name "*openclaw*" 2>/dev/null
find / -maxdepth 4 -type d -name "*looped*" 2>/dev/null
echo ""
echo "=== DOCKER COMPOSE FILES ==="
find / -maxdepth 4 -name "docker-compose*" 2>/dev/null | head -10
echo ""
echo "=== ENV FILES ==="
find / -maxdepth 4 -name ".env" 2>/dev/null | grep -v proc | head -10
echo ""
echo "=== DOCKER LOGS (last container) ==="
LAST=$(docker ps -aq | head -1)
if [ -n "$LAST" ]; then
  docker logs "$LAST" --tail 30 2>&1
else
  echo "No containers found"
fi
echo ""
echo "=== LISTENING PORTS ==="
ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null
REMOTE
