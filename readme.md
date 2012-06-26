Run in Scratch
==============
A simple plugin to run the current buffer, and output its results to another view in Sublime Text 2, instead of the console. The results view will be associated with the original buffer, so any subsequent running of Run in Scratch will output to this view. The first time it is run, a new view is created on the right in column mode (currently it assumes you are working with one view per window).


[example](https://github.com/ryecroft/RunInScratch/blob/master/example.jpg?raw=true)

Why?
----
I'm surprised not to have found something like this already out there, which leads me to think that I may be alone in my dislike of results of scripts being displayed in the console, so here are my reasons:

- Same colour scheme as the rest of the program.
- It seems more efficient to have the results to the side of the script, as the shape of monitors generally means there is more space available for another view column than there is for another view row.
- I prefer being able to detach the results view and move it to a different monitor.

Notes
-----
The command will check what syntax the current buffer is, and run a command on the command line based on this (but see note below). Currently the only syntaxes associated with any commands are:

- Ruby
- Python
- Applescript

These are all run without arguments. To add arguments or use any other interpreter, add a shebang line to the top of the file.

Before running the file, the command will cd into its base directory.