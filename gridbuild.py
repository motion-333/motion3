#!/usr/bin/env python3
"""
Script to auto-generate folders.json and files.json manifests under /static/pf.
- folders.json: list of subfolder names inside /static/pf
- files.json: for each subfolder, list of media files with metadata for the grid
"""
import os
import json

# Configuration
BASE_REL_PATH = 'static/pf'
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.gif'}
VIDEO_EXTS = {'.mp4', '.webm'}
DEFAULT_IMAGE_ROWS = 5
DEFAULT_VIDEO_ROWS = 8

# Resolve absolute path to /static/pf
BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), BASE_REL_PATH))
if not os.path.isdir(BASE_DIR):
    raise RuntimeError(f"Directory '{BASE_DIR}' does not exist.")

# Gather subfolders
folders = [d for d in sorted(os.listdir(BASE_DIR))
           if os.path.isdir(os.path.join(BASE_DIR, d))]

# Write folders.json
folders_manifest = os.path.join(BASE_DIR, 'folders.json')
with open(folders_manifest, 'w') as f:
    json.dump(folders, f, indent=2)
print(f"Wrote {folders_manifest} with {len(folders)} folders.")

# Generate files.json for each folder
for folder in folders:
    folder_path = os.path.join(BASE_DIR, folder)
    files = []
    for fname in sorted(os.listdir(folder_path)):
        _, ext = os.path.splitext(fname)
        ext = ext.lower()
        if ext in IMAGE_EXTS or ext in VIDEO_EXTS:
            ftype = 'video' if ext in VIDEO_EXTS else 'image'
            rows = DEFAULT_VIDEO_ROWS if ftype == 'video' else DEFAULT_IMAGE_ROWS
            cols = rows  # default square span; adjust manually in files.json if needed
            files.append({
                'name': fname,
                'type': ftype,
                'src': f"/static/pf/{folder}/{fname}",
                'cols': cols,
                'rows': rows
            })
    manifest_path = os.path.join(folder_path, 'files.json')
    with open(manifest_path, 'w') as mf:
        json.dump(files, mf, indent=2)
    print(f"Wrote {manifest_path} with {len(files)} media files.")
