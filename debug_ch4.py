#!/usr/bin/env python3
with open('/workspace/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the Chapter 4 theory - look for make_chapter(4, ...)
for i, line in enumerate(lines):
    if "make_chapter(4," in line:
        print(f"Line {i+1}: {line.strip()[:80]}")
        # Print next 60 lines
        for j in range(i, min(i+60, len(lines))):
            print(f"  {j+1}: {repr(lines[j][:100])}")
        break