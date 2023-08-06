import os
import shutil

def updateCanary(): 
  directory = os.getcwd()

  source_path = directory + "\\dist"

  dirs = directory.split('\\')
  current_dir = dirs[len(dirs)-1]

  print("\nPackage: " + current_dir + "\n")

  os.chdir("../../../pa3-frontend/node_modules/@fds")
  fullpath = os.path.abspath(os.curdir)

  found = False

  for dirs in os.walk(fullpath).__next__()[1]:
    if dirs == current_dir or dirs == 'pa-'+current_dir or dirs == 'pa3-'+current_dir:
      destination_path = fullpath + "\\" + dirs + "\\dist"
      print(dirs + " package found in pa3-frontend\n")
      found = True
      break

  if found == True:
    print("\nUpdating " + current_dir + " package")

    print("Removing older dist...")
    shutil.rmtree(destination_path)

    print("Copying new dist...")
    shutil.copytree(source_path, destination_path)
    print("done!")

    print("\nSUCCESS: " + current_dir + " package updated")

  else: 
    print("\nFAIL: "+ current_dir + " package not found!")