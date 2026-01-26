"""Read log file and search for last specified record."""


from app_modules.utilities import get_last_log_segment


def get_last_hlap_rec_count(entries):  # sourcery skip: use-next
    """Get the hlap record count."""
    for entry in sorted(entries, reverse=True):
        if 'Total bills:' in entry:
            return entry
    return None


def get_print_count(line):
    """Extract record count from line."""
    return int(line.split(': ')[1])


def check_count(actual_count):
    """Get bill count from log file entry of PRN file create."""
    entries = get_last_log_segment()
    hlap_rec = get_last_hlap_rec_count(entries)
    expected_count = get_print_count(hlap_rec) if hlap_rec else None
    return expected_count == actual_count


def check_idx_file(index_file, first_acc, last_acc, actual_count):
    """Check created index file makes sense."""
    with open(index_file, encoding='utf8') as idx_file:
        entries = idx_file.readlines()
    first_line = entries[0].split(',')
    last_line = entries[-1].split(',')
    actual_count = int(actual_count)
    return {
        'count_ok': check_count(actual_count),
        'idx_lines_ok': len(entries) == actual_count,
        'first_acc_ok': int(first_line[0]) == int(first_acc),
        'first_idx_ok': int(first_line[1]) == int(first_line[2]) == 1,
        'last_acc_ok': int(last_line[0]) == int(last_acc),
        'last_idx_ok': int(last_line[1]) == int(last_line[2]) == actual_count
    }


if __name__ == '__main__':
    arg1 = ['B47001_02_202103_47001.spdfi', '0075941001', '0014683001', '6877']
    print(all(check_idx_file(*arg1).values()))
