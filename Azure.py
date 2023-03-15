import azure.cognitiveservices.speech as speechsdk
import threading
import queue
from functools import partial


class Azure():
    def __init__(self) -> None:
        '''
        initialize parameters BASICALLY
        '''
        self.api_key = ""
        self.service_region = "eastus"
        self.speech_config = speechsdk.SpeechConfig(subscription=self.api_key,region=self.service_region)

    def prepare_synthesis(self):
        '''
        define voice type etc
        '''
        self.speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoNeural" 
        # self.speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
        # self.speech_config.speech_synthesis_voice_name = "en-US-JennyMultilingualNeural"
        # self.speech_config.
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config)

    def synthesis(self,sentence):
        '''
        speak words(str or list) out
        '''
        if(type(sentence)==list):
            idx = 0
            for sent in sentence:
                idx += 1
                self.speech_synthesizer.speak_text_async(sent).get()
        elif(type(sentence)==str):
                self.speech_synthesizer.speak_text_async(sentence).get()
    

    def synthesis_ssml(self,text:str):
        '''
        Try synthesis speak_ssml_async which can design voice in many aspects
        '''
        # ssml_string = open("ssml.xml", "r", encoding="utf-8").read()
        ssml_string = f'''
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
       xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="zh-CN">
    <voice name="zh-CN-XiaoxiaoNeural">
        <mstts:express-as style="affectionate">
            {text}
        </mstts:express-as>
    </voice>
</speak>
        '''
        self.speech_synthesizer.speak_ssml_async(ssml_string).get()

    def systhesis_over(self):
        print("Systhesis Over!")

    def prepare_recognition(self):
        '''
        Only English will be recognized and spoken in English mode 
        therefor Non-English mode is recommended
        '''
        self.speech_config.speech_recognition_language="zh-CN" # en-US or zh-CN
        
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config) # , audio_config=audio_input

    def recognition(self)->str:
        '''
        get result of recognition
        '''
        print("Speak into your microphone.")
        speech_recognition_result = self.speech_recognizer.recognize_once_async().get()
        # print(speech_recognition_result.text)
        return speech_recognition_result.text


    def exc_queue(self,q:queue):
        while True:
            item = q.get()
            item() # process the item
            q.task_done()
            if item is self.systhesis_over:
                break 
            

    def start_queue_thread(self):
        '''
        start queue and thread for synthesize
        '''
        self.que = queue.Queue()
        self.thr = threading.Thread(target=self.exc_queue, args=(self.que,))
        self.thr.start()

    def put2queue(self,clause:str):
        '''
        add CLAUSE to queue for synthesizing.
        systhesis_over() cann't be passed thay way.
        '''
        paraFunc = partial(self.synthesis, clause,)
        # paraFunc = partial(self.synthesis_ssml, clause,)
        self.que.put(paraFunc)

    def end_queue(self):
        '''give an ending to queue'''
        self.que.put(self.systhesis_over)


if __name__ == '__main__':
    azure = Azure()
    azure.prepare_synthesis()
    # azure.test_synthesis_ssml()
    sent_list=['花间一壶酒，独酌无相亲。',
        '举杯邀明月，对影成三人。',
        '月既不解饮，影徒随我身。'
        ]
    azure.start_queue_thread()
    for sent in sent_list:
        azure.put2queue(sent)

    # azure.put2queue(azure.systhesis_over)
    azure.end_queue()
    azure.que.join()
    print(azure.que.empty())



    # azure.prepare_recognition()
    # azure.recognition()