import sublime, sublime_plugin, os, subprocess

class MarsDiffCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		regions = []
		for num in self.get_changed_lines():
			num = int(num)
			if num > 1: #actually exists
				linePoint = self.view.line(self.view.text_point(num - 1, 0))
			regions.append(linePoint)
		self.view.add_regions('highlightText', regions, 'keyword', 'dot', sublime.DRAW_OUTLINED)
		


	def get_changed_lines(self):
		if self.view.file_name() is not None:
			#print(self.view.file_name())
			args = [
				'mars-diff',
				'--lines',
				self.view.file_name()
			]
			output = self.run_cmd(args)
			#print(output)
			return output.strip().split(' ')
		else:
			return [0]


	def run_cmd(self, args):
		startupinfo = None
		if os.name == 'nt':
			startupinfo = subprocess.STARTUPINFO()
			startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
		proc = subprocess.Popen(args, stdout=subprocess.PIPE,
			startupinfo=startupinfo, stderr=subprocess.PIPE)
		return proc.stdout.read()