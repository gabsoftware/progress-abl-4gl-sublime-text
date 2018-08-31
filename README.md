# Progress ABL 4GL support for Sublime Text 3

By [GabSoftware](http://www.gabsoftware.com/)

If you want to add support for [Progress](http://www.progress.com/) ABL 4GL in [Sublime Text](http://www.sublimetext.com/), you can use this syntax plugin.
A ready-to-install package is located in the `dist` directory.

## Building

1. Zip the **content** of the OpenEdge ABL.sublime-package directory (not the directory itself)
2. Rename the archive to "OpenEdge ABL.sublime-package" (without .zip in the end of the file name)

## Installing or modifying

1. Close Sublime Text if necessary
2. Locate the data directory of Sublime Text 3 :
   * On Windows, it is located in `%APPDATA%\Sublime Text 3`
   * On Linux, it is located in `~/.config/sublime-text-3`
   * On OS X, it is located in `~/Library/Application Support/Sublime Text 3`
3. In the data directory, place the package `OpenEdge ABL.sublime-package` in the `Installed Packages` directory.
4. In the data directory (but in `%LOCALAPPDATA%\Sublime Text 3` in Windows!), delete the `Cache/OpenEdge ABL` directory
5. Restart Sublime Text
6. You may need to open each progress file type (.p, .cls, .i, .w...) and associate them with the new syntax scheme:
   `View > Syntax > Open all with current extension as... > OpenEdge ABL`

## "Check Syntax,Compile,Run" support with auto capitalization of keywords

It is possible to get the "Check Syntax,Compile,Run" feature of OpenEdge working in Sublime Text. To do so, you can follow these steps :

1. Makes sure you have saved your project, this creates a <project_name>.sublime-project
2. Update your <project_name>.sublime-project to add the settings.abl node
```
	{  
		"folders":  
		[  
			{  
				"path": "."  
			}  
		],  
		"settings":  
		{  
			"abl":  
			{  
				"dlc": "/path/to/dlc",  // Path to your DLC   
				"hooks":  
				{  
					"pre": "/code/to/run/pre.p" // This code will be run before compile,checking syntax or running but after propath bellow has been set  
				},  
				"pf": "conf/sublime.pf", // this path can be fully qualified or relative to the sublime-project file  
				"propath":  
				[  
					"src/module1", // these paths can be fully qualified or relative to the sublime-project file  
					"src/module2"  
				],  
				"uppercase_keywords": true // Do you want sublime to capitalize ABL Keywords  
			}  
		}  
	}
```
3. Hitting CTRL + SHIFT + B will give you a list
	- ABL                  : checks syntax
	- ABL - Check Syntax   : checks syntax
	- ABL - Compile        : compiles
	- ABL - Run Batch      : runs code in an \_progres -b session and returns messages to the sublime console
	- ABL - Run GUI        : runs the code in an prowin/32.exe
3. You can now repeat your last choice by hitting CTRL + B

This doesnt work on untitled buffers in sublime, the buffer must have a filename

## Notes

This product is not supported by Progress.
