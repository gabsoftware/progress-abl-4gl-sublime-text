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

## "Check Syntax" support

It is possible to get the "Check Syntax" feature of OpenEdge working in Sublime Text. To do so, you can use the provided files in the `CheckSyntax` directory :

1. Close Sublime Text
2. Place the `syntax.p` file in a directory or your choice, for example `C:\syntax`
3. Copy the files `ABL.sublime-build.example` and `ABL.sublime-settings` and paste them in the data directory, in `Packages\User`
4. Rename `ABL.sublime-build.example` to `ABL.sublime-build`
5. Modify `ABL.sublime-build` to reflect your configuration
6. Restart Sublime Text
7. You can now check the syntax of Progress ABL source files by hitting CTRL + B

## Notes

This product is not supported by Progress.