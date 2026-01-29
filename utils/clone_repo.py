import os
import shutil
import git
import stat

def handle_remove_readonly(func, path, _):
    # Change permission and retry delete
    os.chmod(path, stat.S_IWRITE)
    func(path)


def clone_repo(repo_url, local_dir="cloned_repo"):
    # If the directory already exists, delete it
    if os.path.exists(local_dir):
        shutil.rmtree(local_dir, onerror=handle_remove_readonly)
    
    # Clone the repo fresh
    git.Repo.clone_from(repo_url, local_dir)
    return local_dir