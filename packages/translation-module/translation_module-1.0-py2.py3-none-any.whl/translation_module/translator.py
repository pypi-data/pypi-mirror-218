import openai

openai.api_key = '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'

def translate_text(input_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that creates kids short stories."},
            {"role": "user", "content": input_text},
        ],
        temperature=1,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    translated_text = response.choices[0].message.content
    return translated_text

def translate_file(input_file, output_file):
    with open(input_file, 'r') as file:
        english_text = file.read()
    arabic_translation = translate_text(english_text)
    with open(output_file, 'w') as file:
        file.write(arabic_translation)
