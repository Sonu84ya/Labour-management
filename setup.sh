#!/bin/bash
# ============================================================
# GaonKaam – Village Labour Connect
# Complete Setup Script
# ============================================================

set -e
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo "  GaonKaam – Village Labour Connect"
echo "======================================"
echo ""

# --- 1. Python dependencies ---
echo -e "${YELLOW}[1/6] Installing Python dependencies...${NC}"
pip install django pymysql pillow django-cors-headers --break-system-packages -q
echo -e "${GREEN}  Dependencies installed${NC}"

# --- 2. MySQL database ---
echo ""
echo -e "${YELLOW}[2/6] Setting up MySQL database...${NC}"
echo "  • Creating database 'gaonkaam_db' with password 'backend@2024'"

mysql -u root -pbackend@2024 -e "
  CREATE DATABASE IF NOT EXISTS gaonkaam_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  GRANT ALL PRIVILEGES ON gaonkaam_db.* TO 'root'@'localhost' IDENTIFIED BY 'backend@2024';
  FLUSH PRIVILEGES;
" 2>/dev/null || {
  echo -e "${YELLOW}  ⚠  Could not auto-create DB. Please run manually:${NC}"
  echo "     mysql -u root -p"
  echo "     CREATE DATABASE gaonkaam_db CHARACTER SET utf8mb4;"
  echo ""
}
echo -e "${GREEN}  Database ready${NC}"

# --- 3. Migrations ---
echo ""
echo -e "${YELLOW}[3/6] Running migrations...${NC}"
cd "$(dirname "$0")"
python manage.py migrate
echo -e "${GREEN}  Database tables created${NC}"

# --- 4. Static files ---
echo ""
echo -e "${YELLOW}[4/6] Collecting static files...${NC}"
python manage.py collectstatic --noinput -v 0 2>/dev/null || true
mkdir -p static staticfiles media
echo -e "${GREEN}  Static files ready${NC}"

# --- 5. Seed demo data ---
echo ""
echo -e "${YELLOW}[5/6] Seeding demo data...${NC}"
python manage.py seed_data
echo -e "${GREEN}  Demo data loaded${NC}"

# --- 6. Done ---
echo ""
echo "======================================"
echo -e "${GREEN}  GaonKaam is ready to run!${NC}"
echo "======================================"
echo ""
echo "  To start the server:"
echo "    python manage.py runserver 0.0.0.0:8000"
echo ""
echo "  Then open:  http://localhost:8000"
echo ""
echo "  Demo accounts (password: demo1234):"
echo "     ram_shrestha  – Worker & Employer"
echo "     hari_tamang   – Worker"
echo "     sita_rai      – Employer"
echo "     bikram_magar  – Both"
echo ""
echo "  Admin panel:  http://localhost:8000/admin"
echo "     admin / admin123"
echo ""
