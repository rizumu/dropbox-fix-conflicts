#! /usr/bin/env python
# coding=utf8
import os, re, shutil, sys

# example usage 
# python fixconflicts.py Movies
# where Movies is the name of the folder in conflict

def get_conflict_folders(folder_name, conflict_regex):
	"""
	Return all folder names that contain passed in folder_name
	and the string (Case Conflict *)
	"""
	parent = os.path.dirname(os.path.abspath(folder_name))
	siblings = os.listdir(parent)
	conflicted_folders = []
	for sibling in siblings:
		if re.match(conflict_regex, sibling):
			conflicted_folders.append(sibling)
	return conflicted_folders

def get_files(conflict_folder):
	"""
	Return all files and their relative pathnames for the conflicted folder
	"""
	pathnames = []
	for root, dirs, files in os.walk(conflict_folder):
		for name in files:
			pathnames.append((root, name))
	return pathnames
		
def move_files(root_folder, pathnames):
	"""
    1. If file already exists display error and quit.
    2. Copy each file to the passed in folder name. (ex. Movies) If parent
        folders do not exist, make the folder tree.
    3. If successful, remove file
    4. After all files are copied successfully, remove the conflict folders.
	"""
	for pathname in pathnames:
		source = os.path.join(pathname[0], pathname[1])
		match_list = re.match('[^/]+/(.*)', pathname[0])
		if match_list:
			relative_pathname = match_list.group(1)
			full_pathname = os.path.join(root_folder, relative_pathname)
			destination = os.path.join(full_pathname, pathname[1])
			if not os.path.exists(full_pathname):
				os.makedirs(full_pathname) # makes the folder if nonexist
			os.rename(source, destination) # moves the file		

def main():
	conflict_regex = '^%s \(Case Conflict \d+\)' % (sys.argv[1],)
	conflicted_folders = get_conflict_folders(sys.argv[1], conflict_regex)
	for folder in conflicted_folders:
		pathnames = get_files(folder)
		move_files(sys.argv[1], pathnames)
		
	for folder in conflicted_folders:
		shutil.rmtree(folder)
	

if __name__ == "__main__":
    sys.exit(main())
