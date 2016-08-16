# OSX Dock Remover
This is a tool to remove icons from the OSX Dock for all the users of the system. 

###### Basic Usage
```
python dock-icon-remove.py -r <partial_name_to_remove> -i <partial_name_to_ignore>
```
# Basic Examples
###### Remove all Microsoft icons except Microsoft Office 2011 icons
```
python dock-icon-remove.py -r "/Applications/Microsoft" -i "/Applications/Microsoft Office 2011"
```

###### Remove Microsoft PowerPoint icons but leave Microsoft PowerPoint 2011 icon
```
python dock-icon-remove.py -r "Microsoft PowerPoint" -i "/Applications/Microsoft Office 2011"
```
