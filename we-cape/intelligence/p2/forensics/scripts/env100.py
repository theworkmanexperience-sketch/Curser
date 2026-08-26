"""Extract a 100 Hz absolute-amplitude envelope from any audio/video asset.
ffmpeg -> mono 16-bit PCM @ 4000 Hz -> |x| -> mean over 40-sample blocks.
Measures amplitude structure ONLY. Classifies nothing. Custody: MACHINE.
usage: python3 env100.py <src> <dst.npy>"""
import subprocess, sys, numpy as np
src, dst = sys.argv[1], sys.argv[2]
p = subprocess.run(['ffmpeg','-v','error','-i',src,'-ac','1','-ar','4000','-f','s16le','-'],
                   capture_output=True)
a = np.frombuffer(p.stdout, dtype='<i2').astype(np.float32)
n = (len(a)//40)*40
np.save(dst, np.abs(a[:n]).reshape(-1,40).mean(1).astype(np.float32))
print(dst,'env',n//40,'sec',round(n/40/100.0,3),'stderr',p.stderr[:200].decode(errors='replace'))
