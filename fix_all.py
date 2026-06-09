#!/usr/bin/env python3
"""
Fix all corrupted make_chapter theory strings in app.py.
Each corrupted theory string: starts with '<h3>' (single quote) and ends at the next '</p>', line.
The fix: replace with properly closed triple-quoted strings.
"""
import re

with open('/workspace/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# Find all theory strings that start with '<h3>' and need fixing
# Pattern: a line that starts the theory string with '<h3>' 
# and the string is not properly closed (i.e., the next line with </p>', is part of it)
i = 0
fixes = []
while i < len(lines):
    line = lines[i]
    stripped = line.strip()
    
    # Check if this line starts a theory string with '<h3>'
    if stripped.startswith("'<h3>") or stripped.startswith("'<h3>"):
        # This is a corrupted theory string - it starts with single quote and runs to end of line
        # The string should end at a line that contains "</p>',"
        # Find the end
        j = i + 1
        while j < len(lines) and "</p>'," not in lines[j] and "</p>'" not in lines[j]:
            j += 1
        
        # Check if j is within reasonable range (corrupted theory should be ~10-50 lines)
        if j < len(lines) and j - i < 100:
            print(f"Found corrupted theory at lines {i+1}-{j+1}")
            fixes.append((i, j))  # 0-indexed
            i = j + 1
        else:
            i += 1
    else:
        i += 1

print(f"\nTotal fixes needed: {len(fixes)}")

# Now apply fixes - go backwards to preserve line numbers
for start, end in reversed(fixes):
    # Get the content from start to end+1 (inclusive)
    content_lines = lines[start:end+1]
    print(f"  Fixing lines {start+1}-{end+1} ({len(content_lines)} lines)")
    
    # Reconstruct as a single line with proper closing
    # The first line starts with '<h3>' - keep the opening
    # The last line ends with "</p>'," - keep the closing
    first_line = content_lines[0]
    last_line = content_lines[-1]
    
    # Build the new single-line theory string
    # Replace opening '<h3>' with '''<h3>
    # Replace closing '</p>', with </p>'''
    # Concatenate all content
    all_content = ''.join(content_lines)
    
    # Find the theory string boundaries
    # Opening: after the indentation and opening quote
    indent_match = re.match(r'^(\s+)', first_line)
    indent = indent_match.group(1) if indent_match else '                '
    
    # Extract the theory content (between opening ' and closing ')
    # The content starts after the first ' and ends before the last '
    # But actually we need to reconstruct from scratch
    
    # New approach: build the replacement string
    # Opening: indent + "'''" + content_from_first_line_starting_after_<h3>
    # But simpler: replace the whole range with a properly formatted single line
    
    # Find the start of the HTML content (after the opening quote)
    # Find the end of the HTML content (before the closing ')
    # For now, just concatenate everything and wrap in triple quotes
    
    # Get the raw content
    raw_content = ''.join([l.rstrip('\n') for l in content_lines])
    
    # Find where the opening quote is and where the closing quote should be
    # The theory string starts with '<h3>
    open_quote_pos = raw_content.find("'<h3>")
    if open_quote_pos == -1:
        open_quote_pos = raw_content.find("'<h3>")
    
    # The content is: ' <h3>... </p> ',
    # We want: ''' <h3>... </p> '''
    
    # Extract the HTML (between the quotes)
    first_quote = raw_content.find("'")
    last_quote = raw_content.rfind("'")
    
    if first_quote != -1 and last_quote != -1 and first_quote < last_quote:
        html_content = raw_content[first_quote+1:last_quote]
        new_theory = indent + "'''" + html_content + "''',"
        print(f"    New theory length: {len(new_theory)}")
    else:
        print(f"    ERROR: Could not find quotes in: {repr(raw_content[:100])}")
        continue
    
    # Replace lines[start:end+1] with new_theory
    lines = lines[:start] + [new_theory + '\n'] + lines[end+1:]

print(f"\nAfter fixes: {len(lines)} lines")

# Write back
with open('/workspace/app.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Written!")

# Check syntax
try:
    compile(''.join(lines), '/workspace/app.py', 'exec')
    print("SYNTAX OK!")
except SyntaxError as e:
    print(f"SYNTAX ERROR at line {e.lineno}: {e.msg}")