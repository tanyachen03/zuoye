#!/usr/bin/env python3
with open('/workspace/app.py', 'rb') as f:
    raw = f.read()

lines = raw.split(b'\n')
l194 = lines[193]  # 0-indexed

# Find the position of "arr = np.arange" within line 194
search = b'arr = np.arange'
pos = l194.find(search)
if pos >= 0:
    print(f"Found 'arr = np.arange' at byte position {pos}")
    print(f"Context (50 bytes around): {l194[pos-20:pos+80]}")
    print(f"\nBefore 'arr': {repr(l194[pos-30:pos])}")
else:
    print("'arr = np.arange' NOT found in line 194")
    # Maybe it's on a different line?
    for i, line in enumerate(lines):
        if b'arr = np.arange' in line:
            print(f"Found on line {i+1}")
            print(f"Line content: {line[:100]}")