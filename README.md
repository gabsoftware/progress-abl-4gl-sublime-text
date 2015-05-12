# progress-abl-4gl-sublime-text
Progress ABL 4GL support for Sublime Text 3
By GabSoftware

== Building ==
1. Zip the *content* of the OpenEdge ABL.sublime-package directory
2. Rename it "OpenEdge ABL.sublime-package" (without .zip)

== Installing or modifying ==
1. Close Sublime Text if necessary
2. Locate the data directory of Sublime Text 3 :
   * On Windows, it is located in `%APPDATA%\Sublime Text 3`
   * On Linux, it is located in `~/.config/sublime-text-3`
   * On OS X, it is located in `~/Library/Application Support/Sublime Text 3`
3. In the data directory, place the package in the `Installed Packages` directory.
4. In the data directory, delete the `Cache/OpenEdge ABL` directory
5. Restart Sublime Text
6. You may need to open each progress file type (.p, .cls, .i, .w...) and associate them with the new syntax scheme:
   * `View > Syntax > Open all with current extension as... > OpenEdge ABL`

== "Check Syntax" support
It is possible to get the "Check Syntax" feature of OpenEdge working in Sublime Text. To do so, you can use the provided `syntax.p` and `ABL.sublime-build` files :
1. Close Sublime Text
2. Place the `syntax.p` file in a directory, for example `C:\syntax`
3. Copy the file `ABL.sublime-build.example` and paste it as `ABL.sublime-build` in the data directory, in `Packages\User`
4. Modify it to reflect your configuration
5. Restart Sublime Text
6. You can now check the syntax of Progress ABL source files by hitting CTRL + B