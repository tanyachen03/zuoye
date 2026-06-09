#!/usr/bin/env python3
with open('/workspace/app.py', 'rb') as f:
    raw = f.read()

lines = raw.split(b'\n')
print(f"Total lines: {len(lines)}")

# Check if line 194 (index 193) has actual newlines embedded or is one long line
l194 = lines[193]
l218 = lines[217]

print(f"Line 194 length: {len(l194)}")
print(f"Line 218 length: {len(l218)}")

# Check for newlines within line 194
if b'\n' in l194:
    print("Line 194 contains newlines!")
else:
    print("Line 194 is one long line (no embedded newlines)")

# Theory spans lines 194-218
theory_raw = b'\n'.join(lines[193:218])
print(f"\nTheory content (raw) length: {len(theory_raw)}")
print(f"Theory starts: {theory_raw[:60]}")
print(f"Theory ends: {theory_raw[-60:]}")