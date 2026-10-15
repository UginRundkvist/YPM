#!/usr/bin/env bash
# Поднимает Oracle в Docker и заливает схему ED_SALES.
# Запускать из той папки, где лежит ed_sales_oracle.sql:   bash install_oracle.sh
set -euo pipefail
cd "$(dirname "$0")"

SQL=ed_sales_oracle.sql
NAME=oracle-bd
IMAGE=gvenzl/oracle-free:23-slim
PASS=oracle

[ -f "$SQL" ] || { echo "Рядом со скриптом нет файла $SQL"; exit 1; }

# --- 1. Docker ---
if ! command -v docker >/dev/null 2>&1; then
  echo ">>> Ставлю Docker..."
  sudo apt-get update
  sudo apt-get install -y docker.io
  sudo systemctl enable --now docker
  sudo usermod -aG docker "$USER"
  echo
  echo ">>> Docker поставлен, но права на него появятся только после перелогина."
  echo ">>> Выполни:  newgrp docker   и запусти этот скрипт ещё раз."
  exit 0
fi
docker info >/dev/null 2>&1 || { echo "Docker есть, но демон не отвечает. Запусти: sudo systemctl start docker"; exit 1; }

# --- 2. Контейнер ---
echo ">>> Поднимаю Oracle (образ ~1.5 ГБ, качается один раз)..."
docker rm -f "$NAME" >/dev/null 2>&1 || true
docker run -d --name "$NAME" -p 1521:1521 -e ORACLE_PASSWORD="$PASS" "$IMAGE" >/dev/null

echo -n ">>> Жду готовности базы (первый запуск 1-3 минуты)"
for i in $(seq 1 120); do
  if docker logs "$NAME" 2>&1 | grep -q "DATABASE IS READY TO USE"; then echo " готово"; break; fi
  sleep 5; echo -n "."
  if [ "$i" = 120 ]; then echo; echo "Не дождался. Смотри: docker logs $NAME"; exit 1; fi
done

# --- 3. Схема и данные ---
echo ">>> Заливаю схему ED_SALES..."
docker cp "$SQL" "$NAME":/tmp/ed_sales.sql
docker exec -e NLS_LANG=.AL32UTF8 -i "$NAME" \
  sqlplus -S "system/$PASS@localhost:1521/FREEPDB1" @/tmp/ed_sales.sql

cat <<'MSG'

=========================================================
Готово. Подключение из SQL Developer:

  Username : ED_SALES
  Password : ed_sales
  Hostname : localhost
  Port     : 1521
  тип      : Service name  (НЕ SID)
  Service  : FREEPDB1

Админ (если понадобится):  SYSTEM / oracle

Управление контейнером:
  docker stop oracle-bd     # остановить
  docker start oracle-bd    # включить снова (данные на месте)
  docker rm -f oracle-bd    # снести совсем
=========================================================
MSG
