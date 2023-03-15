# diy library 
from Crawler_chatGPT import Crawler_chatGPT
from Azure import Azure
# STL
import traceback


crawler = Crawler_chatGPT()
# crawler.load_new_page()
crawler.load_old_page()
crawler.new_chat()


azure = Azure()
azure.prepare_synthesis()
azure.prepare_recognition()

while(True):
    # update msg from User
    # msg = azure.recognition()
    msg = input("Type in : \t")
    print("Recognition_Results:\t"+msg)
    crawler.sendMsg(msg)

    azure.start_queue_thread()

    # q = queue.Queue()
    # thread = threading.Thread(target=azure.exc_queue, args=(q,))
    # thread.start()

    while True:
        # update msg from chatGPT
            try:
                # time.sleep(0.1) # According to your own needs for display synchronization
                msg = crawler.recvMsg()
                
                while True:
                    # get the value of clauses and synthesize them
                    clause = crawler.punctuate(msg)
                    if(clause==""): # didn't get new clause
                        break
                    else:
                        print("="*40)
                        print(clause)
                        ''' 
                        synthesis mustn't take much time here otherwise 
                        ending will come earlier than it should,
                        so starting new thread is necessary.
                        English reply comes much quicker than other language,
                        therefor there is such a huge speed difference between synthesis() and print() for non-English such as Chinese 
                        that u must wait for a long time until synthesis is over
                        '''
                        azure.put2queue(clause)
                        # paraFunc = partial(azure.synthesis, clause,)
                        # q.put(paraFunc)


                        # azure.synthesis(clause)
                        print("*"*40)
                        crawler.start = crawler.end

                if crawler.isFinished():
                    # may end prematurely if synthesis took too much time
                    
                    azure.end_queue() # add None to stop the worker
                    azure.que.join()
                    break # start another dialog
            except Exception as e:
                traceback.print_exc()
                print("..",end="")
                pass