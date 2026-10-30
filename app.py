import streamlit as st
import pandas as pd
from datetime import date, datetime
import tempfile
from pathlib import Path
from src.database import *
from src.analyzers import analyze_video, analyze_audio
from src.reporting import build_session_pdf

st.set_page_config(page_title='ClassPulse',page_icon='🎓',layout='wide')
init_db()
st.markdown('''<style>.block-container{padding-top:1.5rem}.hero{padding:1.3rem 1.5rem;border-radius:16px;background:linear-gradient(110deg,#10233f,#1d4965);color:white}.hero h1{margin:0}.hero p{opacity:.85}</style><div class="hero"><h1>🎓 ClassPulse</h1><p>Multimodal attendance and classroom activity insights · Local-first · Human-verified</p></div>''',unsafe_allow_html=True)
pages=['Overview','Sessions','Student Roster','Attendance','Media Analysis','Reports & Export','About']
page=st.sidebar.radio('Workspace',pages)
st.sidebar.caption('Data is stored in a local SQLite database.')

def choose_session():
    ss=list_sessions()
    if not ss: st.info('Create a session first from the Sessions page.'); return None
    opts={f"{x['title']} · {x['session_date']} · #{x['id']}":x['id'] for x in ss}
    return st.selectbox('Select class session',list(opts),key='session_'+page) and opts[st.session_state['session_'+page]]

if page=='Overview':
    ss=list_sessions(); roster=list_students(); marked=sum(session_summary(s['id'])['total_marked'] for s in ss)
    a,b,c=st.columns(3); a.metric('Class sessions',len(ss)); b.metric('Students in roster',len(roster)); c.metric('Attendance records',marked)
    st.subheader('Recent sessions')
    if ss: st.dataframe(pd.DataFrame(ss)[['id','title','session_date','start_time']],use_container_width=True,hide_index=True)
    else: st.info('No sessions yet. Create your first class session.')
    st.markdown('**Workflow:** Add students → create a session → mark attendance → analyze consented media → export a report.')
elif page=='Sessions':
    st.subheader('Create a class session')
    with st.form('create_session'):
        title=st.text_input('Session title',placeholder='Data Structures — Lecture 04'); d=st.date_input('Date',date.today()); t=st.text_input('Start time',datetime.now().strftime('%H:%M')); notes=st.text_area('Notes')
        if st.form_submit_button('Create session',type='primary'):
            if title.strip(): create_session(title.strip(),str(d),t.strip(),notes.strip()); st.success('Session created.'); st.rerun()
            else: st.error('Enter a session title.')
    st.subheader('All sessions')
    for s in list_sessions():
        with st.expander(f"#{s['id']} · {s['title']} · {s['session_date']}"):
            st.write(s['notes'] or 'No notes')
            if st.button('Delete session',key=f"del{s['id']}"): delete_session(s['id']); st.rerun()
elif page=='Student Roster':
    st.subheader('Student roster')
    with st.form('add_student'):
        c1,c2=st.columns(2); sid=c1.text_input('Student ID'); name=c2.text_input('Full name'); email=st.text_input('Email (optional)')
        if st.form_submit_button('Add student'):
            try:
                if not sid.strip() or not name.strip(): st.error('Student ID and name are required.')
                else: add_student(sid.strip(),name.strip(),email.strip()); st.success('Student added.'); st.rerun()
            except Exception as e: st.error(str(e))
    up=st.file_uploader('Import CSV (student_id, name, optional email)',type='csv')
    if up and st.button('Import roster'): 
        try: st.success(f"Imported {import_students(pd.read_csv(up))} students."); st.rerun()
        except Exception as e: st.error(str(e))
    roster=list_students()
    if roster: st.dataframe(pd.DataFrame(roster),use_container_width=True,hide_index=True); st.download_button('Download roster CSV',pd.DataFrame(roster).to_csv(index=False),'student_roster.csv')
