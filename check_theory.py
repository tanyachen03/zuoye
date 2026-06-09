#!/usr/bin/env python3
with open('/workspace/app.py', 'r') as f:
    lines = f.readlines()

l218 = lines[217]
print("Line 218 ends with:", repr(l218[-80:]))
l194 = lines[193]
print("\nLine 194 starts with:", repr(l194[:60]))
print("Line 194 starts with single quote:", l194.strip().startswith("'<h3>"))

open_q = l194.find("'")
close_q = l218.rfind("'")
print("\nLine 194 first quote at:", open_q)
print("Line 218 last quote at:", close_q)

# Check the theory string content
theory = ''.join(lines[193:218])
print("\nTheory content length:", len(theory))
print("Theory starts:", repr(theory[:50]))
print("Theory ends:", repr(theory[-50:]))