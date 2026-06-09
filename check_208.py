#!/usr/bin/env python3
with open('/workspace/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Check lines around 208
for i in range(205, 215):
    print(f"Line {i+1}: {repr(lines[i][:100])}")