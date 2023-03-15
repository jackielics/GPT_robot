from Dialog import GPT3
from Azure import Azure

chatbot = GPT3()
azure = Azure()
azure.prepare_synthesis()
azure.prepare_recognition()
while(True):
    print("old_prompt:"+chatbot._prompt)
    prompt = chatbot.get_input_from_console()
    # prompt = azure.recognition()
    print("Recognition_Results:"+prompt)
    response = chatbot.get_response(prompt)
    print("--Answer from robot:\t\t"+response)
    azure.synthesis(response)
    chatbot._prompt = chatbot._prompt+response