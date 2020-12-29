__doc__ = '''模板AI函数

（必要）play函数

（可选）load，summary函数

（多局比赛中可选）init，summaryall函数

详见AI_Template.pdf
'''


def play(stat, storage):
    size = stat['size']
    my_id = stat['now']['me']['id']
    my_direction = stat['now']['me']['direction']
    your_direction = stat['now']['enemy']['direction']
    my_x = stat['now']['me']['x']
    my_y = stat['now']['me']['y']
    your_x = stat['now']['enemy']['x']
    your_y = stat['now']['enemy']['y']
    my_fields = stat['now']['fields']
    turnleft = stat['now']['turnleft'][my_id-1]
    my_bands = stat['now']['bands']

    square = storage['core']
    return square.goAhead(10,size,my_fields,my_id,my_direction,my_x,my_y) 

    
    
        
    


def load(stat, storage):
    '''
    初始化函数，向storage中声明必要的初始参数
    若该函数未声明将不执行
    该函数超时或报错将判负
    
    params:
        stat - 游戏数据
        storage - 游戏存储
    '''
    '''
        my_id = stat['now']['me']['id']
        my_x = stat['now']['me']['x']
        my_y = stat['now']['me']['y']
        your_x = stat['now']['enemy']['x']
        your_y = stat['now']['enemy']['y']
        turnleft = stat['now']['turnleft'][myid-1]

        fields = stat['now']['fields']
        bands = stat['now']['bands']
    '''
    size = stat['size']
    my_id = stat['now']['me']['id']
    your_id = stat['now']['enemy']['id']
    WIDTH = size(0)
    HEIGHT = size(1)

    def bandsPoint(bands,myid,size):
        bandslist = []
        for i in range(size[0]):
            for j in range(size[1]):
                if bands[i][j] == myid:
                    bandslist.append((i,j))
        return bandslist

    storage['bandsList'] = bandsPoint

    def edge(size,fields,my_id):                           #找到边界点，加入边界列表
        edgelist = []
        for i in range(1,size[0]-1):
            for j in range(1,size[1]-1):
                if fields[i][j] == my_id:
                    if fields[i][j-1] != my_id or fields[i][j+1] != my_id:        #两侧的地盘一边不为我的，一边是我的，就可以认为是边界
                        edgelist.append((i,j))
        for j in range(1, size[1] - 1):
            for i in range(1, size[0] - 1): 
                if fields[i][j] == my_id:
                    if fields[i-1][j] != my_id or fields[i+1][j] != my_id:
                        edgelist.append((i, j))
        return edgelist
    storage['edgeList'] = edge

    def turnDir(size,my_fields,my_id,my_direction,my_x,my_y):
        temp_list = edge(size,my_fields,my_id)        #边界点赋值
        y_list = []
        x_list = []
        for i in range(len(temp_list)):      #取出x或者y寻找最大的
            y_list.append(temp_list[i][1])
            x_list.append(temp_list[i][0])
            max_y = abs(max(y_list) - my_y)
            min_y = abs(min(y_list) - my_y)
            max_x = abs(max(x_list) - my_x)
            min_x = abs(min(x_list) - my_x)
        if my_direction ==0:
            if max_y>min_y:
                return 'R'
            else:
                return 'L'
        elif my_direction ==2:
            if max_y>min_y:
                return 'L'
            else:
                return 'R'
        elif my_direction ==1:
            if max_x>min_x:
                return 'L'
            else:
                return 'R'
        else:
            if max_x>min_x:
                return 'R'
            else:
                return 'L'
    class square():
        def __init__(self):
            self.lenth = 0
            self.direc = 'U'
        def clear(self):
            self.lenth=0
            self.direc = 'U'
        def goAhead(self,walk_lenth,size,my_fields,my_id,my_direction,my_x,my_y):
            '''
            walk_lenth：要前进的距离
            '''
            
            if walk_lenth>0:
                self.lenth-=self.lenth
                return 'U'
            elif walk_lenth == 0:                
                #此处写入判断旋转方向的函数
                storage['turn'] = turnDir(size,my_fields,my_id,my_direction,my_x,my_y)
                #此处写入要前进的距离（到领地的最小的距离）的函数
                self.lenth = walk_lenth
                return storage['turn']
            else:
                print('error')
    storage['core'] =  square()            

                       
    def howToImitate(my_pos,next_pos):
        flag = (my_pos-next_pos)
        if flag == 3 or flag == -1 :
            return 'R'
        elif flag == 0:
            return 'U'
        elif flag == -3 or flag ==1 :
            return 'L'
        else:
            print("cant go")
            return '1'
    storage['Imitation'] = howToImitate

def summary(match_result, stat, storage):
    '''
    一局对局总结函数
    若该函数未声明将不执行
    该函数报错将跳过

    params:
        match_result - 对局结果
        stat - 游戏数据
        storage - 游戏存储
    '''
    pass

def init(storage):
    '''
    多轮对决中全局初始化函数，向storage中声明必要的初始参数
    若该函数未声明将不执行
    该函数报错将跳过
    
    params:
        storage - 游戏存储
    '''
    pass

def summaryall(storage):
    '''
    多轮对决中整体总结函数
    若该函数未声明将不执行
    该函数报错将跳过

    params:
        storage - 游戏存储
    '''
    pass