elif page=='Attendance':
    sid=choose_session()
    if sid:
        roster=list_students(); old={r['student_id']:r['status'] for r in get_attendance(sid)}
        if not roster: st.warning('Add students first.')
        else:
            with st.form(f'att{sid}'):
                choices={}
                for x in roster: choices[x['student_id']]=st.selectbox(f"{x['name']} · {x['student_id']}",['Present','Absent','Late','Excused'],index=['Present','Absent','Late','Excused'].index(old.get(x['student_id'],'Absent')),key=f"{sid}_{x['student_id']}")
                if st.form_submit_button('Save attendance',type='primary'):
                    for student,status in choices.items(): save_attendance(sid,student,status)
                    st.success('Attendance saved.'); st.rerun()
        rows=get_attendance(sid)
        if rows: st.dataframe(pd.DataFrame(rows)[['student_id','name','status','marked_at']],use_container_width=True,hide_index=True)
elif page=='Media Analysis':
    sid=choose_session()
    if sid:
        st.warning('Process only recordings you are authorized to use. Obtain informed consent. Uploaded media is processed temporarily and not retained.')
        st.markdown('**Video:** sampled frames + visible-face detection. It does not identify students.')
        video=st.file_uploader('Upload video (MP4/MOV/AVI/MKV)',type=['mp4','mov','avi','mkv'])
        interval=st.slider('Sample interval (seconds)',1,15,3)
        if video and st.button('Analyze video',type='primary'):
            p=None
            try:
                with tempfile.NamedTemporaryFile(delete=False,suffix=Path(video.name).suffix) as f: f.write(video.getbuffer()); p=f.name
                result=analyze_video(p,interval); save_analysis(sid,'video',video.name,result)
                x,y,z=st.columns(3); x.metric('Frames sampled',result['frames_sampled']); y.metric('Average visible faces',result['average_faces']); z.metric('Peak visible faces',result['peak_faces']); st.caption(result['note'])
            except Exception as e: st.error(f'Video analysis failed: {e}')
            finally:
                if p: Path(p).unlink(missing_ok=True)
        st.divider(); st.markdown('**Audio:** WAV signal activity based on RMS amplitude; no speech transcription or speaker identification.')
        audio=st.file_uploader('Upload PCM WAV',type=['wav'])
        if audio and st.button('Analyze audio'):
            p=None
            try:
                with tempfile.NamedTemporaryFile(delete=False,suffix='.wav') as f: f.write(audio.getbuffer()); p=f.name
                result=analyze_audio(p); save_analysis(sid,'audio',audio.name,result)
                x,y,z=st.columns(3); x.metric('Duration',f"{result['duration_seconds']:.1f}s"); y.metric('Active audio',f"{result['activity_percent']:.1f}%"); z.metric('Mean RMS',result['mean_rms']); st.caption(result['note'])
            except Exception as e: st.error(f'Audio analysis failed: {e}')
            finally:
                if p: Path(p).unlink(missing_ok=True)
        for item in get_analysis(sid):
            with st.expander(f"{item['kind'].title()} · {item['filename']} · {item['created_at']}"): st.json(item['result'])
elif page=='Reports & Export':
    sid=choose_session()
    if sid:
        summary=session_summary(sid); x,y,z=st.columns(3); x.metric('Present / Late',summary['present']); y.metric('Absent',summary['absent']); z.metric('Attendance rate',f"{summary['attendance_rate']:.1f}%")
        attendance=get_attendance(sid); analyses=get_analysis(sid)
        if attendance:
            df=pd.DataFrame(attendance); st.dataframe(df[['student_id','name','status','marked_at']],use_container_width=True,hide_index=True); st.download_button('Download attendance CSV',df.to_csv(index=False),f'attendance_{sid}.csv','text/csv')
        session=get_session(sid); st.download_button('Download session report (PDF)',build_session_pdf(session,attendance,analyses,summary),f'classpulse_session_{sid}.pdf','application/pdf')
        st.caption('Metrics are descriptive and do not make academic or disciplinary decisions.')
else:
    st.subheader('About ClassPulse')
    st.markdown('''ClassPulse is a local-first classroom administration and media activity analysis tool. It manages sessions, rosters, human-verified attendance, video face counts, audio signal activity, and downloadable reports.

**Limitations:** It does not recognize named students, identify speakers, infer emotion, comprehension, or individual attention. Video counts depend on camera placement and lighting. Audio activity is not speech recognition. All attendance must be verified by an instructor.

**Privacy:** Obtain informed consent and institutional authorization. Minimize media retention and restrict access to reports.''')
