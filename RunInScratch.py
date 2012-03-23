import sublime, sublime_plugin
import commands, re

class RunInScratchCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		current_file = self.view.file_name()
		line1 = self.view.substr(self.view.line(0))
		self.current_file = current_file
		file_name = current_file.split("/")[-1]
		self.file_name = file_name
		window = sublime.active_window()
		self.window = window
		
		window.run_command("save")
		
		syntax = self.view.settings().get('syntax')
		
		file_directory = "/".join( current_file.split("/")[0:-1] )
		
		execute_string = self.get_execute_string(syntax, line1)
		
		cmd = "cd '%s'" % (file_directory) + "\n" + execute_string + " '%s'" % (file_name)
		output = commands.getoutput(cmd)

		view = self.get_results_window()

		edit = view.begin_edit()
		view.replace(edit, sublime.Region(0, view.size()), output)
		view.sel().clear()
		view.end_edit(edit)
		
	def get_execute_string(self, syntax, line1):
		if re.match("#!", line1):
			return line1.replace("#!", "")
			
		syntax = syntax.split("/")[-1].split(".")[0].lower()
		return {
			'applescript':'osascript',
			'python':'python',
			'ruby':'ruby'
		}[syntax]
		
	def get_results_window(self):
		for window in sublime.windows():
			for view in window.views():
				if view.settings().get('parent_file') == self.current_file:
					return view
				
		window = sublime.active_window()
		view = window.new_file()
		view.settings().set('parent_file', self.current_file)
		window.run_command("set_layout",
		      {
		          "cols": [0.0, 0.65, 1.0],
		          "rows": [0.0, 1.0],
		          "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]
		      })
		
		window.run_command("move_to_group", {"group": 1})
		window.run_command("focus_group", {"group": 0})
		
		view.set_name('Results of %s' % (self.file_name))
		view.set_scratch(True)
		
		return view