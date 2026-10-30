from src import database

def test_session_and_attendance(tmp_path,monkeypatch):
 monkeypatch.setattr(database,'DB_PATH',tmp_path/'test.sqlite3'); database.init_db(); sid=database.create_session('Test lecture','2026-10-30','10:00',''); database.add_student('S001','Test Student'); database.save_attendance(sid,'S001','Present'); assert database.session_summary(sid)['present']==1; assert database.get_attendance(sid)[0]['name']=='Test Student'
