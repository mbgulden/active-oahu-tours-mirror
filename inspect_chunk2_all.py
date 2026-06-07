def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    diff_text = read_file('nav_diff.txt')
    lines = diff_text.splitlines()
    
    # We want to print every added and removed line in Chunk 2
    current_chunk = []
    chunk_index = 0
    for line in lines:
        if line.startswith('@@'):
            chunk_index += 1
        if chunk_index == 2:
            current_chunk.append(line)
            
    print(f"Chunk 2 has {len(current_chunk)} lines total.")
    print("Listing all modifications (+ or -) in Chunk 2:")
    for line in current_chunk:
        if line.startswith('+') or line.startswith('-'):
            if not line.startswith('+++') and not line.startswith('---'):
                print(line)

if __name__ == '__main__':
    main()
