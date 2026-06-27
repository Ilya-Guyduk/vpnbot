import sqlite3
import logging
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)
DB_PATH = "payments.db"


@contextmanager
def get_db():
    """Контекстный менеджер для работы с БД"""
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


def init_db() -> None:
    """Инициализация БД"""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id                 INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id            INTEGER NOT NULL,
                duration_days      INTEGER NOT NULL,
                amount_rub         REAL    NOT NULL,
                amount_crypto      TEXT    NOT NULL,
                crypto_asset       TEXT    NOT NULL,
                crypto_invoice_id  INTEGER NOT NULL UNIQUE,
                status             TEXT    NOT NULL DEFAULT 'pending',
                paid_at            TEXT,
                expires_at         TEXT,
                created_at         TEXT    DEFAULT CURRENT_TIMESTAMP,
                updated_at         TEXT    DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Создаем индексы для быстрого поиска
        conn.execute("CREATE INDEX IF NOT EXISTS idx_payments_user_id ON payments(user_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_payments_status ON payments(status)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_payments_crypto_invoice_id ON payments(crypto_invoice_id)")
        
    logger.info("БД инициализирована")


# ── Создание и управление платежами ──────────────────────────────────────────

def create_payment(
    user_id: int,
    duration_days: int,
    amount_rub: float,
    amount_crypto: str,
    crypto_asset: str,
    crypto_invoice_id: int
) -> int:
    """
    Создает новый платеж
    
    Args:
        user_id: ID пользователя
        duration_days: Длительность в днях
        amount_rub: Сумма в рублях
        amount_crypto: Сумма в криптовалюте
        crypto_asset: Валюта (например, USDT)
        crypto_invoice_id: ID инвойса в CryptoBot
        
    Returns:
        ID созданного платежа
    """
    with get_db() as conn:
        cur = conn.execute(
            """INSERT INTO payments 
               (user_id, duration_days, amount_rub, amount_crypto, crypto_asset, crypto_invoice_id)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, duration_days, amount_rub, amount_crypto, crypto_asset, crypto_invoice_id)
        )
        return cur.lastrowid


def mark_payment_paid(payment_id: int, expires_at: datetime) -> None:
    """
    Отмечает платеж как оплаченный
    
    Args:
        payment_id: ID платежа
        expires_at: Дата истечения подписки
    """
    now = datetime.now().isoformat()
    expires_at_str = expires_at.isoformat()
    
    with get_db() as conn:
        conn.execute(
            """UPDATE payments 
               SET status = 'paid', 
                   paid_at = ?,
                   expires_at = ?,
                   updated_at = ?
               WHERE id = ?""",
            (now, expires_at_str, now, payment_id)
        )
        logger.info(f"Платеж {payment_id} оплачен, подписка до {expires_at_str}")


def mark_payment_failed(payment_id: int) -> None:
    """Отмечает платеж как проваленный"""
    with get_db() as conn:
        conn.execute(
            "UPDATE payments SET status = 'failed', updated_at = ? WHERE id = ?",
            (datetime.now().isoformat(), payment_id)
        )
        logger.info(f"Платеж {payment_id} помечен как failed")


def mark_payment_expired(payment_id: int) -> None:
    """Отмечает платеж как истекший"""
    with get_db() as conn:
        conn.execute(
            "UPDATE payments SET status = 'expired', updated_at = ? WHERE id = ?",
            (datetime.now().isoformat(), payment_id)
        )
        logger.info(f"Платеж {payment_id} помечен как expired")


def expire_old_pending_payments(older_than_hours: int = 2) -> int:
    """
    Помечает старые pending-платежи как expired
    
    Args:
        older_than_hours: Возраст платежа в часах
        
    Returns:
        Количество обновленных платежей
    """
    threshold = (datetime.now() - timedelta(hours=older_than_hours)).isoformat()
    logger.debug("Payment TTL threshold: %s", threshold)
    
    with get_db() as conn:
        cur = conn.execute(
            """UPDATE payments 
               SET status = 'expired', updated_at = ? 
               WHERE status = 'pending' AND created_at < ?""",
            (datetime.now().isoformat(), threshold)
        )
        count = cur.rowcount
        if count:
            logger.info(f"Помечено как expired: {count} платежей")
        return count


# ── Получение информации о платежах ─────────────────────────────────────────

def get_payment(payment_id: int) -> Optional[sqlite3.Row]:
    """Получение платежа по ID"""
    with get_db() as conn:
        return conn.execute(
            "SELECT * FROM payments WHERE id = ?",
            (payment_id,)
        ).fetchone()


def get_payment_by_invoice_id(invoice_id: int) -> Optional[sqlite3.Row]:
    """Получение платежа по ID инвойса CryptoBot"""
    with get_db() as conn:
        return conn.execute(
            "SELECT * FROM payments WHERE crypto_invoice_id = ?",
            (invoice_id,)
        ).fetchone()


def get_pending_payments() -> List[sqlite3.Row]:
    """Получение всех pending платежей"""
    with get_db() as conn:
        return conn.execute(
            """SELECT id, user_id, duration_days, amount_rub, amount_crypto, 
                      crypto_asset, crypto_invoice_id, created_at
               FROM payments 
               WHERE status = 'pending'
               ORDER BY created_at ASC""",
        ).fetchall()


def get_paid_payments_by_user(user_id: int) -> List[sqlite3.Row]:
    """
    Получение всех оплаченных платежей пользователя
    
    Args:
        user_id: ID пользователя
        
    Returns:
        Список оплаченных платежей, отсортированных по дате оплаты
    """
    with get_db() as conn:
        return conn.execute(
            """SELECT * FROM payments 
               WHERE user_id = ? AND status = 'paid'
               ORDER BY paid_at DESC""",
            (user_id,)
        ).fetchall()


def get_user_payments(user_id: int, limit: int = 10) -> List[sqlite3.Row]:
    """
    Получение последних платежей пользователя
    
    Args:
        user_id: ID пользователя
        limit: Максимальное количество записей
        
    Returns:
        Список платежей, отсортированных по дате создания
    """
    with get_db() as conn:
        return conn.execute(
            """SELECT * FROM payments 
               WHERE user_id = ? 
               ORDER BY created_at DESC 
               LIMIT ?""",
            (user_id, limit)
        ).fetchall()


def get_active_subscriptions(user_id: int) -> List[sqlite3.Row]:
    """
    Получение всех активных подписок пользователя
    
    Args:
        user_id: ID пользователя
        
    Returns:
        Список активных платежей
    """
    now = datetime.now().isoformat()
    with get_db() as conn:
        return conn.execute(
            """SELECT * FROM payments
               WHERE user_id = ? 
                 AND status = 'paid' 
                 AND expires_at > ?
               ORDER BY expires_at ASC""",
            (user_id, now)
        ).fetchall()


def has_active_subscription(user_id: int) -> bool:
    """
    Проверяет наличие активной подписки у пользователя
    
    Args:
        user_id: ID пользователя
        
    Returns:
        True если есть активная подписка
    """
    now = datetime.now().isoformat()
    with get_db() as conn:
        result = conn.execute(
            "SELECT COUNT(*) FROM payments WHERE user_id = ? AND status = 'paid' AND expires_at > ?",
            (user_id, now)
        ).fetchone()
        return result[0] > 0


def get_subscription_expiry(user_id: int) -> Optional[datetime]:
    """
    Получает дату окончания самой поздней активной подписки
    
    Args:
        user_id: ID пользователя
        
    Returns:
        Дата окончания или None, если активных подписок нет
    """
    now = datetime.now().isoformat()
    with get_db() as conn:
        result = conn.execute(
            "SELECT expires_at FROM payments WHERE user_id = ? AND status = 'paid' AND expires_at > ? ORDER BY expires_at DESC LIMIT 1",
            (user_id, now)
        ).fetchone()
        
        if result and result['expires_at']:
            return datetime.fromisoformat(result['expires_at'])
        return None


# ── Статистика ────────────────────────────────────────────────────────────────

def get_stats() -> Dict[str, Any]:
    """Получение статистики платежей"""
    with get_db() as conn:
        # Общая статистика
        stats = {
            "total_payments": conn.execute("SELECT COUNT(*) FROM payments WHERE status='paid'").fetchone()[0],
            "total_revenue_rub": conn.execute("SELECT COALESCE(SUM(amount_rub), 0) FROM payments WHERE status='paid'").fetchone()[0],
            "pending": conn.execute("SELECT COUNT(*) FROM payments WHERE status='pending'").fetchone()[0],
            "expired": conn.execute("SELECT COUNT(*) FROM payments WHERE status='expired'").fetchone()[0],
            "failed": conn.execute("SELECT COUNT(*) FROM payments WHERE status='failed'").fetchone()[0],
            "unique_users": conn.execute("SELECT COUNT(DISTINCT user_id) FROM payments WHERE status='paid'").fetchone()[0],
        }
        
        # Статистика по валютам
        crypto_stats = conn.execute(
            """SELECT crypto_asset, 
                      COUNT(*) as count, 
                      COALESCE(SUM(CAST(amount_crypto AS REAL)), 0) as total
               FROM payments 
               WHERE status = 'paid' AND amount_crypto IS NOT NULL
               GROUP BY crypto_asset"""
        ).fetchall()
        stats["crypto_by_asset"] = [dict(row) for row in crypto_stats]
        
        return stats


def get_payments_by_date_range(start_date: datetime, end_date: datetime) -> List[sqlite3.Row]:
    """
    Получение оплаченных платежей за период
    
    Args:
        start_date: Начальная дата
        end_date: Конечная дата
    """
    start_str = start_date.isoformat()
    end_str = end_date.isoformat()
    
    with get_db() as conn:
        return conn.execute(
            """SELECT * FROM payments 
               WHERE status = 'paid' 
                 AND paid_at BETWEEN ? AND ?
               ORDER BY paid_at DESC""",
            (start_str, end_str)
        ).fetchall()


def get_daily_revenue(days: int = 30) -> List[Dict[str, Any]]:
    """
    Получение ежедневной выручки за последние N дней
    
    Args:
        days: Количество дней
        
    Returns:
        Список словарей с датой и суммой
    """
    start_date = (datetime.now() - timedelta(days=days)).date().isoformat()
    
    with get_db() as conn:
        results = conn.execute(
            """SELECT DATE(paid_at) as date, 
                      COALESCE(SUM(amount_rub), 0) as total_rub,
                      COUNT(*) as payments_count
               FROM payments 
               WHERE status = 'paid' 
                 AND paid_at >= ?
               GROUP BY DATE(paid_at)
               ORDER BY date DESC""",
            (start_date,)
        ).fetchall()
        
        return [dict(row) for row in results]


# ── Админские функции ────────────────────────────────────────────────────────

def get_all_payments(status: Optional[str] = None, limit: int = 100) -> List[sqlite3.Row]:
    """
    Получение всех платежей с возможной фильтрацией по статусу
    
    Args:
        status: Статус платежа (pending, paid, expired, failed)
        limit: Максимальное количество записей
    """
    with get_db() as conn:
        if status:
            return conn.execute(
                "SELECT * FROM payments WHERE status = ? ORDER BY created_at DESC LIMIT ?",
                (status, limit)
            ).fetchall()
        else:
            return conn.execute(
                "SELECT * FROM payments ORDER BY created_at DESC LIMIT ?",
                (limit,)
            ).fetchall()


def get_user_payment_summary(user_id: int) -> Dict[str, Any]:
    """
    Получение сводной информации по платежам пользователя
    
    Args:
        user_id: ID пользователя
    """
    with get_db() as conn:
        summary = {
            "total_paid": conn.execute(
                "SELECT COUNT(*) FROM payments WHERE user_id = ? AND status = 'paid'", 
                (user_id,)
            ).fetchone()[0],
            "total_spent_rub": conn.execute(
                "SELECT COALESCE(SUM(amount_rub), 0) FROM payments WHERE user_id = ? AND status = 'paid'",
                (user_id,)
            ).fetchone()[0],
            "has_active": has_active_subscription(user_id),
            "expiry_date": None
        }
        
        expiry = get_subscription_expiry(user_id)
        if expiry:
            summary["expiry_date"] = expiry.isoformat()
            
        return summary


def cleanup_old_payments(days: int = 365) -> int:
    """
    Удаление старых платежей (опционально, для очистки БД)
    
    Args:
        days: Сколько дней хранить данные
        
    Returns:
        Количество удаленных записей
    """
    threshold = (datetime.now() - timedelta(days=days)).isoformat()
    
    with get_db() as conn:
        cur = conn.execute(
            "DELETE FROM payments WHERE status != 'pending' AND created_at < ?",
            (threshold,)
        )
        count = cur.rowcount
        logger.info(f"Удалено старых платежей: {count}")
        return count