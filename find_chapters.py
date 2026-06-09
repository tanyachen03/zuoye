#!/usr/bin/env python3
"""
Systematic fix for all corrupted make_chapter calls in app.py.
Strategy: Find each make_chapter's start, identify the 5 parameters (theory, code_example, quiz, starter_code),
and rebuild them with proper triple-quoted strings.
"""
import re

with open('/workspace/app.py', 'r', encoding='utf-8') as f:
    data = f.read()

# Strategy: 
# 1. Find all make_chapter(N, ...) calls where N is a number and the theory string starts with '<h3>'
# 2. Each corrupted make_chapter has theory string that runs to end of line without closing
# 3. After the theory string, there are orphaned code_example lines
# 4. Then quiz, then starter_code
# 5. We need to find the END of each make_chapter and rebuild it

# First, let's find ALL make_chapter( calls and analyze their structure
pattern = r"make_chapter\((\d+), '([^']+)', '([^']+)',"
matches = list(re.finditer(pattern, data))

print(f"Found {len(matches)} make_chapter calls")

# For each match, find the extent of that make_chapter call
results = []
for m in matches:
    chapter_num = int(m.group(1))
    chapter_title = m.group(2)
    start_pos = m.start()
    
    # Find the end: look for '), that closes this make_chapter
    # We look for the pattern: starter_code_string_end '), new_make_chapter or end of dict
    # Search forward from start_pos for the end marker
    search_region = data[start_pos:start_pos+5000]
    
    # Look for the closing pattern: '),  (starter_code string closing + make_chapter close)
    # The starter_code is a string like 'import numpy as np...'
    # We look for ...mean())'), which appears at the end of many chapters
    end_match = re.search(r"mean\(\)\'\),", search_region)
    if end_match:
        end_pos = start_pos + end_match.end()
        results.append((chapter_num, chapter_title[:30], start_pos, end_pos, search_region[:100]))
    else:
        # Try other patterns
        end_match2 = re.search(r"\)'\),", search_region)
        if end_match2:
            end_pos = start_pos + end_match2.end()
            results.append((chapter_num, chapter_title[:30], start_pos, end_pos, search_region[:100]))
        else:
            results.append((chapter_num, chapter_title[:30], start_pos, -1, "NO END FOUND"))

for r in results[:10]:
    print(f"Chapter {r[0]}: {r[1]}... start={r[2]}, end={r[3]}")
    print(f"  Preview: {r[4]}")