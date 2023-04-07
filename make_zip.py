"""
Automatically package and sign SHBT release
"""

import shutil
import json
import pathlib
import sys
import os

def print_help():
	print("Usage:")
	print(f"{sys.argv[0]} [branches ...]")

def load_json(filename):
	"""
	Load a json data file
	"""
	
	return json.loads(pathlib.Path(filename).read_text())

def save_json(filename, content):
	"""
	Save a json file with nice formatting
	"""
	
	return pathlib.Path(filename).write_text(json.dumps(content, sort_keys = True, indent = 4))

def load_bl_info(basedir):
	"""
	This is the same as the function in blender tools in common.py
	"""
	
	filename = f"{basedir}/blender_tools.py"
	blinfo = pathlib.Path(filename).read_text()
	blinfo = eval(blinfo[blinfo.index("{"):blinfo.index("}") + 1])
	
	return blinfo

def make_version(l):
	return str(l[0]) + "." + str(l[1]) + "." + str(l[2])

def update_updater_info(bl_info, branches):
	"""
	Update the updater info to match
	"""
	
	# Read in update file
	info = load_json("update.json")
	
	for branch in branches:
		# Make the branch if it doesn't exist
		if (not info.get(branch, None) == None):
			info[branch] = {}
		
		# Update version and download info
		info[branch]["version"] = bl_info["version"]
		version = make_version(bl_info["version"])
		info[branch]["download"] = f"https://github.com/smashing-tech/Smash-Hit-Blender-Tools/releases/download/{version}/shbt_{version}.zip"
	
	# Save update file
	save_json("update.json", info)

def main():
	"""
	Package the release and sign it
	"""
	
	# Load config
	conf = load_json("make_zip_config.json")
	
	# Get config values
	private = conf.get("private_key", "../shbt-private.key")
	folder = conf.get("basedir", "../Smash-Hit-Blender-Tools")
	
	# Get version
	bl_info = load_bl_info(folder)
	version = make_version(bl_info["version"])
	
	# Get branch, if none provided then just use prerelease
	branches = sys.argv[1] if len(sys.argv) >= 2 else ["prerelease"]
	
	# Update "update.json" file
	print(f"Updating updater info file ...")
	
	update_updater_info(bl_info, branches)
	
	# Make archive base name
	zip_file = f"shbt_{version}"
	
	# Make the archive file itself
	print(f"Creating archive '{zip_file}.zip' ...")
	
	shutil.make_archive(f"../{zip_file}", "zip", folder, "")
	
	# Sign the update
	print(f"Creating signature '{zip_file}.zip.sig' ...")
	
	import sign_update
	
	sign_update.sign_file(f"../{zip_file}.zip", private)
	
	# Update meta git repo
	print(f"Git commit to meta repo ...")
	
	os.system(f"git add .")
	os.system(f"git commit -m \"Bump version to {version}\"")

if (__name__ == "__main__"):
	main()
