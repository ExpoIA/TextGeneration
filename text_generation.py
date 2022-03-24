import openai

# Functions
def complete_text(text, temperature=0.0, engine="text-davinci-001"):
	response = openai.Completion.create(
	        engine=engine,
	        prompt=text,
	        temperature=temperature)

	return response.choices[0].text.lstrip("\n ")

# Import private key
with open('openai_private_key.priv') as f:
	openai.api_key = f.read()

# Complete the user's prompts until it says "EXIT"

print("----------- text_generation_demo_v1 -----------")
print("Esta demo utiliza GPT-3 para completar el texto introducido por el usuario.")
print("En caso de querer salir del programa, escribe 'EXIT'")

end = False

while not end:
	user_prompt = input("<User>: ")

	if user_prompt.upper() == "EXIT":
		end = True
	else:
		openai_response = complete_text(user_prompt)

		print("<GPT-3>:", openai_response)
