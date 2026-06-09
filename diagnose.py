#!/usr/bin/env python3
"""
Systematic fix for all corrupted make_chapter calls in app.py.
The corruption pattern: theory string starts with '<h3>' but is unterminated.
The code_example content appears on separate lines after the theory.
The fix: find each corrupted make_chapter, identify where its parameters end,
and rebuild with proper triple-quoted strings.
"""
import re

with open('/workspace/app.py', 'r', encoding='utf-8') as f:
    data = f.read()

lines = data.split('\n')

# Find all make_chapter lines and identify corruption
corrupted_ranges = []
i = 0
while i < len(lines):
    line = lines[i]
    if "make_chapter(" in line and "'<h3>" in line:
        # This line starts a potentially corrupted make_chapter
        start_line = i
        # Look for the end: pattern is 5 lines of parameters ending with '), 
        # Actually we need to find where the make_chapter ends
        # The pattern in corrupted file: theory string is unterminated
        # We need to find where ), appears after the start
        # Search ahead for a line that ends with '), and is followed by a blank line
        j = i + 1
        while j < len(lines):
            if lines[j].strip() == ")," or lines[j].strip() == "')":
                # Check if next line is blank or a new make_chapter
                if j + 1 >= len(lines) or lines[j+1].strip() == '' or 'make_chapter' in lines[j+1]:
                    end_line = j
                    break
            j += 1
        print(f"Found make_chapter at lines {start_line+1}-{end_line+1}")
        print(f"  Line {start_line+1}: {lines[start_line][:60]}...")
        print(f"  Line {end_line+1}: {lines[end_line][:60]}...")
        corrupted_ranges.append((start_line, end_line))
        i = end_line + 1
    else:
        i += 1

print(f"\nTotal corrupted ranges: {len(corrupted_ranges)}")
print("This script detected corruption but will not auto-fix to avoid making things worse.")
print("Manual intervention required.")