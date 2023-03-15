import time
end = -1
start = 0 # beginning of next string
source = '''
小说。
剧本。
戏剧。
音乐剧。
1。
2。
3。
4。
5。
6。
7。
8。
9。
'''
marks = ['，','。'] # ending of a clause such as '.','?','!' is recommended

idx_clause = 0

def get_end(marks:list,msg:str)->int:
    end_list = []
    for mark in marks:
        tmp = msg.find(mark,start)
        if tmp != -1:
            end_list.append(tmp)

    if end_list==[]:
        return -1
    else:
        return min(end_list)


def punctuate(msg:str):
    '''
    update START only when msg get delimiter successfully last time 
    '''
    global end
    global start
    if end != -1: 
        # update START only when msg get delimiter successfully last time 
        start = end+1
    # end = msg.find(delimiter,start)
    end = get_end(marks,msg)
    if end == -1: # didn't find delimiter
        return ""
    else :
        return msg[start:end+1]
    print(msg[start:end+1])
    print("---------------------")

def get_clause(msg:str):
    global start
    while True:
        res = punctuate(msg)
        if(res==""): # didn't get new clause
            break
        else:
            print("="*40)
            print(res)
            start = end

def split_clause(msg:str):
    '''
    Simpler writing, slower efficiency
    '''
    msg = msg.split('。')
    global idx_clause
    print(idx_clause)
    print(msg)
    print(len(msg))
    # if 
    for sent in msg[idx_clause:]:
        print(sent)
    idx_clause += 1

for i in range(200):
    time.sleep(0.3)
    msg = source[:i]
    get_clause(msg)
    # split_clause(msg)
    # while True:
    #     res = punctuate(msg)
    #     if(res==""): # didn't get new clause 
    #         break
    #     else:
    #         print(res)
    #         # print(f"start:\t{start}end:{end}")
    #         start = end
