from threading import Thread
from pathlib import Path
import shutil
from multiprocessing import Pool, cpu_count
import sys

threads = []

def copy_file(file_path: Path, dest_root: Path):
    ext = file_path.suffix[1:] if file_path.suffix else 'no_extension'
    dest_folder = dest_root / ext
    dest_folder.mkdir(parents=True, exist_ok=True)

    shutil.copy2(file_path, dest_folder / file_path.name)
    print(f'Copied {file_path} to {dest_folder / file_path.name}')


def walk_and_copy(path: Path, dest_root: Path):
    global threads
    for item in path.iterdir():
        if item.is_dir():
            walk_and_copy(item, dest_root)
        elif item.is_file():
            thread = Thread(target=copy_file, args=(item, dest_root))
            thread.start()
            threads.append(thread)


def factorize_single(n):
    return [i for i in range(1, n + 1) if n % i == 0]


def factorize(*numbers):
    with Pool(processes=cpu_count()) as pool:
        return pool.map(factorize_single, numbers)


if __name__ == '__main__':
    # --- Part 1: File sorting by extension
    if len(sys.argv) < 2:
        print("Usage: python script.py <source_dir> [<destination_dir>]")
        sys.exit(1)

    source = Path(sys.argv[1])
    destination = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("dist")

    if not source.exists():
        print(f'Dont find {source}')
    else:
        destination.mkdir(exist_ok=True)
        walk_and_copy(source, destination)
        for t in threads:
            t.join()
        print('All files copied successfully.')

    # --- Part 2: Multiprocessing factorizationw
    a, b, c, d = factorize(128, 255, 99999, 10651060)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140,
                 76079, 152158, 304316, 380395, 532553, 760790,
                 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
    print("Factorization passed.")