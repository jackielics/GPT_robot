from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import lxml.html
from selenium.webdriver.common.by import By
import undetected_chromedriver.v2 as uc

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Crawler_chatGPT():
    '''
    Enter the command before starting:
    chrome.exe --remote-debugging-port=9527 --user-data-dir="D:\Codes\crawler"
    '''
    def __init__(self):
        ''''''
        # self.options = Options()
        # self.options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
        # self.browser = webdriver.Chrome(options=self.options) # = connected to Browser synchronously
        # self.browser = uc.Chrome()
        # self.browser.get('https://chat.openai.com/')
        
        self.cnt_cliMsg,self.cnt_serMsg = 0,0

        self.xpath_button_Regenerate_response = '//*[@id="__next"]/div/div[1]/main/div[2]/form/div/div[1]/button'
        # sometimes button_Regenerate_response won't show up

        self.xpath_inputbox = '//textarea'
        # speacial xpath of svg
        self.xpath_svg_send = '//*[@id="__next"]/div/div[1]/main/div[2]/form/div/div[2]/button//*[name()="svg"]'
        
        self.marks = self.marks_trans([',','.','!','?',':'])

        # try:
        #     WebDriverWait(self.browser, 60).until(EC.presence_of_element_located((By.XPATH, self.xpath_inputbox)))
        # except Exception as _:
        #     print('网页加载太慢，不想等了。')

    def load_new_page(self):
        '''log in 60s'''
        self.browser = uc.Chrome()
        self.browser.get('https://chat.openai.com/')
        try:
            WebDriverWait(self.browser, 60).until(EC.presence_of_element_located((By.LINK_TEXT, "New chat")))
        except Exception as _:
            print('logging in too slow!')
        # time.sleep(30)

    def load_old_page(self):
        self.options = Options()
        self.options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
        self.browser = webdriver.Chrome(options=self.options) # = connected to Browser synchronously
        pass

    def new_chat(self):
        '''click 'New Chat' button'''
        self.cnt_cliMsg,self.xpath_serMsg = 0,0
        self.browser.find_element(By.LINK_TEXT, "New chat").click()
       
    def marks_trans(self,marks:list)->list:
        new_marks = marks.copy()
        for mark in marks:
            if mark == '.':
                new_marks.append('。')
            elif mark == ',':
                new_marks.append('，')
            elif mark == '!':
                new_marks.append('！')
            elif mark == '?':
                new_marks.append('？')
            elif mark == ':':
                new_marks.append('：')
        return new_marks
        

    def update_xpath_cliMsg(self):
        '''
        Get Xpath of user's message which cen be read from input
        Maybe useless for NOW.
        '''
        self.cnt_cliMsg += 1
        self.xpath_cliMsg = f'//*[@id="__next"]/div/div[1]/main/div[1]/div/div/div/div[{str(2*self.cnt_cliMsg-1)}]/div/div[2]/div[1]'

    def update_xpath_serMsg(self):
        self.cnt_serMsg += 1
        self.xpath_serMsg = f'//*[@id="__next"]/div/div[1]/main/div[1]/div/div/div/div[{str(2*self.cnt_serMsg)}]/div/div[2]/div[1]/div/div'
                            # //*[@id="__next"]/div/div[1]/main/div[1]/div/div/div/div[2]/div/div[2]/div[1]/div/div
                            # //*[@id="__next"]/div/div[1]/main/div[1]/div/div/div/div[2]/div/div[2]/div[2]/button[1]
                            # //*[@id="__next"]/div/div[1]/main/div[1]/div/div/div/div[4]/div/div[2]/div[2]/button[1]
                            # 
    def recvMsg(self)->str:
        '''receive message from server'''
        self.source = self.browser.page_source
        self.selector = lxml.html.fromstring(self.source)
        msg_block  = self.selector.xpath(self.xpath_serMsg)[0] # /p/text()
        self.msg  = msg_block.xpath('string(.)')
        return self.msg

    
    def sendMsg(self,msg:str):
        self.update_xpath_serMsg() # prepare for receiving message from chatGPT
        time.sleep(2)
        self.browser.find_element(By.XPATH, self.xpath_inputbox).send_keys(msg)
        self.browser.find_element(By.XPATH, self.xpath_svg_send).click()
        # prepare for upcoming reply
        self.end = -1
        self.start = 0 # beginning of next string
        
    def isFinished(self)->bool:
        '''check if the answers from chatGPT ended by searching button_Regenerate_response '''
        svg_send = self.browser.find_elements(By.XPATH,self.xpath_svg_send)# [] if none
            # //*[@id="__next"]/div/div[1]/main/div[1]/div/div/div/div[2]/div/div[2]/div[2]/button[1]
        if svg_send == []: # not finished if svg_send didn't show up 
            return False
        else:
            return True
    
    def get_end(self,msg:str)->int:
        '''
        get the index where the clause ends from a list of delimiters.
        get the smallest end index except -1.
        '''
        end_list = []
        for mark in self.marks:
            tmp = msg.find(mark,self.start)
            if tmp != -1:
                end_list.append(tmp)
        
        if end_list==[]:
            return -1
        else:
            return min(end_list)


    def punctuate(self,msg:str):
        '''
        update START only when msg get delimiter successfully last time
        '''
        if self.end != -1:
            # update START only when msg get delimiter successfully last time
            self.start = self.end+1
        # self.end = msg.find(self.marks[0],self.start)

        self.end = self.get_end(msg)
        if self.end == -1: # didn't find delimiter
            return ""
        else :
            return msg[self.start:self.end+1]
        print(msg[start:end+1])
        print("---------------------")

    def print_clause(self,msg:str):
        '''
        A efficient and sophisticated algorithm with 2 paras.
        Maybe string.split() can make things easier but simpler writing, slower efficiency.
        '''
        while True:
            # update clauses of msg
            res = self.punctuate(msg)
            if(res==""): # didn't get new clause
                break
            else:
                print("="*40)
                print(res)
                print("="*40)
                self.start = self.end
    
    # def get_clause(self,msg:str)->str:
    #     # update clauses of msg
    #     self.marks = ['.','!','?']+['。','！','？']
    #     res = self.punctuate(msg)
    #     if(res==""): # didn't get new clause
    #         break
    #     else:
    #         print("="*40)
    #         print(res)
    #         print("="*40)
    #         self.start = self.end

# '//*[@id="__next"]/div/div[1]/main/div[2]/form/div/div[2]/textarea'

if __name__ == '__main__':
    crawler = Crawler_chatGPT()
    crawler.load_new_page()
    # crawler.new_chat()
    # msg = ""
    idx = 0 # index of to-be-spoken
    while True:
        msg = input("INPUT:")
        crawler.sendMsg(msg)
        while True:
            try:
                time.sleep(0.5) # According to your own needs for display synchronization
                msg = crawler.recvMsg()
                # crawler.print_clause(msg) # simply print clauses in a method
                
                # get the value of clauses in __main__()
                while True:
                    res = crawler.punctuate(msg)
                    if(res==""): # didn't get new clause
                        break
                    else:
                        print("="*40)
                        print(res)
                        print("="*40)
                        
                        crawler.start = crawler.end

                if crawler.isFinished():
                    break
            except:
                # print("...")
                pass
