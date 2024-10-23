import os
import shlex
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama 
init()

def get_file_info(paths):
    all_file_info = {}
    
    for path in paths:
        try:
            if os.path.isfile(path):  # If the path is a file
                size = os.path.getsize(path)
                modified_time = os.path.getmtime(path)
                modified_date = datetime.fromtimestamp(modified_time).strftime('%d/%m/%Y %I:%M %p')
                file_name = os.path.basename(path)
                all_file_info[path] = {'name': file_name, 'size': size, 'modified': modified_date}
                
            elif os.path.isdir(path):  # If the path is a folder
                folder_info = {}
                for file_name in os.listdir(path):
                    file_path = os.path.join(path, file_name)
                    if os.path.isfile(file_path):
                        size = os.path.getsize(file_path)
                        modified_time = os.path.getmtime(file_path)
                        modified_date = datetime.fromtimestamp(modified_time).strftime('%d/%m/%Y %I:%M %p')
                        folder_info[file_name] = {'size': size, 'modified': modified_date}
                all_file_info[path] = folder_info
                
            else:
                print("Path '{}' is neither a file nor a folder.".format(path))
                
        except Exception as e:
            print("Error accessing '{}': {}".format(path, str(e)))

    return all_file_info


def format_file_size(size):
    # if size >= 1024 * 1024:  # Size in MB
    #     return '{:.2f} MB'.format(size / (1024 * 1024))
    if size >= 1024:  # Size in KB
        return '{:,.0f} KB'.format(size / 1024)
    else:  # Size in bytes
        return '{} bytes'.format(size)

def get_user_paths():
    paths = []
    user_input = input(Fore.YELLOW + 'Enter the file or folder paths (space-separated) enclose paths with quote ("): ').strip()
    print(Style.RESET_ALL)
    paths = shlex.split(user_input)

    # Check if path exist
    valid_path = []
    for path in paths:
        if os.path.exists(path):
            valid_path.append(path)
        else:
            print(Fore.RED + 'The path "{}" does not exist.'.format(path) + Style.RESET_ALL)

    return paths

def save_to_file(all_file_info, filename):
    with open(filename, 'w') as f:
        for path, details in all_file_info.items():
            if isinstance(details, dict):
                if 'size' in details:
                    formatted_size = format_file_size(details['size'])
                    f.write(f"{details['name']}\n{formatted_size}\n{details['modified']}\n\n")
                else:
                    f.write(f"Files in: {path}\n")
                    for file_name, file_details in details.items():
                        formatted_size = format_file_size(file_details['size'])
                        f.write(f"  {file_name}\n  {formatted_size}\n  {file_details['modified']}\n")
                        f.write("\n")
                    f.write("\n")

# Replace with the actual folder path
# folder_paths = [
#     'C:\\wamp64\\www\\co_web_2\\package.json',
#     'C:\\wamp64\\www\\co_web_2'
# ]
folder_paths = get_user_paths()
info = get_file_info(folder_paths)
for path, details in info.items():
    if isinstance(details, dict):
        if 'size' in details:
            formatted_size = format_file_size(details['size'])
            print(Fore.GREEN + '\033[1m{} \n'.format(details['name']) + Style.RESET_ALL + '{}\n{}'.format(formatted_size, details['modified']) + Style.RESET_ALL)
        else:
            print(Fore.MAGENTA + 'Files in: {}'.format(path) + Style.RESET_ALL)
            for file_name, file_details in details.items():
                formatted_size = format_file_size(file_details['size'])
                print(Fore.GREEN + '  \033[1m{} \n'.format(file_name) + Style.RESET_ALL + '  {}\n  {}'.format(formatted_size, file_details['modified']) + Style.RESET_ALL)

print()
save_to_file(info, 'file_info.txt')
print('Saved output to file_info.txt')
input('Press any key to end...')