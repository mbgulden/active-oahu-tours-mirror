import re

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    diff_text = read_file('nav_diff.txt')
    lines = diff_text.splitlines()
    
    # Print the second chunk completely
    current_chunk = []
    chunk_index = 0
    for line in lines:
        if line.startswith('@@'):
            chunk_index += 1
        if chunk_index == 2:
            current_chunk.append(line)
            
    print("=== CHUNK 2 COMPLETE ===")
    for line in current_chunk:
        print(line)

if __name__ == '__main__':
    main()
