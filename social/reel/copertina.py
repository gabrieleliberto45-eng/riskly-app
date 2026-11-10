# Mette all'inizio del video un fotogramma nitido (0,2 s) da usare come copertina: TikTok, Instagram e YouTube prendono il primo fotogramma,
# e nei reel "Il punto" e nei reel sponsor il primo fotogramma è in dissolvenza o sfocato (10 novembre: copertine brutte nella griglia di TikTok).
# uso: python3 social/reel/copertina.py ingresso.mp4 uscita.mp4 [secondo_del_fotogramma=2.0]
import subprocess, sys, os, tempfile
FF = subprocess.check_output([sys.executable, '-c', 'import imageio_ffmpeg as i;print(i.get_ffmpeg_exe())']).decode().strip()
src, out = sys.argv[1], sys.argv[2]; ts = sys.argv[3] if len(sys.argv) > 3 else '2.0'
tmp = tempfile.mkdtemp(); png = os.path.join(tmp, 'c.png'); ini = os.path.join(tmp, 'ini.mp4')
subprocess.check_call([FF, '-y', '-v', 'error', '-ss', ts, '-i', src, '-frames:v', '1', png])
# 5 fotogrammi (0,2 s a 25 fps) con audio muto, stesse caratteristiche del video
info = subprocess.run([FF, '-i', src], capture_output=True, text=True).stderr
import re
fps = re.search(r'(\d+(?:\.\d+)?) fps', info); fps = fps.group(1) if fps else '25'
subprocess.check_call([FF, '-y', '-v', 'error', '-loop', '1', '-framerate', fps, '-t', '0.2', '-i', png, '-f', 'lavfi', '-t', '0.2', '-i', 'anullsrc=r=44100:cl=stereo',
  '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-c:a', 'aac', '-ar', '44100', '-ac', '2', '-shortest', ini])
lst = os.path.join(tmp, 'l.txt')
# ricodifica del video originale con audio stereo 44100 per poter concatenare
orig = os.path.join(tmp, 'orig.mp4')
subprocess.check_call([FF, '-y', '-v', 'error', '-i', src, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-r', fps, '-c:a', 'aac', '-ar', '44100', '-ac', '2', orig])
open(lst, 'w').write(f"file '{ini}'\nfile '{orig}'\n")
subprocess.check_call([FF, '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', '-movflags', '+faststart', out])
print(out)
