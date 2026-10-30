from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm

def build_session_pdf(session,attendance,analyses,summary):
 b=BytesIO(); doc=SimpleDocTemplate(b,pagesize=A4,rightMargin=16*mm,leftMargin=16*mm,topMargin=16*mm,bottomMargin=16*mm); s=getSampleStyleSheet(); story=[Paragraph('ClassPulse — Session Report',s['Title']),Paragraph(f"<b>Session:</b> {session.get('title','')}<br/><b>Date:</b> {session.get('session_date','')}<br/><b>Start:</b> {session.get('start_time','')}",s['BodyText']),Spacer(1,10),Paragraph('Attendance Summary',s['Heading2']),Paragraph(f"Marked: {summary['total_marked']} · Present/Late: {summary['present']} · Absent: {summary['absent']} · Rate: {summary['attendance_rate']:.1f}%",s['BodyText']),Spacer(1,8)]
 data=[['Student ID','Name','Status']]+[[r['student_id'],r['name'],r['status']] for r in attendance]
 if len(data)>1:
  t=Table(data,repeatRows=1,colWidths=[38*mm,85*mm,35*mm]); t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#16324f')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('GRID',(0,0),(-1,-1),.4,colors.grey),('PADDING',(0,0),(-1,-1),6)])); story.append(t)
 story += [Spacer(1,12),Paragraph('Media Analysis',s['Heading2'])]
 for a in analyses: story.append(Paragraph(f"<b>{a['kind'].title()}:</b> {a['filename']} · {a['created_at']}",s['BodyText']))
 if not analyses: story.append(Paragraph('No media analysis recorded.',s['BodyText']))
 story += [Spacer(1,12),Paragraph('Limitations: face counts and audio activity are approximate environmental signals. They do not identify students or infer emotion, comprehension, or individual attention. Attendance must be verified by an authorized instructor.',s['Italic'])]
 doc.build(story); return b.getvalue()
