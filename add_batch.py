#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

def get_file_size(filepath):
    """Get file size in bytes"""
    return os.path.getsize(filepath)

def run_git_command(args, check=True):
    """Run a git command and return output"""
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        check=check
    )
    return result

def get_untracked_and_modified_files():
    """Get list of untracked and modified files"""
    # Get untracked files
    result = run_git_command(["ls-files", "--others", "--exclude-standard"])
    untracked = [f for f in result.stdout.strip().split('\n') if f]
    
    # Get modified but not staged
    result = run_git_command(["diff", "--name-only"])
    modified = [f for f in result.stdout.strip().split('\n') if f]
    
    all_files = list(set(untracked + modified))
    return [f for f in all_files if os.path.exists(f)]

def add_until_size(target_size_gb=1):
    """
    Add files up to target_size_gb and commit once, then exit
    """
    target_size = target_size_gb * 1024 * 1024 * 1024
    
    files = get_untracked_and_modified_files()
    
    if not files:
        print("No untracked or modified files found.")
        return
    
    print(f"Found {len(files)} files to process")
    print(f"Target: ~{target_size_gb} GB for this commit\n")
    
    # Sort by size (smallest first to maximize file count, or largest first - your choice)
    files_with_sizes = [(f, get_file_size(f)) for f in files]
    files_with_sizes.sort(key=lambda x: x[1])  # Smallest first
    
    batch = []
    batch_size = 0
    
    for filepath, size in files_with_sizes:
        # Skip if single file exceeds target (would make commit too big)
        if size > target_size:
            print(f"⚠️  Skipping {filepath} ({size/1e9:.2f}GB) - exceeds target size")
            continue
        
        # Stop if adding this file would exceed target
        if batch_size + size > target_size and batch:
            break
        
        batch.append(filepath)
        batch_size += size
    
    if not batch:
        print("No files fit within the target size.")
        return
    
    # Add files
    size_gb = batch_size / (1024 * 1024 * 1024)
    print(f"Adding {len(batch)} files ({size_gb:.2f} GB):")
    
    for i, filepath in enumerate(batch, 1):
        print(f"  ({i}/{len(batch)}) {filepath}")
        run_git_command(["add", filepath])
    
    # Commit
    commit_msg = f"Add {len(batch)} files ({size_gb:.2f} GB)"
    print(f"\nCommitting: {commit_msg}")
    run_git_command(["commit", "-m", commit_msg])
    
    print(f"\n✅ Done. Committed {len(batch)} files ({size_gb:.2f} GB)")
    
    remaining = len(files) - len(batch)
    if remaining > 0:
        print(f"\n{remaining} files remain uncommitted.")
        print("Run the script again to commit the next batch.")

def main():
    # Check if we're in a git repo
    try:
        result = subprocess.run(["git", "rev-parse", "--show-toplevel"], 
                                capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError:
        print("Error: Not a git repository")
        sys.exit(1)
    
    add_until_size(target_size_gb=1)

if __name__ == "__main__":
    main()
