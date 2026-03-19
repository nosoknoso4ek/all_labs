import subprocess

def human_readable_size(size_bytes):
    units = ['B','KiB','MiB','GiB','TiB']
    size = float(size_bytes)
    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PiB"

def get_summary_rss(file_path):
    total_rss = 0
    with open(file_path, 'r') as f:
        lines = f.readlines()[1:]
        for line in lines:
            columns = line.split()
            if len(columns) > 5:
                total_rss += int(columns[5]) * 1024
    return human_readable_size(total_rss)

if __name__ == "__main__":
    output_file = "output_file.txt"
    with open(output_file, 'w') as f:
        subprocess.run(["ps","aux"], stdout=f)
    result = get_summary_rss(output_file)
    print(result)
