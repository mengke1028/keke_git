import turtle  # 导入turtle库，用于图形绘制
import random  # 导入random库，生成随机数
import math  # 导入math库，进行数学计算

turtle.setup(1.0, 1.0)  # 设置窗口大小为屏幕大小
turtle.title("流星雨动画")   # 设置窗口标题
turtle.bgcolor('black')  # 设置背景颜色为黑色

t = turtle.Turtle()  # 创建一个画笔对象
t.hideturtle()  # 隐藏画笔，不显示画布的形状
t.pensize(1)    # 设置画笔的大小

# 定义流星的颜色列表
colors = ['gold', 'yellow', 'orange']  # 金色


class Meteor:  # 定义流星类
    def __init__(self):  # 初始化方法，创建每颗流星时调用
        self.r = random.randint(50, 100)    # 随机生成流星的半径
        self.k = random.uniform(2, 4)   # 随机生成角度参数
        self.x = random.randint(-1000, 1000)  # 随机生成流星的x坐标
        self.y = random.randint(-500, 500)  # 随机生成流星的y坐标
        self.speed = random.randint(5, 10)  # 随机生成流星的移动速度
        self.color = random.choice(colors)  # 随机选择流星的颜色

    def meteor(self):  # 绘制流星的方法
        # 移动画笔到指定的坐标位置处
        t.penup()
        t.goto(self.x, self.y)
        t.pendown()
        # 设置流星的颜色
        t.begin_fill()
        t.fillcolor(self.color)
        # 开始绘制流星
        t.setheading(-30)  # 设置流星的朝向
        t.right(self.k)  # 根据随机角度右转
        t.forward(self.r)  # 沿直线前进一定长度
        t.left(self.k)  # 左转回到垂直方向
        t.circle(self.r * math.sin(math.radians(self.k)), 180)  # 绘制半圆弧
        t.left(self.k)  # 再次左转恢复角度
        t.forward(self.r)  # 沿直线前进相同长度以闭合流星形状
        t.end_fill()  # 结束填充

    def move(self):  # 更新流星位置的方法
        if self.y >= -500:  # 当流星的y坐标大于等于-500时
            self.y -= self.speed  # 减小流星y坐标的大小，将画笔向下移动
            self.x += 2 * self.speed  # 增加流星x坐标的大小，将画笔向右移动
        else:  # 当流星的y坐标小于-500时
            self.r = random.randint(50, 100)  # 重新设置流星的半径
            self.k = random.uniform(2, 4)  # 重新设置角度参数
            self.x = random.randint(-2000, 1000)  # 重新设置流星的x坐标
            self.y = 500  # 重新设置流星的y坐标
            self.speed = random.randint(5, 10)  # 重新设置流星的速度
            self.color = random.choice(colors)  # 重新设置流星的颜色


# 创建一个流星列表，用来存储流星实例
Meteors = []
for i in range(200):
    Meteors.append(Meteor())

# 进行无限循环，模拟流星雨动画
while True:
    turtle.tracer(0)  # 关闭tracer，提高性能
    t.clear()  # 清除画布内容
    for i in range(200):
        Meteors[i].move()  # 更新每颗流星的位置
        Meteors[i].meteor()  # 重新绘制每颗流星
    turtle.update()  # 更新屏幕显示内容
