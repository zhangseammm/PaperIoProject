'''
Group Name: 
        Eclosure King
Members:
        张洋铭  19309189
        刘星云  19309095
        刘佳慧  19309091
        张宁    19309183
        唐苛耕  19309129
'''

def play(stat, storage):
    
    size = stat['size']
    my_id = stat['now']['me']['id']
    your_id = stat['now']['enemy']['id']
    my_direction = stat['now']['me']['direction']
    
    my_x = stat['now']['me']['x']
    my_y = stat['now']['me']['y']

    your_x = stat['now']['enemy']['x']
    your_y = stat['now']['enemy']['y']
    
    fields = stat['now']['fields']
    bands = stat['now']['bands']    #根据返回值判断是敌人的还是我的领地

    #turnleft = stat['now']['turnleft'][my_id - 1]
    storage['my_fields_status'] = 1 #表示我现在在filed里面
    square = storage['core']
    #print(size[0])
    #这句话放入寻找步长的函数，现在这个mylength只是根据回合数逐渐增加前进步数
    #mylength = int(50000 / int(turnleft))
    kill =storage['kill']
    
    avoidBoundaryAndBands = storage['avoidBoundaryAndBands'] 
    #getNearestDistanceToEnermy = storage['getNearestDistanceToEnermy']
    whetherhit = avoidBoundaryAndBands(size, fields, bands, my_id, my_direction, my_x, my_y)
    getNearestDistancetolaststep = storage['getNearestDistancetolaststep']
    #getNearestDistanceToBands=storage['getNearestDistanceToBands']
    '''
    print('ho')
    lenth,[],[] = getNearestDistanceToBands(your_x,your_y,bands,my_id)
    print(lenth)
    print('ho2')
    '''
    
    whetherKill = kill.killIt(my_id,your_id,my_x,my_y,my_direction,your_x,your_y,fields,bands,size)
    YtoMBands = storage['YtoMBands'] 
    dis,nouse1,nouse2 = YtoMBands(your_x,your_y,fields,bands,size,my_id)
    if dis>30:
        dis = 15
    #print(storage['mode'])
    if whetherhit == None:
        if whetherKill ==None:
            if storage['mode']=='main':
                
                return square.goAhead(dis, size, fields, bands, my_id, my_direction, my_x, my_y,your_id)
        else:
            
            return whetherKill    
    else:
        storage['length'] = getNearestDistancetolaststep(my_x,my_y,fields,my_direction,my_id,size,1)
        storage['count'] = -10
        return whetherhit

    #mylength是行走步数
