import sys

def get_mean_size(lines):
    total_size = 0
    count = 0
    
    for line in lines[1:]:  # пропускаем первую строку
        columns = line.split()
        if len(columns) < 5:
            continue
        try:
            size = int(columns[4])  # 5-й столбец — размер
            total_size += size
            count += 1
        except ValueError:
            continue

    if count == 0:
        return 0
    return total_size / count


if __name__ == "__main__":
    lines = sys.stdin.readlines()
    mean_size = get_mean_size(lines)
    print(f"{mean_size:.2f}")
