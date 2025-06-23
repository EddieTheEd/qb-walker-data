import os

def find_large_files(folder_path, size_limit_bytes=100 * 1024 * 1024):
    large_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            try:
                size = os.path.getsize(full_path)
                if size > size_limit_bytes:
                    large_files.append((full_path, size))
            except Exception as e:
                print(f"Could not check size of {full_path}: {e}")
    return large_files

folder =input("Folder?\n") 
large_files = find_large_files(folder)

if large_files:
    print("Files larger than 100 MiB:")
    for path, size in large_files:
        print(f"{path} — {size / (1024 * 1024):.2f} MiB")
else:
    print("No files over 100 MiB.")

