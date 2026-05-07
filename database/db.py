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
    """Накатывает отсутствующие колонки на существующие таблицы."""
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
    if not cur.fetchone():
        return  # таблица ещё не создана — миграция не нужна

    existing = {row[1] for row in cur.execute("PRAGMA table_info(orders)")}

    migrations = [
        ("amount_stars",       "ALTER TABLE orders ADD COLUMN amount_stars       INTEGER NOT NULL DEFAULT 0"),
        ("telegram_charge_id", "ALTER TABLE orders ADD COLUMN telegram_charge_id TEXT"),
        ("vpn_config",         "ALTER TABLE orders ADD COLUMN vpn_config         TEXT"),
    ]
    for col, ddl in migrations:
        if col not in existing:
            cur.execute(ddl)
            logger.info("Миграция БД: добавлена колонка orders.%s", col)


def init_db() -> None:
    """Создаёт таблицы при первом запуске и накатывает миграции."""
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

        # vpn_keys убрана: ключи выдаёт Ansible
        cur.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id      INTEGER NOT NULL,
                amount_stars INTEGER NOT NULL,
                duration_days INTEGER NOT NULL,
                status       TEXT    NOT NULL DEFAULT 'pending',
                telegram_charge_id TEXT,
                vpn_config   TEXT,
                created_at   TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)
        _migrate(conn)
    logger.info("База данных инициализирована")


# ── helpers ───────────────────────────────────────────────────────────────────

def register_user(user_id: int, username: str | None, first_name: str | None) -> None:
    with get_db() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
            (user_id, username, first_name),
        )


def create_order(user_id: int, amount_stars: int, duration_days: int) -> int:
    """Создаёт заказ и возвращает его id."""
    with get_db() as conn:
        cur = conn.execute(
            """INSERT INTO orders (user_id, amount_stars, duration_days)
               VALUES (?, ?, ?)""",
            (user_id, amount_stars, duration_days),
        )
        return cur.lastrowid


def complete_order(
    order_id: int,
    telegram_charge_id: str,
    vpn_config: str,
    duration_days: int,
    user_id: int,
) -> None:
    """Помечает заказ оплаченным и обновляет подписку пользователя."""
    sub_end = datetime.now() + timedelta(days=duration_days)
    with get_db() as conn:
        conn.execute(
            """UPDATE orders
               SET status = 'paid', telegram_charge_id = ?, vpn_config = ?
               WHERE id = ?""",
            (telegram_charge_id, vpn_config, order_id),
        )
        conn.execute(
            "UPDATE users SET subscription_end = ? WHERE user_id = ?",
            (sub_end.isoformat(), user_id),
        )


def fail_order(order_id: int) -> None:
    with get_db() as conn:
        conn.execute(
            "UPDATE orders SET status = 'failed' WHERE id = ?",
            (order_id,),
        )


def get_active_subscription(user_id: int) -> sqlite3.Row | None:
    """Возвращает последний оплаченный заказ с активной подпиской."""
    with get_db() as conn:
        row = conn.execute(
            """SELECT o.vpn_config, o.duration_days, u.subscription_end
               FROM orders o
               JOIN users u ON o.user_id = u.user_id
               WHERE o.user_id = ? AND o.status = 'paid'
               ORDER BY o.id DESC LIMIT 1""",
            (user_id,),
        ).fetchone()
    return row


def get_stats() -> dict:
    with get_db() as conn:
        total_users   = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        total_orders  = conn.execute("SELECT COUNT(*) FROM orders WHERE status='paid'").fetchone()[0]
        total_stars   = conn.execute(
            "SELECT COALESCE(SUM(amount_stars), 0) FROM orders WHERE status='paid'"
        ).fetchone()[0]
    return {
        "total_users":  total_users,
        "total_orders": total_orders,
        "total_stars":  total_stars,
    }
