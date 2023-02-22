# -- Graphical Interface --
# Code partially extracted from: https://github.com/rdbende/Azure-ttk-theme

import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from PIL import ImageTk, Image 

from gpt_3 import API

# This class implements all the gui and inherits from tk.Frame
class App(ttk.Frame):
	def __init__(self, root):
		ttk.Frame.__init__(self)

		self.root = root

		# Set number of rows and cols
		self.columnconfigure(index=0, weight=1)
		self.columnconfigure(index=1, weight=2)
		self.columnconfigure(index=2, weight=2)
		self.columnconfigure(index=3, weight=2)
		self.rowconfigure(index=0, weight=0)
		self.rowconfigure(index=1, weight=1)
		self.rowconfigure(index=2, weight=0)

		self.setup_widgets()


		# initialize GPT-3 API
		self.api = API()

	def setup_widgets(self):
		"""self.widgets_frame = ttk.Frame(self, padding=(0, 0, 0, 10))
		self.widgets_frame.grid(
			row=0, column=0, padx=10, pady=(30, 10), sticky="nsew", rowspan=3
		)
		self.widgets_frame.columnconfigure(index=0, weight=1)"""

		# Dasci logo at the botton
		self.frame = tk.Frame(self)
		self.frame.grid(row=0, column=0, columnspan=4, padx=0, pady=0)

		img_aspect_ration = 0.123 # height / width
		img_width = int(self.root.winfo_screenwidth()*0.8)
		img_height = int(img_width*img_aspect_ration)
		img_size = (img_width, img_height)
		self.dasci_footer = Image.open("footer_dasci.jpg")
		self.dasci_footer = self.dasci_footer.resize(img_size, Image.ANTIALIAS)
		self.dasci_footer = ImageTk.PhotoImage(self.dasci_footer)

		self.footer_label = tk.Label(self.frame, image=self.dasci_footer)
		self.footer_label.image = self.dasci_footer

		self.footer_label.grid(row=0, column=0)

		# Entry
		
		text_font = Font(family="Gotham", size=18)

		self.text_entry = tk.Text(self, font=text_font, padx=10, pady=10)
		self.text_entry.grid(row=1, column=0, columnspan=4, padx=20, pady=(10,20), sticky="nsew")
		#self.text_entry.bind('<Control_L>', self.complete_text_keybind) # Instead of pressing the button, the user can press Crtl to complete the text.
		#self.text_entry.bind('<Control_R>', self.complete_text_keybind)

		self.text_entry.bind("<Escape>", lambda e: self.text_entry.delete('1.0', 'end'))

		# Complete button
		self.button_text = tk.StringVar(value="Completar Texto")
		self.complete_button = ttk.Button(self, textvariable=self.button_text, command=self.complete_text)
		self.complete_button.grid(row=2, column=2, padx=10, pady=(0, 25))

		# Clear button (used to clear the text)

		clear_button_img = tk.PhotoImage(file = 'clear_text_icon.png')

		self.clear_button = ttk.Button(self, image=clear_button_img, command=self.clear_text)
		self.clear_button.image = clear_button_img
		self.clear_button.grid(row=2, column=0, padx=0, pady=(0, 20))

		# Language list
		self.available_languages = ["", "Español", "English"]
		self.selected_language = tk.StringVar(value=self.available_languages[1])
		self.language_list = ttk.OptionMenu(self, self.selected_language, *self.available_languages, command=self.changed_language)
		self.language_list.grid(row=2, column=1, padx=10, pady=(0, 20))

		# Create a frame to contain the scale and a text label
		self.num_sentences_frame = tk.Frame(self)
		self.num_sentences_frame.grid(row=2, column=3, padx=0, pady=(0, 25))

		self.scale_text = tk.StringVar(value="Frases (1-5)")
		self.scale_label = tk.Label(self.num_sentences_frame, textvariable=self.scale_text)
		self.scale_label.grid(row=0, column=0)

		# Sentences to output
		self.num_sentences = tk.IntVar(value=1)
		self.num_sentences_bar = ttk.Scale(self.num_sentences_frame, from_=1, to=5, variable=self.num_sentences, \
			command=self.changed_num_sentences)
		self.num_sentences_bar.grid(row=0, column=1, padx=(10,0))


	"""
	When the button is pressed, complete the text using GPT-3.
	"""
	def complete_text(self):
		curr_language = self.selected_language.get()

		# If the text is too short, don't do anything
		if len(self.text_entry.get('1.0', 'end-1c')) > 10:

			# Get number of calls to GPT-3
			num_calls = self.num_sentences.get()

			pos1 = self.text_entry.index('end-1c') # Get current end position of text 

			for i in range(num_calls):
				# Get text_entry text
				prompt = self.text_entry.get('1.0', 'end-1c')

				# Add the sentence "Responde en español." to the beginning of the prompt if the current language is Spanish
				# Now with GPT-3.5, this doesn't seem necessary
				# if curr_language == "Español":
				#	prompt = "Responde en español. " + prompt

				#print("Prompt:", prompt)
				
				# Put cursor in the end position
				self.text_entry.see("end")

				# Delete "\n" at the end of the current text in the text_entry
				while self.text_entry.get("end-1c linestart") == '\n':
					self.text_entry.delete("end-1c linestart", "end")

				# Complete it with GPT-3
				completion = self.api.complete_text(prompt, max_tokens=200, stop=".", response_lstrip="\n",
				 response_rstrip="\n", response_beginning="", response_end=".")

				# Format text
				if i == 0:
					completion = '\n\n' + completion
				else:
					completion = ' ' + completion

				if i == num_calls - 1:
					completion += '\n\n'

				# Add the text to the text_entry
				self.text_entry.insert('end', completion)

			pos2 = self.text_entry.index('end-1c')

			# Change appearance of text
			self.text_entry.tag_add("response", pos1, pos2)
			self.text_entry.tag_config("response", foreground="blue")

	"""
	Just like complete_text, but called by using a keybind.
	"""
	def complete_text_keybind(self, event):
		self.complete_text()


	"""
	Used to clear all the text of the window.
	"""
	def clear_text(self):
		self.text_entry.delete('1.0', 'end')

	"""
	Called when the user selects a language from the menu. It changes the language of the text in the app and also how the GPT-3 API is called.
	"""
	def changed_language(self, *args):
		curr_language = self.selected_language.get()

		# Change button text
		if curr_language == "Español":
			self.button_text.set("Completar Texto")
			self.scale_text.set("Frases (1-5)")

		elif curr_language == "English":
			self.button_text.set("Complete Text")
			self.scale_text.set("Sentences (1-5)")


	"""
	Called when the user uses the slider to change the number of sentences to output.
	"""
	def changed_num_sentences(self, *args):
		# Round the value, so that the slider only jumps through discrete values
		rounded_val = int(round(self.num_sentences_bar.get(), 0))

		self.num_sentences.set(rounded_val)

def main():
	root = tk.Tk()
	root.title("Generación de Textos")

	# Set theme
	root.tk.call("source", "azure.tcl")
	root.tk.call("set_theme", "light")

	app = App(root)
	app.pack(fill="both", expand=True)

	# Create the window

	root.config(width=300, height=200)

	"""root.update()
	root.minsize(root.winfo_width(), root.winfo_height())
	x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
	y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
	root.geometry("+{}+{}".format(x_cordinate, y_cordinate-20))"""

	root.mainloop()