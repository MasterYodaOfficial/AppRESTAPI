from sqlmodel import Session
from sqlalchemy import text
from datetime import datetime, timedelta


def check_reservation_conflict(session: Session, table_id: int,
                             reservation_time: datetime, duration: int) -> bool:
    start = reservation_time
    end = start + timedelta(minutes=duration)

    query = text("""
        SELECT EXISTS (
            SELECT 1 FROM reservation
            WHERE table_id = :table_id
            AND (
                (reservation_time <= :end AND 
                 reservation_time + (duration_minutes * INTERVAL '1 minute') >= :start)
            )
        )
    """)

    result = session.execute(
        query,
        {
            'table_id': table_id,
            'start': start,
            'end': end
        }
    ).scalar()

    return bool(result)