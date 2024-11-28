import os
import shutil
import random


def split_files(source_dir, dest_dirs, split_ratios):
    # Upewnij się, że katalogi docelowe istnieją
    for dest_dir in dest_dirs:
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

    # Pobierz listę plików w katalogu źródłowym
    files = os.listdir(source_dir)
    total_files = len(files)
    file_indices = list(range(total_files))
    random.shuffle(file_indices)

    # Oblicz liczbę plików do każdego podziału
    num_files_to_split = [int(split_ratio * total_files) for split_ratio in split_ratios]

    # Podziel indeksy plików na trzy grupy
    start_idx = 0
    for dest_dir, num_files in zip(dest_dirs, num_files_to_split):
        end_idx = start_idx + num_files
        selected_indices = file_indices[start_idx:end_idx]
        start_idx = end_idx

        # Kopiuj wybrane pliki do katalogu docelowego
        for idx in selected_indices:
            file_name = files[idx]
            source_path = os.path.join(source_dir, file_name)
            dest_path = os.path.join(dest_dir, file_name)
            shutil.copyfile(source_path, dest_path)
            # print(f"Skopiowano plik: {file_name} do {dest_dir}")


if __name__ == "__main__":
    source_directory = "cat"
    test_directory = "test"
    train_directory = "train"
    val_directory = "val"

    # Podział plików: test - 10%, train - 90%
    split_ratios = [0.1, 0.9, 0.0]

    split_files("img/TIRADS1", ["img/test/TIRADS1", "img/train/TIRADS1", "img/val/TIRADS1"], split_ratios)
    split_files("img/TIRADS2", ["img/test/TIRADS2", "img/train/TIRADS2", "img/val/TIRADS2"], split_ratios)
    split_files("img/TIRADS3", ["img/test/TIRADS3", "img/train/TIRADS3", "img/val/TIRADS3"], split_ratios)
    split_files("img/TIRADS4", ["img/test/TIRADS4", "img/train/TIRADS4", "img/val/TIRADS4"], split_ratios)
    split_files("img/TIRADS5", ["img/test/TIRADS5", "img/train/TIRADS5", "img/val/TIRADS5"], split_ratios)
