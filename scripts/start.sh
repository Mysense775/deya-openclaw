#!/bin/bash
# Start script for Deya OpenClaw Instance

set -e

echo "🌺 Starting Deya OpenClaw Instance..."
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Paths
WORKSPACE="${HOME}/.openclaw/workspace"
SKILLS_DIR="${WORKSPACE}/skills"
LOGS_DIR="${HOME}/.openclaw/logs"

# Create logs directory
mkdir -p "${LOGS_DIR}"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Shutting down...${NC}"
    
    if [ -n "$DASHBOARD_PID" ]; then
        kill $DASHBOARD_PID 2>/dev/null || true
        echo "   Dashboard stopped"
    fi
    
    if [ -n "$GATEWAY_PID" ]; then
        kill $GATEWAY_PID 2>/dev/null || true
        echo "   Gateway stopped"
    fi
    
    exit 0
}

trap cleanup SIGINT SIGTERM

# Check if already running
if [ -f "${HOME}/.openclaw/dashboard.pid" ]; then
    OLD_PID=$(cat "${HOME}/.openclaw/dashboard.pid")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Dashboard already running (PID: $OLD_PID)${NC}"
        echo "   Restarting..."
        kill "$OLD_PID" 2>/dev/null || true
        sleep 2
    fi
fi

# Start Dashboard
echo -e "${BLUE}🎛️  Starting Dashboard...${NC}"
cd "${SKILLS_DIR}/deya-dashboard"
python3 main.py > "${LOGS_DIR}/dashboard.log" 2>&1 &
DASHBOARD_PID=$!
echo $DASHBOARD_PID > "${HOME}/.openclaw/dashboard.pid"
echo -e "${GREEN}   Dashboard PID: $DASHBOARD_PID${NC}"

# Wait for dashboard to be ready
echo -n "   Waiting for dashboard to be ready..."
for i in {1..30}; do
    if curl -fsSL http://localhost:8001 > /dev/null 2>&1; then
        echo -e " ${GREEN}✅${NC}"
        break
    fi
    sleep 1
    echo -n "."
done

# Start OpenClaw Gateway (if installed)
if command -v openclaw &> /dev/null; then
    echo -e "${BLUE}💬 Starting OpenClaw Gateway...${NC}"
    openclaw gateway start > "${LOGS_DIR}/gateway.log" 2>&1 &
    GATEWAY_PID=$!
    echo $GATEWAY_PID > "${HOME}/.openclaw/gateway.pid"
    echo -e "${GREEN}   Gateway PID: $GATEWAY_PID${NC}"
else
    echo -e "${YELLOW}   ⚠️  OpenClaw not found, skipping gateway${NC}"
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                        ║${NC}"
echo -e "${GREEN}║  ✅  DEYA INSTANCE RUNNING!  ✅                      ║${NC}"
echo -e "${GREEN}║                                                        ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}🌐 Dashboard:${NC} http://localhost:8001"
echo -e "${BLUE}💬 Gateway:${NC}  http://localhost:8000"
echo ""
echo -e "${YELLOW}📋 Logs:${NC}"
echo -e "   Dashboard: ${LOGS_DIR}/dashboard.log"
echo -e "   Gateway:   ${LOGS_DIR}/gateway.log"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
echo ""

# Keep script running
wait
