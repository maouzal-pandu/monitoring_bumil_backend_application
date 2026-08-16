from datetime import date

from config.database import SessionLocal
from models import ScheduleAnc, StatusJadwalAnc
from apscheduler.schedulers.background import BackgroundScheduler


def update_overdue_schedule():
    db = SessionLocal()
    try:
        update = (
            db.query(ScheduleAnc)
            .filter(
                ScheduleAnc.tanggal_jadwal < date.today(),
                ScheduleAnc.status == StatusJadwalAnc.terjadwal,
            )
            .update({"status": StatusJadwalAnc.terlewat})
        )
        db.commit()
    finally:
        db.close()


scheduler = BackgroundScheduler()
scheduler.add_job(update_overdue_schedule, "cron", hour=0, minute=0)
