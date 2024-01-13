import os

def find_gitignore(launch_directory:str, source_directory:str):

    current_dir = source_directory
    while True:
        gitignore_file = os.path.join(current_dir, '.gitignore')
        
        if os.path.isfile(gitignore_file):
            return gitignore_file
        elif current_dir == launch_directory:
            break
        else:
            print("current_dir")
            print(current_dir)
            print("os.path.dirname(current_dir)")
            print(os.path.dirname(current_dir))
            current_dir = os.path.dirname(current_dir)
            break
    return None