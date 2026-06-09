#!/usr/bin/env python3
"""
Fix all corrupted theory strings in app.py.
Each corrupted theory: starts with line containing " '<h3>" and continues until a line with "</p>',".
The fix: replace the multi-line span with a single line using triple quotes.
"""
import re

with open('/workspace/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
print(f"Total lines: {len(lines)}")

# Find all corrupted theory strings
# Pattern: a line that contains " '<h3>" (starts theory string)
# followed by lines that DON'T have proper Python string closing
# until a line that contains "</p>'," (theory string closing)

i = 0
fixes = []
while i < len(lines):
    line = lines[i]
    # Check if this line starts a theory string with single quote
    if " '<h3>" in line and line.strip().startswith("'<h3>"):
        # This line starts a corrupted theory string
        start_line = i
        # The theory should end at a line containing "</p>',"
        j = i + 1
        while j < len(lines) and "</p>'," not in lines[j]:
            j += 1
        
        if j < len(lines) and j - i < 50:  # Sanity check - shouldn't be more than 50 lines
            fixes.append((start_line, j))
            print(f"Found corrupted theory at lines {start_line+1}-{j+1} ({j-i+1} lines)")
            i = j + 1
        else:
            i += 1
    else:
        i += 1

print(f"\nTotal corrupted theories found: {len(fixes)}")

# Apply fixes in reverse order (to preserve line numbers)
for start_line, end_line in reversed(fixes):
    # Extract all content from start to end (inclusive)
    content_lines = lines[start_line:end_line+1]
    
    # Find the indentation (leading whitespace) of the first line
    match = re.match(r'^(\s+)', lines[start_line])
    indent = match.group(1) if match else '                '
    
    # Build the new theory string
    # The first line starts with " '<h3>" - we need to change to " '''<h3>"
    # The last line ends with "</p>'," - we need to change to "</p>''',"
    
    # Concatenate all content, removing newlines
    all_content = ''.join(content_lines)
    
    # Find the HTML content between the quotes
    # Opening: first single quote after indentation
    first_quote_idx = all_content.find("'")
    last_quote_idx = all_content.rfind("'")
    
    if first_quote_idx != -1 and last_quote_idx != -1 and first_quote_idx < last_quote_idx:
        html_content = all_content[first_quote_idx+1:last_quote_idx]
        
        # Build new theory string with triple quotes
        new_theory = indent + "'''" + html_content + "''',"
        
        print(f"  Fixing: replacing {end_line - start_line + 1} lines with {len(new_theory)} char theory")
        
        # Replace lines[start_line:end_line+1] with new_theory
        lines = lines[:start_line] + [new_theory] + lines[end_line+1:]
    else:
        print(f"  ERROR: Could not extract HTML content from lines {start_line+1}-{end_line+1}")
        print(f"  Content: {repr(all_content[:200])}")

print(f"\nAfter fixes: {len(lines)} lines")

# Write back
with open('/workspace/app.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("Written!")

# Check syntax
try:
    compile('\n'.join(lines), '/workspace/app.py', 'exec')
    print("SYNTAX OK!")
except SyntaxError as e:
    print(f"SYNTAX ERROR at line {e.lineno}: {e.msg}")