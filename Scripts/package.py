import shutil
import os

# Get the current working directory
cwd = os.getcwd()
print(cwd)
# Package
shutil.make_archive(base_name="./Python/bin/cc_manage_lambda", base_dir="./Python/App", format="zip")