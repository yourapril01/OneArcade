#!/usr/bin/env python3
"""
xml_patch.py: A utility tool to apply block replacements to XML files.
Supports exact matching and flexible whitespace matching.
"""

import os
import sys
import re
import argparse

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def log(msg: str, color: str = '', quiet: bool = False):
    if not quiet:
        print(f"{color}{msg}{Colors.RESET if color else ''}")

def log_error(msg: str):
    print(f"{Colors.RED}{msg}{Colors.RESET}")

def parse_xml_patch(lines: list) -> list:
    """Parses the FILE, REPLACE, and END format."""
    files = []
    current_file = None
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 1. Find FILE
        if line.startswith('FILE '):
            current_file = {'file_path': line[5:].strip(), 'actions': []}
            files.append(current_file)
            i += 1
            
        # 2. Find REPLACE
        elif line.startswith('REPLACE') and current_file is not None:
            search_lines = []
            first_line = line[7:].strip()
            if first_line:
                search_lines.append(first_line)
            i += 1
            
            # Read search block until an empty line separates it from the replace block
            while i < len(lines) and lines[i].strip() != '':
                search_lines.append(lines[i])
                i += 1

            # Skip the empty lines
            while i < len(lines) and lines[i].strip() == '':
                i += 1

            replace_lines = []
            # Read replace block until END or another keyword
            while (i < len(lines) and 
                   lines[i].strip() != 'END' and 
                   not lines[i].startswith('FILE ') and 
                   not lines[i].startswith('REPLACE')):
                replace_lines.append(lines[i])
                i += 1

            current_file['actions'].append({
                'search': '\n'.join(search_lines),
                'replace': '\n'.join(replace_lines)
            })

            # Consume END tag if present
            if i < len(lines) and lines[i].strip() == 'END':
                i += 1
        else:
            i += 1

    return files

def apply_patch_to_file(work_dir: str, file_patch: dict, quiet: bool) -> bool:
    target_path = os.path.join(work_dir, file_patch['file_path'])
    
    if not os.path.exists(target_path):
        log_error(f"   ✗ File not found: {file_patch['file_path']}")
        return False

    log(f"  Patching: {file_patch['file_path']}", Colors.YELLOW, quiet)

    with open(target_path, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False
    for idx, action in enumerate(file_patch['actions']):
        search_text = action['search']
        replace_text = action['replace']

        # Attempt 1: Exact literal match
        if search_text in content:
            content = content.replace(search_text, replace_text)
            modified = True
            log(f"    ✓ Applied REPLACE block #{idx + 1} (Exact Match)", Colors.GREEN, quiet)
            
        else:
            # Attempt 2: Fuzzy match (ignores spaces/newlines variations in XML)
            words = search_text.split()
            pattern = r'\s+'.join(re.escape(w) for w in words)
            
            match = re.search(pattern, content)
            if match:
                content = content[:match.start()] + replace_text + content[match.end():]
                modified = True
                log(f"    ✓ Applied REPLACE block #{idx + 1} (Fuzzy Match)", Colors.GREEN, quiet)
            else:
                log_error(f"   ✗ XML block not found for REPLACE #{idx + 1}")
                log_error(f"     Looking for: {search_text[:60]}...")
                return False

    if modified:
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    return True

def main():
    parser = argparse.ArgumentParser(description='Apply block replacements to XML files.')
    parser.add_argument('work_dir', help='Root directory containing decompiled files')
    parser.add_argument('patch_file', help='Path to .xmlpatch file')
    parser.add_argument('-q', '--quiet', action='store_true')
    args = parser.parse_args()

    if not os.path.isdir(args.work_dir):
        log_error(f"ERROR: Directory not found {args.work_dir}")
        sys.exit(1)

    if not os.path.isfile(args.patch_file):
        log_error(f"ERROR: Patch file not found {args.patch_file}")
        sys.exit(1)

    with open(args.patch_file, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    patches = parse_xml_patch(lines)

    if not patches:
        log_error("ERROR: No valid patches found")
        sys.exit(1)

    log(f"Found {len(patches)} file(s) to patch", Colors.BLUE, args.quiet)
    log("=" * 50, '', args.quiet)

    success_count = 0
    for patch in patches:
        if apply_patch_to_file(args.work_dir, patch, args.quiet):
            success_count += 1
        log("", '', args.quiet)

    log("=" * 50, '', args.quiet)
    if success_count == len(patches):
        log(f" Success: {success_count}/{len(patches)} files patched", Colors.GREEN, args.quiet)
        sys.exit(0)
    else:
        log_error(f" Failed: {success_count}/{len(patches)} files patched")
        sys.exit(1)

if __name__ == '__main__':
    main()

