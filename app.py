import ollama

print("=== AI CHATBOT ===")
print("Ketik 'exit' untuk keluar\n")

while True:
    user_input = input("Kamu: ")

    if user_input.lower() == "exit":
        print("Program selesai")
        break

    response = ollama.chat(
        model='llama3',
        messages=[
            {
                'role': 'user',
                'content': user_input
            }
        ]
    )

    print("\nAI:")
    print(response['message']['content'])
    print()
