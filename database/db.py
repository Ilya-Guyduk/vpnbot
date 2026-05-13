import sqlite3
import logging
from contextlib import contextmanager
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
DB_PATH = "vpn_bot.db"


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _migrate(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
    if not cur.fetchone():
        return

    existing = {row[1] for row in cur.execute("PRAGMA table_info(orders)")}
    migrations = [
        ("amount_stars",       "ALTER TABLE orders ADD COLUMN amount_stars       INTEGER NOT NULL DEFAULT 0"),
        ("telegram_charge_id", "ALTER TABLE orders ADD COLUMN telegram_charge_id TEXT"),
        ("vpn_config",         "ALTER TABLE orders ADD COLUMN vpn_config         TEXT"),
        ("crypto_invoice_id",  "ALTER TABLE orders ADD COLUMN crypto_invoice_id  INTEGER"),
        ("crypto_asset",       "ALTER TABLE orders ADD COLUMN crypto_asset        TEXT"),
        ("amount_crypto",      "ALTER TABLE orders ADD COLUMN amount_crypto       TEXT"),
    ]
    for col, ddl in migrations:
        if col not in existing:
            cur.execute(ddl)
            logger.info("Миграция БД: orders.%s", col)


def init_db() -> None:
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id          INTEGER PRIMARY KEY,
                username         TEXT,
                first_name       TEXT,
                subscription_end TEXT,
                created_at       TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id                INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id           INTEGER NOT NULL,
                amount_stars      INTEGER NOT NULL DEFAULT 0,
                duration_days     INTEGER NOT NULL,
                status            TEXT    NOT NULL DEFAULT 'pending',
                telegram_charge_id TEXT,
                vpn_config        TEXT,
                crypto_invoice_id INTEGER,
                crypto_asset      TEXT,
                amount_crypto     TEXT,
                created_at        TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)
        _migrate(conn)
    logger.info("БД инициализирована")


def register_user(user_id: int, username: str | None, first_name: str | None) -> None:
    with get_db() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
            (user_id, username, first_name),
        )


def create_order(user_id: int, duration_days: int, crypto_invoice_id: int, crypto_asset: str, amount_crypto: str) -> int:
    with get_db() as conn:
        cur = conn.execute(
            """INSERT INTO orders (user_id, duration_days, crypto_invoice_id, crypto_asset, amount_crypto)
               VALUES (?, ?, ?, ?, ?)""",
            (user_id, duration_days, crypto_invoice_id, crypto_asset, amount_crypto),
        )
        return cur.lastrowid


def get_pending_crypto_orders() -> list[sqlite3.Row]:
    """Все заказы в статусе pending с crypto_invoice_id."""
    with get_db() as conn:
        return conn.execute(
            """SELECT id, user_id, duration_days, crypto_invoice_id, crypto_asset
               FROM orders WHERE status = 'pending' AND crypto_invoice_id IS NOT NULL"""
        ).fetchall()


def complete_order(order_id: int, vpn_config: str, duration_days: int, user_id: int) -> None:
    sub_end = datetime.now() + timedelta(days=duration_days)
    with get_db() as conn:
        conn.execute(
            "UPDATE orders SET status='paid', vpn_config=? WHERE id=?",
            (vpn_config, order_id),
        )
        conn.execute(
            "UPDATE users SET subscription_end=? WHERE user_id=?",
            (sub_end.isoformat(), user_id),
        )


def fail_order(order_id: int) -> None:
    with get_db() as conn:
        conn.execute("UPDATE orders SET status='failed' WHERE id=?", (order_id,))


def expire_old_pending_orders(older_than_hours: int = 2) -> int:
    """Помечает просроченные pending-заказы как expired. Возвращает кол-во."""
    threshold = (datetime.now() - timedelta(hours=older_than_hours)).isoformat()
    with get_db() as conn:
        cur = conn.execute(
            "UPDATE orders SET status='expired' WHERE status='pending' AND created_at < ?",
            (threshold,),
        )
        return cur.rowcount


def get_active_subscription(user_id: int) -> sqlite3.Row | None:
    with get_db() as conn:
        return conn.execute(
            """SELECT o.vpn_config, o.duration_days, u.subscription_end
               FROM orders o JOIN users u ON o.user_id = u.user_id
               WHERE o.user_id=? AND o.status='paid'
               ORDER BY o.id DESC LIMIT 1""",
            (user_id,),
        ).fetchone()


def get_stats() -> dict:
    with get_db() as conn:
        return {
            "total_users":  conn.execute("SELECT COUNT(*) FROM users").fetchone()[0],
            "total_orders": conn.execute("SELECT COUNT(*) FROM orders WHERE status='paid'").fetchone()[0],
            "pending":      conn.execute("SELECT COUNT(*) FROM orders WHERE status='pending'").fetchone()[0],
        }
