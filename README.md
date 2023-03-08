# KUKA-TOOL-AND-BASE-COMPARISON
This editor allows to compare bases and tools of the Kuka robots.

# Table of contents
  - General Info
  - Technologies Used
  - Features
  - Screenshots
  - Setup
  - Usage
  - Project Status
  - Contact
 
 # General Information
The editor allows to load bases and tools of the Kuka robots from different sources (e.g. backup and .olp files). The main idea of this editor is the ability to quickly
compare tools and bases (what is inside the backup and what has been measured or generated by Process Simulate). The editor allows you to see data in two windows 
(the left window shows data from backup, the right one from .olp files), see differences, generate reports and export data from offline. It allows to quickly find out 
where there is a big difference in frame values, which can cause offline programs not to match.

# Technologies Used 
  - Python - version 3.9.16,
  - PyQt5 - version 5.15.9.
  
# Features
List the ready features here:
- Load from kuka backup - allows to load all tools and bases and their values from the config.dat file available in the kuka robot backup. These data are displayed 
in the left window.
- Load from olp files - allows to load all tools and bases and their values from the .olp files available in the selected directory generated by Process Simulate
or a measurement report. These data are displayed in the right window.
- Compare - allows to compare bases and tools loaded from Kuka backup (the left window) and those loaded from .olp files (the right window). If there is a value 
difference, the background color of the specified frame changes to red. It allows to find frames where there are differences.
- Save existing olp data - allows to export all tools and bases and their values available in the right window to a .txt file. The data is in krl format ready to be 
uploaded to the kuka robot.
- Create report - allows to generate a report as a .txt file, which contains differences in X, Y, Z, A, B, C between frames loaded from a backup and those loaded from
.olp files.

# Screenshots
Basic view of the editor (the left layout shows available options, the middle one frames loaded from a robot backup, the right one frames loaded from .olp files).
All frames have default values: 
![image](https://user-images.githubusercontent.com/86266104/223544405-ff2c17f7-6d31-411a-a730-44b18210c834.png)
The editor view after loading data from a backup (on the left side) and after loading from a directory with .olp files (on the right side):
![image](https://user-images.githubusercontent.com/86266104/223553183-81546e65-c73d-4017-971b-511289e1c9fa.png)
Editor view after selecting the compare option:
![image](https://user-images.githubusercontent.com/86266104/223648311-f792dd35-7355-474e-8f05-02aac0ed3737.png)
Data generated after selecting the save existing olp data option (in krl syntax):
![image](https://user-images.githubusercontent.com/86266104/223648720-fe64f86e-950b-4971-a277-f5a1ae0aecd7.png)

Data generated after selecting the create report option:
This allows to easily find the answer why offline programs could not fit.
![image](https://user-images.githubusercontent.com/86266104/223656918-67960612-8808-46d9-8293-348082a5ad91.png)

# Setup
- Install Python on your computer. You can download it from https://www.python.org/downloads/.
-	Install python package PyQt5, (using pip installer) in the appropriate versions.
-	Clone this repository. 
	
# Usage
If you want to start the application double click on the main.py file or use cmd and type python main.py.
	
# Project Status
Project is completed. 
	
# Contact
Created by Mateusz Ptak (mateusz.ptak@op.pl, mobile 696 166 418) - feel free to contact me!
