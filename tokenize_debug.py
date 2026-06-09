#!/usr/bin/env python3
"""
Use Python's tokenize module to find the EXACT positions of string tokens
and identify which ones are corrupted theory strings.
"""
import tokenize
import io

with open('/workspace/app.py', 'rb') as f:
    content = f.read()

print(f"File size: {len(content)} bytes")

# Use tokenize to find all string tokens
tokens = []
try:
    g = tokenize.tokenize(io.BytesIO(content).readline)
    for tok in g:
        if tok.type == tokenize.STRING:
            tokens.append((tok.start, tok.end, tok.string))
except tokenize.TokenError as e:
    print(f"TokenError: {e}")

print(f"\nFound {len(tokens)} string tokens")

# Look for string tokens that:
# 1. Start with '<h3>' (corrupted theory)
# 2. Are very long (theory strings)
# 3. Are multi-line (indented continuation)

for i, (start, end, s) in enumerate(tokens[:20]):
    print(f"\nToken {i}: lines {start[0]}-{end[0]}, start={start}, string={repr(s[:100])}")
    if s.startswith("'<h3>") or s.startswith("'<h3>"):
        print("  *** CORRUPTED THEORY? Starts with single quote <h3>")