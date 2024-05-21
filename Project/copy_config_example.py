# Used to copy the .example file under configs in batches and name it as .py file
import os
import shutil

if __name__ == "__main__":
    files = os.listdir("configs")

    src_files = [os.path.join("configs", file) for file in files if ".example" in file]

    for src_file in src_files:
        tar_file = src_file.replace(".example", "")
        shutil.copy(src_file, tar_file)
