import os
import sublime, sublime_plugin

class HtmlToSlimFromFileCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		source = self.view.file_name()
		if source.endswith(".erb"):
			target = source.replace('.erb', '.slim')
		if source.endswith(".html"):
			target = source + '.slim'
		if target:
			Slim.convert(source, target)
			self.view.window().open_file(target)

	def is_enabled(self):
		return True #return (self.view.file_name().endswith(".html") or self.view.file_name().endswith(".erb"))

class HtmlToSlimFromSelectionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			if not region.empty():
				html = self.view.substr(region)
				slim = Slim.buffer(html)
				if slim != None:
					self.view.replace(edit, region, slim)

	def is_enabled(self):
		return True #return self.view.file_name().endswith(".slim")

class HtmlToSlimFromClipboardCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		html = sublime.get_clipboard()
		slim = Slim.buffer(html)
		if slim != None:
			for region in self.view.sel():
				self.view.replace(edit, region, slim)

	def is_enabled(self):
		return True #return self.view.file_name().endswith(".slim")

class Slim:
	@classmethod
	def convert(self, html_file, slim_file):
		cmd = ' '.join(['/usr/local/bin/rbenv', 'exec', 'erb2slim', html_file, slim_file])
		from subprocess import call
		call(cmd, shell=True)
		return True

	def buffer(self, html):
		html_file = "/tmp/_sublime_buffer.html"
		slim_file = html_file + ".slim"

		with open(html_file, "w") as tmp_file:
		  tmp_file.write(html)  

		slim = open(slim_file, 'r').read()

		os.remove(html_file)
		os.remove(slim_file)

		return slim