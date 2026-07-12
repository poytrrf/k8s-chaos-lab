import os
import time
import logging

import redis
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("service-b")

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))

PG_HOST = os.environ.get("PG_HOST", "postgres")
PG_PORT = os.environ.get("PG_PORT", "5432")
PG_DB = os.environ.get("PG_DB", "appdb")
PG_USER = os.environ.get("PG_USER", "appuser")
PG_PASSWORD = os.environ.get("PG_PASSWORD", "changeme")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, socket_connect_timeout=2, socket_timeout=2)


def get_pg_conn():
    return psycopg2.connect(
        host=PG_HOST, port=PG_PORT, dbname=PG_DB,
        user=PG_USER, password=PG_PASSWORD, connect_timeout=3,
    )


@app.route("/")
def index():
    return jsonify({"service": "service-b", "message": "hello from service-b"})


@app.route("/healthz")
def healthz():
    # liveness: 只判断进程本身是否存活，不做外部依赖检查
    return jsonify({"status": "ok"}), 200


@app.route("/readyz")
def readyz():
    # readiness: 检查关键依赖是否可用
    checks = {}
    ok = True

    try:
        r.ping()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = f"fail: {e}"
        ok = False

    try:
        conn = get_pg_conn()
        conn.close()
        checks["postgres"] = "ok"
    except Exception as e:
        checks["postgres"] = f"fail: {e}"
        ok = False

    status_code = 200 if ok else 503
    return jsonify({"status": "ready" if ok else "not_ready", "checks": checks}), status_code


@app.route("/work")
def work():
    # 模拟一次真实业务请求：写redis + 查pg
    start = time.time()
    r.incr("request_count")
    try:
        conn = get_pg_conn()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.fetchone()
        cur.close()
        conn.close()
    except Exception as e:
        log.error(f"pg error: {e}")
        return jsonify({"error": str(e)}), 500

    elapsed = time.time() - start
    return jsonify({"service": "service-b", "elapsed_ms": round(elapsed * 1000, 2)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
