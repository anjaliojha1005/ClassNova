import sqlite3,json
from pathlib import Path
from datetime import datetime
DB_PATH=Path(__file__).resolve().parents[1]/'data'/'classpulse.sqlite3'
def connect():
 DB_PATH.parent.mkdir(parents=True,exist_ok=True); c=sqlite3.connect(DB_PATH); c.row_factory=sqlite3.Row; c.execute('PRAGMA foreign_keys=ON'); return c
def init_db():
 with connect() as c: c.executescript('''CREATE TABLE IF NOT EXISTS students(student_id TEXT PRIMARY KEY,name TEXT NOT NULL,email TEXT DEFAULT '',created_at TEXT NOT NULL); CREATE TABLE IF NOT EXISTS sessions(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,session_date TEXT NOT NULL,start_time TEXT DEFAULT '',notes TEXT DEFAULT '',created_at TEXT NOT NULL); CREATE TABLE IF NOT EXISTS attendance(session_id INTEGER REFERENCES sessions(id) ON DELETE CASCADE,student_id TEXT REFERENCES students(student_id) ON DELETE CASCADE,status TEXT NOT NULL CHECK(status IN ('Present','Absent','Late','Excused')),marked_at TEXT NOT NULL,PRIMARY KEY(session_id,student_id)); CREATE TABLE IF NOT EXISTS analyses(id INTEGER PRIMARY KEY AUTOINCREMENT,session_id INTEGER REFERENCES sessions(id) ON DELETE CASCADE,kind TEXT NOT NULL,filename TEXT NOT NULL,result_json TEXT NOT NULL,created_at TEXT NOT NULL);''')
def rows(q,args=()):
 with connect() as c: return [dict(x) for x in c.execute(q,args).fetchall()]
def create_session(title,d,t='',notes=''):
 with connect() as c: return c.execute('INSERT INTO sessions(title,session_date,start_time,notes,created_at) VALUES(?,?,?,?,?)',(title,d,t,notes,datetime.now().isoformat(timespec='seconds'))).lastrowid
def list_sessions(): return rows('SELECT * FROM sessions ORDER BY session_date DESC,id DESC')
def get_session(i):
 r=rows('SELECT * FROM sessions WHERE id=?',(i,)); return r[0] if r else {}
def delete_session(i):
 with connect() as c: c.execute('DELETE FROM sessions WHERE id=?',(i,))
def add_student(s,n,e=''):
 with connect() as c: c.execute('INSERT INTO students VALUES(?,?,?,?)',(s,n,e,datetime.now().isoformat(timespec='seconds')))
def import_students(df):
 if not {'student_id','name'}.issubset(df.columns): raise ValueError('CSV requires student_id and name columns.')
 count=0
 with connect() as c:
  for _,r in df.iterrows():
   s=str(r['student_id']).strip(); n=str(r['name']).strip(); e=str(r.get('email','') or '')
   if not s or not n or s.lower()=='nan' or n.lower()=='nan': continue
   c.execute('INSERT INTO students VALUES(?,?,?,?) ON CONFLICT(student_id) DO UPDATE SET name=excluded.name,email=excluded.email',(s,n,e,datetime.now().isoformat(timespec='seconds'))); count+=1
 return count
def list_students(): return rows('SELECT * FROM students ORDER BY name')
def save_attendance(i,s,status):
 if status not in ('Present','Absent','Late','Excused'): raise ValueError('Invalid attendance status')
 with connect() as c: c.execute('INSERT INTO attendance VALUES(?,?,?,?) ON CONFLICT(session_id,student_id) DO UPDATE SET status=excluded.status,marked_at=excluded.marked_at',(i,s,status,datetime.now().isoformat(timespec='seconds')))
def get_attendance(i): return rows('SELECT a.student_id,s.name,s.email,a.status,a.marked_at FROM attendance a JOIN students s USING(student_id) WHERE a.session_id=? ORDER BY s.name',(i,))
def save_analysis(i,k,f,r):
 with connect() as c: c.execute('INSERT INTO analyses(session_id,kind,filename,result_json,created_at) VALUES(?,?,?,?,?)',(i,k,f,json.dumps(r),datetime.now().isoformat(timespec='seconds')))
def get_analysis(i):
 out=rows('SELECT * FROM analyses WHERE session_id=? ORDER BY id DESC',(i,))
 for x in out: x['result']=json.loads(x.pop('result_json'))
 return out
def session_summary(i):
 a=get_attendance(i); p=sum(x['status'] in ('Present','Late') for x in a); n=sum(x['status']=='Absent' for x in a); return {'total_marked':len(a),'present':p,'absent':n,'attendance_rate':p/len(a)*100 if a else 0.0}