def load(stat, storage):
    aggressive = 0#取值0到5
    defensive = 3#取值3到5d
    storage['mode']='main'
    #directions = ((1, 0), (0, 1), (-1, 0), (0, -1))
    size = stat['size']
    storage['my_fields_area'] = 9
    #my_id = stat['now']['me']['id']
    #your_id = stat['now']['enemy']['id']
    temp_point={}
    temp_point['x']=0
    temp_point['y']=0
    my_point={}
    my_point['x']=0
    my_point['y']=0
    WIDTH = size[0]
    HEIGHT = size[1]

    # 查找纸带的区域，返回己方已经占有区域，一个list(tuple)
    def aheadField(fields,my_x,my_y,my_direction,my_id,size):
        if my_direction ==0:
            for i in range(my_x+1,WIDTH):
                if fields[i][my_y]==my_id:
                    return 1
        elif my_direction==2:
            for i in range(my_x):
                if fields[i][my_y]==my_id:
                    return 1
        elif my_direction==1:
            for i in range(my_y+1,HEIGHT):
                if fields[my_x][i]==my_id:
                    return 1
        elif my_direction==3:
            for i in range(my_y):
                if fields[my_x][i]==my_id:
                    return 1
        return 0
    
    # 区域点集
    def bandsPoint(bands, id, size):

        '''
        如果传入是id=my_id那么就是我的，id = your_id那么就是敌人的bands
        '''
        bandslist = []
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if bands[i][j] == id:
                    bandslist.append((i, j))
        return bandslist

    #头到大本营的最短距离
    def getNearstDistanceToFields(my_x, my_y, fields, bands, id):  # id/x/y/可以调节
        if fields[my_x][my_y] == id:
            print(my_x, my_y)
            return -1, my_x, my_y

        min_distancetofields = 10000
        my_fields = fieldsPoint(fields, id, size)
        my_bands = bandsPoint(bands, id, size)

        x_bands = []
        y_bands = []
        for i in range(len(my_bands)):
            x_bands.append(my_bands[i][0])
            y_bands.append(my_bands[i][1])
        j = 2

        if(list(set(x_bands) & set(range(0, 110))) == my_x):
            j = 1
        if(list(set(y_bands) & set(range(0, 110))) == my_y):
            j = 0
        for i in range(len(my_fields)):
            if(j == 1):
                if(my_fields[i][1] != my_y):
                    distance1 = abs(my_fields[i][0]-my_x) + \
                        abs(my_fields[i][1]-my_y)
                    if (distance1 < min_distancetofields):
                        min_distancetofields = distance1  # 如果头部在大本营内部，最终返回距离值为0
                        nearest_x = my_fields[i][0]
                        nearest_y = my_fields[i][1]
            if(j == 0):
                if(my_fields[i][0] != my_x):
                    distance1 = abs(
                        my_fields[i][0] - my_x) + abs(my_fields[i][1] - my_y)
                    if (distance1 < min_distancetofields):
                        min_distancetofields = distance1  # 如果头部在大本营内部，最终返回距离值为0
                        nearest_x = my_fields[i][0]
                        nearest_y = my_fields[i][1]
            else:
                distance1 = abs(my_fields[i][0] - my_x) + \
                    abs(my_fields[i][1] - my_y)
                if (distance1 < min_distancetofields):
                    min_distancetofields = distance1  # 如果头部在大本营内部，最终返回距离值为0
                    nearest_x = my_fields[i][0]
                    nearest_y = my_fields[i][1]

            return min_distancetofields, nearest_x, nearest_y  # 返回的是tuplel类型

    #头到敌方纸带的最短距离
    def getNearestDistanceToBands(my_x,my_y,bands,id):#id/x/y/可以调节
        min_distancetobands=10000
        your_bands = bandsPoint(bands, id, size)
        if(your_bands==[]):
            return 1000,0,0
        for i in range(len(your_bands)):
            distance2=abs(your_bands[i][0]-my_x)+abs(your_bands[i][1]-my_y)
            if (distance2 < min_distancetobands):
                min_distancetobands=distance2
                nearest_x=your_bands[i][0]
                nearest_y=your_bands[i][1]
        return min_distancetobands,nearest_x,nearest_y                   #返回的是tuple类型
    storage['getNearestDistanceToBands'] = getNearestDistanceToBands
   
    def fieldsPoint(fields, id, size):
            '''
            如果传入是id=my_id那么就是我的fields，id = your_id那么就是敌人的fields
            '''
            fieldslist = []
            for i in range(WIDTH):
                for j in range(HEIGHT):
                    if fields[i][j] == id:
                        fieldslist.append((i, j))
            return fieldslist

    #到达回到大本营的最后一步的最小/大距离
    def getNearestDistancetolaststep(my_x,my_y,fields,my_direction,my_id,size,my_cho):
        '''
        my_cho=0 min
        my_cho=1 max
        '''

        my_fields = fieldsPoint(fields, my_id, size)
        dstList=[]                                      #建立一个空数组
        for i in range (len(my_fields)):                 #访问fields中的所有坐标
            if my_direction==1 or my_direction==3:       #如果当前方向为东西方向
                dst=abs(my_x-my_fields[i][0])
                
                dstList.append(dst)                          #将所有的距离值存入数组中
            else:
                dst=abs(my_y-my_fields[i][1])
                dstList.append(dst)                          #将所有的距离值存入数组中
        if my_cho==0:   
            my_distancetolaststep=min(dstList)               #m的最小值
        else:
            my_distancetolaststep=max(dstList)               #m的最大值


        return my_distancetolaststep-1  
    storage['getNearestDistancetolaststep'] =getNearestDistancetolaststep
    
    def getNearestDistancetolastPoint(my_x,my_y,fields,my_direction,my_id,size):
        '''
        my_cho=0 min
        my_cho=1 max
        '''

        my_fields = fieldsPoint(fields, my_id, size)
        dstList=[]
                                              #建立一个空数组
        for i in range (len(my_fields)):                 #访问fields中的所有坐标
            if my_direction==1 or my_direction==3:       #如果当前方向为东西方向
                dst=abs(my_x-my_fields[i][0])
                
                dstList.append(dst)                          #将所有的距离值存入数组中
            else:
                dst=abs(my_y-my_fields[i][1])
                dstList.append(dst)                          #将所有的距离值存入数组中
        
        my_distancetolaststep=max(dstList)               #m的最大值
        return my_fields[dstList.index(my_distancetolaststep)][0],my_fields[dstList.index(my_distancetolaststep)][1]
    # 找到边界点，加入边界列表
    def edge(size, fields, my_id):
        edgelist = []

        # 上边界和下边界
        for i in range(1, WIDTH - 1):
            for j in range(1, HEIGHT - 1):
                if fields[i][j] == my_id:
                    if fields[i][j - 1] != my_id or fields[i][j + 1] != my_id:
                        edgelist.append((i, j))

        # 左边界和右边界
        for j in range(1, HEIGHT - 1):
            for i in range(1, WIDTH - 1):
                if fields[i][j] == my_id:
                    if fields[i - 1][j] != my_id or fields[i + 1][j] != my_id:
                        edgelist.append((i, j))
        return edgelist

    storage['edgeList'] = edge

    # 转向函数
    def turnDir(size, my_fields, my_id, my_direction, my_x, my_y):#12月28 by zym
        #边界点集
        temp_list = edge(size, my_fields, my_id)

        y_list = []
        x_list = []

        # 将所有的横坐标、纵坐标分别放在y_list,x_list中
        for i in range(len(temp_list)):
            y_list.append(temp_list[i][1])
            x_list.append(temp_list[i][0])

        # 求出现在位置，与边界横纵坐标的最大值和最小值
        max_y = abs(max(y_list) - my_y)
        min_y = abs(min(y_list) - my_y)
        max_x = abs(max(x_list) - my_x)
        min_x = abs(min(x_list) - my_x)

        if my_direction == 0:
            if max_y > min_y:
                #print('01')
                return 'R'
            else:
                #print('02')
                return 'L'

        elif my_direction == 2:
            if max_y >= min_y:
                #print('03')
                return 'L'
            else:
                #print('04')
                return 'R'

        elif my_direction == 1:
            if max_x > min_x:
                #print('05')
                return 'L'
            else:
                #print('06')
                return 'R'

        else:
            if max_x >= min_x:
                #print('7')
                return 'R'
            else:
                #print('8')
                return 'L'

    # 避免撞墙和纸带
        # 避免撞墙和纸带
    def avoidBoundaryAndBands(size, my_fields, my_bands, my_id, my_direction, my_x, my_y):#12月30 by tkg
        boundary_east  = (my_direction == 0 and my_x == (WIDTH - 1))
        boundary_south = (my_direction == 1 and my_y == (HEIGHT - 1))
        boundary_west  = (my_direction == 2 and my_x == 0)
        boundary_north = (my_direction == 3 and my_y == 0)

        band_east, band_south, band_west, band_north = 0, 0, 0, 0
        band_east_edge, band_south_edge, band_west_edge, band_north_edge = 0, 0, 0, 0
        if (0 < my_x < (WIDTH - 1) and 0 < my_y < (HEIGHT - 1)):
            band_east  = (my_direction == 0 and my_bands[my_x + 1][my_y] == my_id)
            band_south = (my_direction == 1 and my_bands[my_x][my_y + 1] == my_id)
            band_west  = (my_direction == 2 and my_bands[my_x - 1][my_y] == my_id)
            band_north = (my_direction == 3 and my_bands[my_x][my_y - 1] == my_id)
        elif ((my_direction == 0 and my_x == WIDTH - 1) or (my_direction == 1 and my_y == HEIGHT - 1) \
            or (my_direction == 2 and my_x == 0) or (my_direction == 3 and my_y == 0)):
            pass
        else:
            band_east_edge  = (my_direction == 0 and my_bands[my_x + 1][my_y] == my_id)
            band_south_edge = (my_direction == 1 and my_bands[my_x][my_y + 1] == my_id)
            band_west_edge  = (my_direction == 2 and my_bands[my_x - 1][my_y] == my_id)
            band_north_edge = (my_direction == 3 and my_bands[my_x][my_y - 1] == my_id)

        boundary = boundary_east or boundary_south or boundary_west or boundary_north
        band = band_east or band_south or band_west or band_north
        band_edge = band_east_edge or band_south_edge or band_west_edge or band_north_edge

        if boundary or band or band_edge:
            return turnDir(size, my_fields, my_id, my_direction, my_x, my_y)
        
    def fieldDirection(my_x,my_y,my_direction,size, fields, my_id):
        field_edge=edge(size, fields, my_id)  #用一个列表存储边界坐标
        x=[] #存储边界坐标中y值和my_y相等的点对应的x坐标
        y=[] #存储边界坐标中x值和my_x相等的点对应的y坐标
        dir=my_direction #存储我当前的朝向
        dis=[] #存储距离

        #找点
        y_edge=[]
        x_edge=[]
        for i in range(len(field_edge)):
            
            pos = field_edge[i]
            if(pos[0]==my_x):
                y_edge.append(pos[1])
                y.append(max(y_edge))
                y.append(min(y_edge))
            if(pos[1]==my_y):
                x_edge.append(pos[0])
                x.append(max(x_edge))
                x.append(min(x_edge))
            


        '''
        #计算distance
        for i in range(len(y)):
            dis.append(abs(y[i]-my_y))
        for i in range(len(x)):
            dis.append(abs(x[i]-my_x))

        #判断最小距离以及最优转向
        index=dis.index(min(dis))
        if(index>len(y)):
            flag='1' #最小距离出现在x轴方向
        else:
            flag='0' #最小距离出现在y轴方向
        '''


        #0和2，在x轴方向出现最小距离都可以直走
        if(dir==0):
            for i in range(len(y)):
                dis.append(abs(y[i]-my_y))
            for i in range(len(x)):
                if(x[i]>my_x):
                    dis.append(abs(x[i]-my_x))
            if dis ==None:
                return 'U'
            index=dis.index(min(dis))
            if(index>=len(y)):#最小距离出现在x轴方向
                return 'U'
            else:
                if((y[index]-my_y)>0): return 'R'
                if((y[index]-my_y)<0): return 'L'
                if((max(y_edge)-my_y)==0): return 'R'
                if((min(y_edge)-my_y)==0): return 'L'

        if(dir==2):
            for i in range(len(y)):
                dis.append(abs(y[i]-my_y))
            for i in range(len(x)):
                if(x[i]<my_x):
                    dis.append(abs(x[i]-my_x))

            index=dis.index(min(dis))
            if(index>=len(y)):#最小距离出现在x轴方向
                return 'U'
            else:#最小距离出现在y轴方向
                if((y[index]-my_y)>0): return 'L'
                if((y[index]-my_y)<0): return 'R'
                if((max(y_edge)-my_y)==0): return 'L'
                if((min(y_edge)-my_y)==0): return 'R'


        #1和3，在y轴方向出现最小距离都可以直走
        if(dir==1):
            for i in range(len(x)):
                dis.append(abs(x[i]-my_x))
            for i in range(len(y)):
                if(y[i]<my_y):
                    dis.append(abs(y[i]-my_y))

            index=dis.index(min(dis))
            if(index>=len(x)):#最小距离出现在y轴方向
                return 'U'
            else:#最小距离出现在x轴方向
                if((x[index]-my_x)>0): return 'L'
                if((x[index]-my_x)<0): return 'R'
                if((max(x_edge)-my_x)==0): return 'L'
                if((min(x_edge)-my_x)==0): return 'R'        


        if(dir==3):
            for i in range(len(x)):
                dis.append(abs(x[i]-my_x))
            for i in range(len(y)):
                if(y[i]>my_y):
                    dis.append(abs(y[i]-my_y))

            index=dis.index(min(dis))
            if(index>=len(x)):#最小距离出现在y轴方向
                return 'U'
            else:#最小距离出现在x轴方向
                if((x[index]-my_x)>0): return 'R'
                if((x[index]-my_x)<0): return 'L'
                if((max(x_edge)-my_x)==0): return 'R'
                if((min(x_edge)-my_x)==0): return 'L'    
    #头部距离敌方纸带的最小距离
    def getNearestDistanceToEnermy(my_x,my_y,bands,your_id,size):
        your_bands=bandsPoint(bands, your_id, size) 
        distance3=[]
        for i in range(len(your_bands)):                                  #访问所有对方纸带的坐标
            distance4=abs(my_x-your_bands[i][0])+abs(my_y-your_bands[i][1])
            distance3.append(distance4)
        my_distancetoenermy=min(distance3)                                #返回最小街区距离
        return my_distancetoenermy
    
    def TheWayToGetPoint(my_x, my_y, your_x, your_y, my_bands, my_direction):
        wayList = []
        for x in range(min(my_x, your_x), max(my_x, your_x)):  # 将到达敌方纸带路径上的点储存在wayList里
            wayList.append((x, my_y))
        for y in range(min(my_y, your_y), max(my_y, your_y)):
            wayList.append((your_x, y))

        if my_direction == 0 or my_direction == 2:
            if my_x - your_x < 0:
                dir = 0
            elif my_x - your_x > 0:
                dir = 2
            else:
                if my_y - your_y < 0:
                    dir = 1
                elif my_y - your_y > 0:
                    dir = 3
                elif my_y - your_y == 0:
                    return None

            if abs(my_direction - dir) != 2:
                return (dir)
            else:
                if my_y - your_y < 0:
                    dir = 1
                elif my_y - your_y > 0:
                    dir = 3
                elif my_y - your_y == 0:
                    #return None
                    if my_y == (HEIGHT - 1):
                        dir = 3
                    else:
                        dir = 1
                return (dir)
        else:
            if my_y - your_y < 0:
                dir = 1
            elif my_y - your_y > 0:
                dir = 3
            else:
                if my_x - your_x < 0:
                    dir = 0
                elif my_x - your_x > 0:
                    dir = 2
                elif my_x - your_x == 0:
                    return None
            if abs(my_direction - dir) != 2:
                return (dir)
            else:
                if my_x - your_x < 0:
                    dir = 0
                elif my_x - your_x > 0:
                    dir = 2
                elif my_x - your_x == 0:
                    if my_x == (WIDTH - 1):
                        dir = 2
                    else:
                        dir = 0
                return (dir)


    def howToImitate(my_pos,next_pos):
            flag = (my_pos-next_pos)
            if flag == 3 or flag == -1 :
                return 'R'
            elif flag == 0:
                return 'U'
            elif flag == -3 or flag ==1 :
                return 'L'
            else:
                return None
    def getNearstPointToFields(my_x,my_y,fields,id):#id/x/y/可以调节
        min_distancetofields=10000
        my_fields = fieldsPoint(fields, id, size)
        for i in range(len(my_fields)):
            distance1=abs(my_fields[i][0]-my_x)+abs(my_fields[i][1]-my_y)
            if (distance1 < min_distancetofields):
                min_distancetofields=distance1                            #如果头部在大本营内部，最终返回距离值为0
                nearest_x=my_fields[i][0]
                nearest_y=my_fields[i][1]
        return nearest_x,nearest_y               #返回的是tuplel类型

    def absDis(x1,y1,x2,y2):
        return (abs(x1-x2)+abs(y1-y2))
    def MtoMFields(my_x,my_y,fields,bands,size,my_id,your_id):
        min_dis = 10000
        #if fields[my_x][my_y] ==my_id:
        #    return 0,my_x,my_y
        fields_points = fieldsPoint(fields,my_id,size)
        for i in range(len(fields_points)):
            temp_dis = absDis(my_x,my_y,fields_points[i][0],fields_points[i][1])
            #if fields_points[i][0] !=my_x and fields_points[i][1]!=my_y:
            if temp_dis<=min_dis:
                min_dis = temp_dis
                my_index = i
        return min_dis,fields_points[my_index][0],fields_points[my_index][1]
    def YtoYFields(your_x,your_y,fields,bands,size,your_id):
        min_dis = 10000
        #if fields[your_x][your_x] ==your_id:
        #    return 0,your_x,your_x
        fields_points = fieldsPoint(fields,your_id,size)
        for i in range(len(fields_points)):
            temp_dis = absDis(your_x,your_y,fields_points[i][0],fields_points[i][1])
            if fields_points[i][0] !=your_x and fields_points[i][1]!=your_y:
                if temp_dis<=min_dis:
                    min_dis = temp_dis
                    my_index = i
        return min_dis,fields_points[my_index][0],fields_points[my_index][1]    
    def YtoMBands(your_x,your_y,fields,bands,size,my_id):
        min_dis = 10000
        bands_points = bandsPoint(bands,my_id,size)
        if bands_points==[]:
            return min_dis,your_x,your_y
        for i in range(len(bands_points)):
            temp_dis = absDis(your_x,your_y,bands_points[i][0],bands_points[i][1])
            if temp_dis<=min_dis:
                min_dis = temp_dis
                my_index = i
        return min_dis,bands_points[my_index][0],bands_points[my_index][1]
    storage['YtoMBands'] =YtoMBands
    def MtoYBands(my_x,my_y,fields,bands,size,your_id):
            min_dis = 10000
            bands_points = bandsPoint(bands,your_id,size)
            if bands_points==[]:
                return min_dis,my_x,my_y
            for i in range(len(bands_points)):
                temp_dis = absDis(my_x,my_y,bands_points[i][0],bands_points[i][1])
                if temp_dis<=min_dis:
                    min_dis = temp_dis
                    my_index = i
            return min_dis,bands_points[my_index][0],bands_points[my_index][1]
    class kill():
        def __init__(self):
            self.length = 0
            self.next_diec = 0    
        def killIt(self,my_id,your_id,my_x,my_y,my_direction,your_x,your_y,fields,bands,size):
            
            
            nouse={}
            storage['you_to_yourfields_distence'],nouse['x'],nouse['y'] = YtoYFields(your_x,your_y,fields,bands,size,your_id)
            storage['me_to_yourbands_distence'],nouse['x'],nouse['y'] = MtoYBands(my_x,my_y,fields,bands,size,your_id)
            storage['me_to_myfields_distence'],nouse['x'],nouse['y'] = MtoMFields(my_x,my_y,fields,bands,size,my_id,your_id)
            
            storage['you_to_mybands_distence'],nouse['x'],nouse['y'] = YtoMBands(your_x,your_y,fields,bands,size,my_id)
            #print( storage['you_to_yourfields_distence'],storage['me_to_yourbands_distence'],storage['me_to_myfields_distence'],storage['you_to_mybands_distence'])
            your_bands =bandsPoint(bands, your_id, size)
            if (storage['me_to_yourbands_distence']<=(storage['you_to_yourfields_distence']+aggressive)) and storage['you_to_yourfields_distence']!=0:#and storage['mode'] == 'main'
                next_point={}
                nouse['x'],next_point['x'], next_point['y'] = MtoYBands(my_x,my_y,fields,bands,size,your_id)
                
                if (next_point['x'], next_point['y']) not in your_bands:
                    storage['mode'] = 'kill'
                    next_direction = TheWayToGetPoint(my_x, my_y, next_point['x'], next_point['y'], your_bands,my_direction)
                    storage['turn'] = howToImitate(my_direction,next_direction)
                    return storage['turn']
            elif storage['mode'] == 'kill':
                storage['count'] = -2
                storage['mode'] = 'goback'
            elif storage['me_to_myfields_distence']>=(storage['you_to_mybands_distence']-defensive):
                storage['mode'] = 'goback'
            if storage['mode'] == 'goback' :
                next_point={}
                storage['mode'] == 'goback'
                nouse['y'],next_point['x'],next_point['y'] = MtoMFields(my_x,my_y,fields,bands,size,my_id,your_id)
                '''
                if (abs(temp_point['x']-my_point['x'])<=1) or (abs(temp_point['y']-my_point['y'])<=1):
                    next_point['x']=my_point['x']
                    next_point['y']=my_point['y']
                else:
                    next_point['x']=temp_point['x']
                    next_point['y']=temp_point['y']
                    my_point['x']=temp_point['x']
                    my_point['y']=temp_point['y']
                '''
                #print('go',next_point['x'],next_point['y'])
                #print(my_x, my_y)
                next_direction = TheWayToGetPoint(my_x, my_y, next_point['x'], next_point['y'], your_bands,my_direction)
                if next_direction!=None:
                    storage['turn'] = howToImitate(my_direction,next_direction)
                if fields[my_x][my_y]== my_id:
                    storage['count'] = -2
                    storage['mode']='main'
                else:
                    return storage['turn']
       
    storage['kill'] = kill()        

    class square(object):#12月29 
        def __init__(self):
            self.length = 0
            storage['count'] = 10  #保存在storage当中便于修改，其实可用作是模式选择，不同的count值对应不同的模式，对应流程图不同的过程

        def clear(self):  #一个循环走完后调用这个函数
            self.length = 0
            storage['count'] = 3
        
        def goAhead(self, walk_length, size, my_fields, my_bands, my_id, my_direction, my_x, my_y,your_id):
            '''
            walk_length：要前进的距离也就是之前的mylength
            '''

            #return avoidBoundaryAndBands(size, my_fields, my_bands, my_id, my_direction, my_x, my_y)
            if storage['count'] == -10:
                self.length = storage['length']
                storage['count'] = 1

            if storage['count']==10 and self.length==0:
                self.length = walk_length
                storage['count'] = storage['count']-1

            if (storage['count']==9 or storage['count']==8 or storage['count']==7 ) and self.length==0:
                self.length = walk_length
                storage['count'] = storage['count']-1
                if storage['count']==6:
                    storage['count'] =-2
                return 'R'
                
            if  storage['count'] == -2:
                #print(storage['count'])
                if aheadField(my_fields,my_x,my_y,my_direction,my_id,size)==1:
                    if my_fields[my_x][my_y]==my_id:
                        #判断是否进入领地，如果进入进行下一个循环
                        storage['count'] = storage['count']-1
                else:
                    storage['mode']='goback'
                
            #流程图当中的第0过程 
            if storage['count'] == -3:
                #print(storage['count'])
                storage['turn']=fieldDirection(my_x,my_y,my_direction,size, my_fields, my_id)
                self.length = 100
                storage['count'] = storage['count']-1
                return storage['turn']
            if storage['count']==-4:
                #print(storage['count'])
                if my_fields[my_x][my_y]!=my_id:
                    self.clear()

            if self.length > 0:
                self.length = self.length - 1
                return 'U'

                

            

            if storage['count'] == 3:
                #print(storage['count'])
                
                storage['count'] = storage['count'] - 1  #storage['count']减去1后便于进入下一个模式
             
                self.length = walk_length  #相当于流程图当中的1过程
            
                

            if self.length == 0 and storage['count'] == 2:
                #此处写入判断旋转方向的函数
                storage['turn'] = turnDir(size, my_fields, my_id, my_direction, my_x, my_y)  #相当于流程图当中的2过程
                #print(storage['count'])
                storage['count'] = storage['count'] - 1  #storage['count']减去1后便于进入下一个模式
        
                self.length = getNearestDistancetolaststep(my_x,my_y,my_fields,my_direction,my_id,size,1)  #相当于流程图当中的3过程
                
                return storage['turn']

            if self.length == 0 and storage['count'] == 1:
                #print(storage['count'])
                storage['count'] = -2  #storage['count']减去1后便于进入下一个模式
                self.length = 100
                storage['turn'] = turnDir(size, my_fields, my_id, my_direction, my_x, my_y)  #相当于流程图当中的4过程
                return storage['turn']

            

            #avoidBoundary(size, my_fields, my_id, my_direction, my_x, my_y)

    storage['core'] = square()
    storage['avoidBoundaryAndBands'] = avoidBoundaryAndBands
    storage['getNearestDistancetolaststep'] =getNearestDistancetolaststep
    storage['getNearestDistanceToEnermy'] = getNearestDistanceToEnermy
