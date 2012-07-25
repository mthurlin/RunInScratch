import sublime, sublime_plugin
import commands, re
import datetime

class RunInScratchCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		line1 = self.view.substr(self.view.line(0))
		syntax = self.view.settings().get('syntax')
		execute_string = self.get_execute_string(syntax, line1)
		current_file = self.view.file_name()
		self.current_file = current_file
		# self.view.settings().set('parent_file')
		
		window = sublime.active_window()

		if current_file == None:
			current_file = "None" + line1
			file_name = self.view.substr(sublime.Region(0,self.view.size()))
			tab_name = "untitled"
			execute_string += self.get_execute_arg(syntax, line1)
			file_directory = ""
		else:
			file_name = current_file.split("/")[-1]
			tab_name = file_name
			window.run_command("save")
			file_directory = "/".join( current_file.split("/")[0:-1] )

		self.tab_name = tab_name
		self.file_name = file_name
		self.window = window
		
		cmd = "cd '%s'" % (file_directory) + "\n" + execute_string + " '%s'" % (file_name)
		
		output = commands.getoutput(cmd).decode('utf-8')

		if re.search("Ruby", str(syntax)):

			header = execute_string.split('\n')[0] + ' -e ' + '\'puts "Ruby #{RUBY_VERSION} #{RUBY_PLATFORM} #{RUBY_RELEASE_DATE}\n\n"\''	
			line1 = commands.getoutput(header).decode('utf-8')	
			output = '\n'.join([line1,output])

		view = self.get_results_window()

		edit = view.begin_edit()
		view.replace(edit, sublime.Region(0, view.size()), output)
		view.sel().clear()
		view.end_edit(edit)
		
	def get_execute_arg(self, syntax, line1):
		return {
			'applescript':' -e',
			'python':' -c',
			'ruby':' -e'
		}[syntax]
		
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
		view.set_syntax_file('/Users/fatboy/Library/Application Support/Sublime Text 2/Packages/RunInScratch/run_in_scratch.tmlanguage')
		view.settings().set('parent_file', self.current_file)
		view.settings().set('word_wrap', True)
		window.run_command("set_layout",
		      {
		          "cols": [0.0, 0.65, 1.0],
		          "rows": [0.0, 1.0],
		          "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]
		      })
		
		
		
		view.set_name('Results of %s' % (self.tab_name))
		view.settings().set("RunInScratch", True)
		
		
		window.run_command("move_to_group", {"group": 1})
		window.run_command("focus_group", {"group": 0})
		view.set_scratch(True)
		
		return view
		
		
class GoToLineListener(sublime_plugin.EventListener):

	def get_parent_view(self, file_name):
		for window in sublime.windows():
			for view in window.views():
				name = view.file_name()
				match = re.search(file_name, str(name))
				if match:
					return view

	def on_selection_modified(self, view):
		if view.settings().get("RunInScratch") == True:
			text = view.substr(view.line(view.sel()[0]))
			match = re.search(r'^.+ from (.+\.rb):(\d+):in', text)
			if match:
				parent_view = self.get_parent_view(match.group(1))
				parent_view.sel().clear()
				parent_view.run_command("goto_line", {"line":int(match.group(2))})
				parent_view.sel().add(parent_view.line(parent_view.sel()[0]))


				