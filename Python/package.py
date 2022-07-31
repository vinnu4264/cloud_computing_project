import shutil
import os

# Get the current working directory
cwd = os.getcwd()
print(cwd)
# Package
shutil.make_archive(base_name="./bin/cc_manage_lambda", base_dir="./App", format="zip")