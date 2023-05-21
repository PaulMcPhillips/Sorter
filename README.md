Sorter App to Automatically sort file types into a new folder

The app is provided as a script.

It can be turned into an executable with PyInstaller from the command line by navigating
to the folder where the script is installed then running:

pyinstaller --onefile -n "Sorter" -w ./sorter.py

This will create a Dist folder which will contain the executable of the script.

To use Sorter, simply click the Choose Folder button, select the folder where the files
are saved. The list of executables will automatically populate in the drop down menu.

Enter a name for the new folder, hit enter to see visual validation of the folder path.

From the drop down menu, choose the file type to be sorted into the new folder then click
Sort, to create the new folder and move all the files into the new folder.
