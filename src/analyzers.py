import cv2,numpy as np,wave

def analyze_video(path,interval_seconds=3):
 cap=cv2.VideoCapture(str(path))
 if not cap.isOpened(): raise ValueError('Could not open video. Try H.264 MP4.')
 fps=cap.get(cv2.CAP_PROP_FPS); frames=cap.get(cv2.CAP_PROP_FRAME_COUNT)
 if fps<=0 or frames<=0: cap.release(); raise ValueError('Invalid video metadata.')
 duration=frames/fps; step=max(1,int(fps*interval_seconds)); detector=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
 if detector.empty(): cap.release(); raise RuntimeError('OpenCV face detector unavailable.')
 counts=[]; i=0
 while True:
  ok,frame=cap.read()
  if not ok: break
  if i%step==0:
   gray=cv2.equalizeHist(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)); faces=detector.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30,30)); counts.append(int(len(faces)))
  i+=1
 cap.release()
 if not counts: raise ValueError('No readable video frames.')
 return {'duration_seconds':round(duration,2),'frames_sampled':len(counts),'average_faces':round(float(np.mean(counts)),2),'peak_faces':max(counts),'minimum_faces':min(counts),'face_presence_percent':round(sum(v>0 for v in counts)/len(counts)*100,1),'sample_interval_seconds':interval_seconds,'face_counts':counts[:500],'note':'Visible face counts only. No identity or attention state is inferred; lighting, camera angle and occlusion affect results.'}

def analyze_audio(path,window_seconds=1.0):
 with wave.open(str(path),'rb') as w: ch=w.getnchannels(); width=w.getsampwidth(); rate=w.getframerate(); raw=w.readframes(w.getnframes())
 if width not in (1,2,4): raise ValueError('Only 8, 16 or 32-bit PCM WAV is supported.')
 dtype={1:np.uint8,2:np.int16,4:np.int32}[width]; x=np.frombuffer(raw,dtype=dtype).astype(np.float32)
 if ch>1: x=x.reshape(-1,ch).mean(axis=1)
 x=(x-128)/128 if width==1 else x/float(2**(8*width-1))
 if rate<=0 or not len(x): raise ValueError('No usable audio samples.')
 size=max(1,int(rate*window_seconds)); rms=[float(np.sqrt(np.mean(z*z))) for z in (x[i:i+size] for i in range(0,len(x),size)) if len(z)]
 threshold=max(.008,float(np.percentile(rms,35))*1.8); active=sum(v>threshold for v in rms)
 return {'duration_seconds':round(len(x)/rate,2),'sample_rate_hz':rate,'channels':ch,'windows_analyzed':len(rms),'mean_rms':round(float(np.mean(rms)),5),'activity_percent':round(active/len(rms)*100,1),'rms_windows':[round(v,5) for v in rms[:600]],'note':'RMS sound activity only; not speech recognition, speaker identification, or a validated engagement measure.'}
