#!/bin/bash
# Deploy LoopedAI Backend to VPS
# Usage: bash deploy.sh
# Idempotent — safe to run multiple times.

set -e

VPS="root@72.61.213.67"
PASS="Emma5cheta5-5"
BASE="/opt/loopedai"
PKG="$BASE/backend"
LOCAL_DIR="$(dirname "$0")"

echo "═══════════════════════════════════════"
echo "  LoopedAI Backend Deploy"
echo "═══════════════════════════════════════"

# 1. Install sshpass if needed
which sshpass > /dev/null 2>&1 || sudo apt-get install -y sshpass
export SSHPASS="$PASS"

# 2. Upload backend files into /opt/loopedai/backend/
echo "📤 Uploading backend files..."
sshpass -e ssh -o StrictHostKeyChecking=no "$VPS" "mkdir -p $PKG"
sshpass -e scp -o StrictHostKeyChecking=no \
    "$LOCAL_DIR/__init__.py" \
    "$LOCAL_DIR/config.py" \
    "$LOCAL_DIR/db.py" \
    "$LOCAL_DIR/rate_limiter.py" \
    "$LOCAL_DIR/llm_client.py" \
    "$LOCAL_DIR/api_server.py" \
    "$LOCAL_DIR/bot.py" \
    "$LOCAL_DIR/admin_cli.py" \
    "$LOCAL_DIR/requirements.txt" \
    "$VPS:$PKG/"
echo " Files uploaded"

# 3. Copy local .env to VPS (only if not already present on VPS)
LOCAL_ENV="$LOCAL_DIR/.env"
if [ -f "$LOCAL_ENV" ]; then
    sshpass -e ssh -o StrictHostKeyChecking=no "$VPS" "test -f $PKG/.env && echo '.env already exists (skipped)' || echo 'uploading .env'"
    HAS_ENV=$(sshpass -e ssh -o StrictHostKeyChecking=no "$VPS" "test -f $PKG/.env && echo yes || echo no")
    if [ "$HAS_ENV" = "no" ]; then
        sshpass -e scp -o StrictHostKeyChecking=no "$LOCAL_ENV" "$VPS:$PKG/.env"
        echo ".env uploaded from local"
    fi
else
    echo "WARNING: No local .env found at $LOCAL_ENV — create it from .env.example"
fi

# 4. Setup Python environment
echo " Setting up Python environment..."
sshpass -e ssh -o StrictHostKeyChecking=no "$VPS" "
    apt-get install -y python3.12-venv python3-pip > /dev/null 2>&1 || true
    cd $BASE
    python3 -m venv venv 2>/dev/null || true
    source venv/bin/activate
    pip install -q -r $PKG/requirements.txt
    echo ' Dependencies installed'
"

# 5. Stop OpenClaw (if running)
echo " Stopping OpenClaw..."
sshpass -e ssh -o StrictHostKeyChecking=no "$VPS" "
    cd /docker/openclaw-io5u && docker compose down 2>/dev/null || true
    echo ' OpenClaw stopped'
"

# 6. Stop any existing bot/api processes
echo "🧹 Cleaning up old processes..."
sshpass -e ssh -o StrictHostKeyChecking=no "$VPS" "
    pkill -f 'uvicorn' 2>/dev/null || true
    pkill -f 'backend.bot' 2>/dev/null || true
    pkill -f 'loopedai_bot' 2>/dev/null || true
    sleep 2
    echo ' Old processes stopped'
"

# 7. Register admin user (idempotent)
echo " Setting up admin user..."
ADMIN_ID=$(sshpass -e ssh -o StrictHostKeyChecking=no "$VPS" "
    cd $BASE && source venv/bin/activate
    export PYTHONPATH=$BASE
    python3 -c '
from backend.db import SQLiteClient
db = SQLiteClient(\"$BASE/loopedai.db\")
db.init_schema()
users = db.list_users()
if not users:
    lid = db.register_user(\"Amari Admin\")
    print(lid)
else:
    print(users[0][\"looped_id\"])
'
")
echo "Admin ID: $ADMIN_ID"

# 8. Start API server + Bot
echo " Starting services..."
sshpass -e ssh -o StrictHostKeyChecking=no "$VPS" "
    cd $BASE && source venv/bin/activate
    export PYTHONPATH=$BASE

    # Start FastAPI backend
    nohup python3 -m uvicorn backend.api_server:app --host 127.0.0.1 --port 8000 > $BASE/api.log 2>&1 &
    sleep 3

    # Verify API is up
    if curl -s http://127.0.0.1:8000/health > /dev/null 2>&1; then
        echo ' API server running'
    else
        echo ' API may still be starting...'
    fi

    # Start Telegram bot
    nohup python3 -m backend.bot > $BASE/bot.log 2>&1 &
    sleep 2
    echo ' Bot started'
"

echo ""
echo "═══════════════════════════════════════"
echo "   DEPLOYMENT COMPLETE"
echo "═══════════════════════════════════════"
echo "  Your LoopedAI ID: $ADMIN_ID"
echo "  Bot: @loopedaibot"
echo "  API: http://127.0.0.1:8000 (VPS local)"
echo "═══════════════════════════════════════"
echo ""
echo "  Test: Open @loopedaibot on Telegram"
echo "  1. Send /start"
echo "  2. Enter ID: $ADMIN_ID"
echo "  3. Ask an immigration question"
echo ""
