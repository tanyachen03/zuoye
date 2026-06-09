#!/usr/bin/env python3
"""
Find all make_chapter calls and their positions to understand the corruption.
"""
import re

with open('/workspace/app.py', 'r', encoding='utf-8') as f:
    data = f.read()

# Find all make_chapter calls
pattern = r"make_chapter\((\d+), '([^']+)', '([^']+)',"
matches = list(re.finditer(pattern, data))

print(f"Found {len(matches)} make_chapter calls")

for i, m in enumerate(matches):
    chapter_num = int(m.group(1))
    title = m.group(2)
    start_pos = m.start()
    line_num = data[:start_pos].count('\n') + 1
    
    # Look for the end of this make_chapter
    # Search for '),  which closes the make_chapter
    search_start = m.end()
    end_pattern = data[search_start:search_start+100]
    
    # Find where the theory string ends (look for ), pattern after HTML content)
    # We search for the closing of the 5th argument
    # Pattern: starter_code_string_end '), 
    # Or we search for the next make_chapter
    
    if i + 1 < len(matches):
        next_start = matches[i+1].start()
        gap = next_start - start_pos
        print(f"Chapter {chapter_num}: pos {start_pos}-{next_pos}, gap: {gap}")
    else:
        print(f"Chapter {chapter_num}: pos {start_pos}, LAST")

# Now find actual end of each make_chapter by looking for '), followed by whitespace or make_chapter
print("\n--- Finding actual end positions ---")
for i, m in enumerate(matches[:5]):  # First 5 chapters
    chapter_num = int(m.group(1))
    start = m.start()
    
    # Look for pattern: mean())'), or similar - the closing of starter_code + closing of make_chapter
    # Search in the region up to next make_chapter
    if i + 1 < len(matches):
        end_search_start = matches[i+1].start()
    else:
        end_search_start = start + 10000
    
    region = data[start:end_search_start]
    
    # Find the pattern: '),  which closes the make_chapter
    # Look for: )'),  or similar patterns
    match = re.search(r"mean\(\)\'\),", region)
    if match:
        actual_end = start + match.end()
        print(f"Chapter {chapter_num}: make_chapter ends at byte {actual_end}")
        print(f"  Content around end: {repr(region[match.start()-20:match.end()+20])}")