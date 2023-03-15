import os
import openai

# import openai

# completion = openai.ChatCompletion.create(
#   model="gpt-3.5-turbo", 
#   messages=[{"role": "user", "content": "Tell the world about the ChatGPT API in the style of a pirate."}]
# )

# print(completion)

class GPT3:
    def __init__(self) -> None:
        '''
        initialize chatmodel parameters
        '''
        self._api_key = ""
        self._model = "text-davinci-003"
        self._temperature=0
        self._max_tokens=500
        self._top_p=1
        self._frequency_penalty=0.0
        self._presence_penalty=0.0
        self._prompt = ""

    def get_input_from_console(self):
        s_input = input("--Shut down VPN and Say sth:\t")
        return s_input
        # self._prompt = old_dialog+"\nQ:"+s_input+"\nA:"

    def get_response(self,prompt)->str:
        openai.api_key = self._api_key
        self._prompt +="\nQ:"+prompt+"\nA:"
        self._response_json = openai.Completion.create(
            model=self._model,
            prompt=self._prompt,
            temperature=self._temperature,
            max_tokens=self._max_tokens,
            top_p=self._top_p,
            frequency_penalty=self._frequency_penalty,
            presence_penalty=self._presence_penalty #,
            # stop=["\n"]
            )
        return self._response_json["choices"][0]["text"]

if __name__ == '__main__':
    chatbot = GPT3()
    while(True):
        print("old_prompt:"+chatbot._prompt)
        prompt = chatbot.get_input_from_console()
        response = chatbot.get_response(prompt)
        chatbot._prompt = chatbot._prompt+response
        print("--Answer from robot:\t\t"+response)