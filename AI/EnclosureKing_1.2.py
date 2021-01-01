'''
Group Name: 
        Eclosure King
Members:
        张洋铭
        刘星云
        刘佳慧
        张宁
        唐苛耕
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

    fields = stat['now']['fields']
    bands = stat['now']['bands']    #根据返回值判断是敌人的还是我的领地

    turnleft = stat['now']['turnleft'][my_id - 1]

    square = storage['core']
    print(size[0])
    #这句话放入寻找步长的函数，现在这个mylength只是根据回合数逐渐增加前进步数
    mylength = int(50000 / int(turnleft))
    whetherhit = avoidBoundaryAndBands(size, fields, bands, my_id, my_direction, my_x, my_y)
    if whetherhit ==None:
        return square.goAhead(mylength, size, fields, bands, my_id, my_direction, my_x, my_y)
    else:
        return whetherhit
    #mylength是行走步数


def load(stat, storage):

    size = stat['size']

    my_id = stat['now']['me']['id']
    your_id = stat['now']['enemy']['id']

    WIDTH = size[0]
    HEIGHT = size[1]

    # 查找纸带的区域，返回己方已经占有区域，一个list(tuple)
    def bandsPoint(bands, id, size):#1月1日 by lxy
        '''
        如果传入是id=my_id那么就是我的，id = your_id那么就是敌人的bands
        '''
        bandslist = []
        for i in range(WIDTH):
            for j in range(HEIGHT):
                if bands[i][j] == id:
                    bandslist.append((i, j))
        return bandslist
    def fieldsPoint(fields, id, size):
            '''
            如果传入是id=my_id那么就是我的fields，id = your_id那么就是敌人的fields
            '''
            fieldslist = []
            for i in range(WIDTH):
                for j in range(HEIGHT):
                    if fields[i][j] == id:
                        fieldsslist.append((i, j))
            return fieldslist

    #到达回到大本营的最后一步的最小距离
    def getNearestDistancetolaststep(my_x,my_y,fields,my_direction,my_id)#1月1日 by lxy
        dstList=[]                                       #建立一个空数组
        #tup0=tuple([my_x,my_y])
        my_fields = edge(size, fields, my_id)
        for i in range (len(my_fields)):                 #访问fields中的所有坐标,my_field只是边界
            if my_direction==0 or my_direction==2:        #如果当前方向为东西方向
                dst=abs(my_x-my_fields[i][0])
                dstList.append(dst)                          #将所有的距离值存入数组中
            #elif my_direction==1 or my_direction==3:           #如果当前方向为南北方向
            else:
                dst=abs(my_y-my_fields[i][1])
                dstList.append(dst)                          #将所有的距离值存入数组中
                my_distancetolaststep=min(dstList)
        return my_distancetolaststep

    def whetherInField(my_x,my_y,size, fields, id):#1月1日by zym
        '''
        查找我的：x = my_x
                 y = my_y
                 id = my_id
        查找敌人的；全改为your
        '''
        #判断是否在field里面
        my_fields_list = fieldsPoint(fields, my_id, size)
        for i in my_fields_list:
            if i == (my_x,my_y):
                return 1
            else:
                return 0

            
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
    def avoidBoundaryAndBands(size, my_fields, my_bands, my_id, my_direction, my_x, my_y):#12月30 by tkg
        boundary_east  = (my_direction == 0 and my_x == (WIDTH - 2))
        boundary_south = (my_direction == 1 and my_y == (HEIGHT - 2))
        boundary_west  = (my_direction == 2 and my_x == 1)
        boundary_north = (my_direction == 3 and my_y == 1)

        band_east, band_south, band_west, band_north = 0, 0, 0, 0
        if (0 < my_x < (WIDTH - 1)) and (0 < my_y < (HEIGHT - 1)):
            band_east  = (my_direction == 0 and my_bands[my_x + 1][my_y] == my_id)
            band_south = (my_direction == 1 and my_bands[my_x][my_y + 1] == my_id)
            band_west  = (my_direction == 2 and my_bands[my_x - 1][my_y] == my_id)
            band_north = (my_direction == 3 and my_bands[my_x][my_y - 1] == my_id)

        boundary = boundary_east or boundary_south or boundary_west or boundary_north
        band = band_east or band_south or band_west or band_north

        if boundary or band:
            return turnDir(size, my_fields, my_id, my_direction, my_x, my_y)

    class square(object):#12月29 by zym
        def __init__(self):
            self.length = 0
            storage['count'] = 3  #保存在storage当中便于修改，其实可用作是模式选择，不同的count值对应不同的模式，对应流程图不同的过程

        def clear(self):  #一个循环走完后调用这个函数
            self.length = 0
            storage['count'] = 3

        def goAhead(self, walk_length, size, my_fields, my_bands, my_id, my_direction, my_x, my_y):
            '''
            walk_length：要前进的距离也就是之前的mylength
            '''

            
            #return avoidBoundaryAndBands(size, my_fields, my_bands, my_id, my_direction, my_x, my_y)

            count = storage['count']
            if self.length > 0:
                self.length = self.length - 1
                return 'U'

            if count == 3:
                #此处写入判断最快出去field的方向的函数，流程图当中的第0过程，两边相同时默认向前
                count = count - 1  #count减去1后便于进入下一个模式
                storage['count'] = count
                self.length = walk_length  #相当于流程图当中的1过程

            if self.length == 0 and count == 2:
                #此处写入判断旋转方向的函数
                storage['turn'] = turnDir(size, my_fields, my_id, my_direction, my_x, my_y)  #相当于流程图当中的2过程

                count = count - 1  #count减去1后便于进入下一个模式
                storage['count'] = count
                self.length = walk_length  #相当于流程图当中的3过程
                return storage['turn']

            if self.length == 0 and count == 1:
                count = count - 1  #count减去1后便于进入下一个模式
                storage['count'] = count
                storage['turn'] = turnDir(size, my_fields, my_id, my_direction, my_x, my_y)  #相当于流程图当中的4过程

            if self.length == 0 and count == 0:
                count = count - 1  #count减去1后便于进入下一个模式
                storage['count'] = count
                self.length = getNearestDistancetolaststep(my_x,my_y,fields,my_direction,my_id)
                #此处写入要前进的距离（到领地的最小的距离）的函数,流程图当中的第5过程

            if self.length == 0 and count == -1:
                count = count - 1  #count减去1后便于进入下一个模式
                storage['count'] = count
                storage['turn'] = turnDir(size, my_fields, my_id, my_direction, my_x, my_y)  #相当于流程图当中的6过程
                self.length= 100 
                return storage['turn']

            if  count == -2 and whetherInField(my_x,my_y,size, fields, my_id):
                #判断是否进入领地，如果进入进行下一个循环

                self.clear()
            
            #avoidBoundary(size, my_fields, my_id, my_direction, my_x, my_y)

    storage['core'] = square()
