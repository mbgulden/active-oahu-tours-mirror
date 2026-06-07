import re

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    diff_text = read_file('nav_diff.txt')
    
    # Let's count how many differences there are, and classify them.
    # We want to check for links difference, logo loading="lazy", weglot translation widget, etc.
    
    # Let's write a python script to inspect differences in detail.
    # First, let's print the entire nav_diff.txt or at least summarize it by looking at lines starting with '+' or '-'
    lines = diff_text.splitlines()
    print(f"Total lines in diff: {len(lines)}")
    
    # Let's print lines around changes to understand the major changes.
    changes = []
    current_chunk = []
    for line in lines:
        if line.startswith('@@'):
            if current_chunk:
                changes.append(current_chunk)
                current_chunk = []
            current_chunk.append(line)
        elif current_chunk:
            current_chunk.append(line)
    if current_chunk:
        changes.append(current_chunk)
        
    print(f"Number of difference chunks: {len(changes)}")
    for i, chunk in enumerate(changes):
        print(f"\n--- Chunk {i+1} ---")
        # print first 15 lines of chunk
        for line in chunk[:20]:
            print(line)
        if len(chunk) > 20:
            print(f"... ({len(chunk)-20} more lines)")

if __name__ == '__main__':
    main()
