# game frame
import os.path
import random
import sys
import time

from yangke.common.win.win_x64 import (get_all_window, find_window, capture_pic_undecorated, post_key, do_click,
                                       get_size_of_window, find_pic)
from yangke.objDetect.ocr import ocr
from yangke.base import show_pic
from yangke.common.config import logger
from yangke.common.win.dminput import DM


class Step:
    def __init__(self, op, target, judge=None, condition=None, wait_method=None):
        """
        定义步骤，
        示例1：
        Step("press", "Ctrl+C", "until", Exist("人物"))  # 按Ctrl+C，直到画面中出现"人物"
        示例2：
        Step(None, None, "until", Exist("竹林偷伐者"))  # 相当于一直等待，直到画面中出现"竹林偷伐者"，该步骤才能通过，进而执行下一步
        示例3：
        Step("long-press-5", "R", None, None)  # 长按R键5s

        :param op: 操作类型，可取值"press", "double-press","left-click", "long-press-{i}",None, "right-click"等，
        其中"long-press-{i}"表示长按某个键i秒，如示例3所示
        None则表示不执行操作，可用于等到condition条件满足时使用，
        op也可以是一个函数或方法，这种情况下，Step.do()将直接调用该方法，此时self.target作为传递给该方法的参数。
        :param judge: 判断操作完成的类型，可取值为until、if或None，如果为None，则表示不判断
        :param wait_method: 条件不满足时，调用的方法，repeat表示重复执行op，如果取值为None，则等待而不重复操作
        """
        self.op = op

        # 按键操作则为键名，鼠标时间则为鼠标点击位置，鼠标点击位置可以通过Position类或Align定义
        self.target: Position | Align | str | tuple = target

        self.judge = judge
        self.condition: "Exist" = condition
        self.wait_method = wait_method

        self.pos = None  # 该步骤执行后，until后条件中判断的位置会保存在该变量中，便于后续使用
        self.obj = None  # 该步骤执行后，until后条件中判断的对象名会保存在该变量中，便于后续使用

    def pre_do(self, last_step):
        if last_step is None:
            return

        if isinstance(self.target, Align):
            self.target = self.target.get_window_pos(last_step.pos[0], last_step.pos[1])

    def _action(self, win_frame: "Frame"):
        logger.debug(f"操作：{self.op} {self.target}")
        if self.op is None:
            return
        elif callable(self.op):  # 如果op是一个可以调用的函数或方法，则直接调用
            if self.target is not None:
                self.op(self.target)
            else:
                self.op()
        elif self.op == "press":
            post_key(win_frame.window, self.target)
        elif self.op == "double-press":
            sleep_interval = random.randint(1, 10) / 100 + 0.1
            post_key(win_frame.window, self.target)
            time.sleep(sleep_interval)
            post_key(win_frame.window, self.target)
        elif self.op.startswith("long-press-"):
            # 长按某个键5s
            last_time = int(self.op.replace("long-press-", ""))
            post_key(win_frame.window, self.target, last_time=last_time)
        elif self.op == "left-click":
            if isinstance(self.target, Position):
                x, y = self.target.get_point(win_frame)
                win_frame.left_click(x, y)
            elif isinstance(self.target, tuple):
                x, y = self.target
                win_frame.left_click(x, y)
        elif self.op == "right-click":
            if isinstance(self.target, Position):
                x, y = self.target.get_point(win_frame)
                win_frame.left_click(x, y)
            elif isinstance(self.target, tuple):
                x, y = self.target
                win_frame.left_click(x, y)

    def do(self, win_frame: "Frame"):
        logger.debug(f"执行步骤：{self.__str__()}")
        self._action(win_frame)
        if self.judge is not None:
            satisfied = self.condition.satisfied(win_frame)
            while not satisfied:  # 如果结束条件不满足，则继续执行本步骤定义的操作
                if self.wait_method is None:
                    time.sleep(0.5)
                else:
                    self._action(win_frame)
                    time.sleep(1)
                satisfied = self.condition.satisfied(win_frame)
            self.pos = self.condition.pos
            self.obj = self.condition.obj
        else:
            self.pos = None
            self.obj = None
        logger.debug(f"步骤执行完毕：{self.__str__()}")
        return True

    def __str__(self):
        if self.judge is not None:
            return f"{self.op} {self.target} {self.judge} {self.condition.__str__()}"
        else:
            return f"{self.op} {self.target}"


class Steps:
    def __init__(self, steps):
        """
        定义游戏内操作的步骤
        """
        self.steps = steps

    def run(self, win_frame):
        """
        逐步执行Steps对象中记录的步骤
        """
        last_step: Step | None = None
        for step in self.steps:
            step: Step = step
            step.pre_do(last_step)  # 在步骤执行前进行的操作
            success = step.do(win_frame)  # 执行步骤，可能执行失败，如点击某个按钮但画面上找不到就会失败
            if not success and last_step is not None:  # 如果执行失败，就尝试再次执行上一个步骤
                last_step.do(win_frame)
                success = step.do(win_frame)

            if success:  # 如果当前步骤执行结束，就记录当前步骤
                last_step = step


class Frame:
    def __init__(self, title, game_path=None, sim_mode=None, sim_info=None):
        """
        游戏图像识别框架
        例如：frame = Frame("天谕",
                           sim_mode="大漠插件",
                           sim_info={"display": "normal", # 大漠绑定窗口的图色模式，模式参数参考dm.BindWindowEx()方法
                                     "mouse": "normal", # 大漠绑定窗口的鼠标模式
                                     "keypad": "normal", # 大漠绑定窗口的键盘模式
                                     "public": "dx.public.active.api", # 大漠绑定窗口的公用模式
                                     "mode": 0,  # 大漠绑定窗口的总模式
                                     "key": "mmdlljafd8c5cbf193e99306e9eb61ceb5bd44",  # 大漠的注册码
                                     "add_key": "ewdSEKFZP",
                                     "guard_type": "memory4", # 开启大漠防护盾的类型，参考dm.DmGuard()方法
                                     })  # 大漠的附加码

        :@param title: 游戏窗口标题，为标题的子字符串，但需要唯一确定的窗口
        :@param game_path: 游戏文件路径，如果不存在游戏窗口，则启动该可执行文件
        :@param sim_mode: 模拟键鼠的方法，默认是python自带的方法，可以取值【大漠插件】则会使用大漠插件的模拟键鼠方法，使用大漠插件时，可以通过sim_info参数传入大漠插件绑定窗口的模式
        """
        if sim_info is None:
            sim_info = {}
        self.set_window_size_steps = None  # 设置窗口尺寸的步骤
        self.title = title
        self.snapshot = None
        self.window = find_window(title, exact=False)
        self.sim_mode = sim_mode
        if isinstance(self.window, dict) and len(self.window) == 1:
            _ = list(self.window.keys())[0]
            self.window_title = self.window[_]
            self.window = _
        else:
            if len(self.window) > 1:
                _ = list(self.window.keys())[0]
                self.window_title = self.window[_]
                self.window = _
                logger.warning(f"找到多个包含{title}的窗口，默认使用第一个:{self.window_title}")
            else:
                logger.error(f"未找到或找到多个包含{title}的窗口，目前不支持这种情况！")
                sys.exit()
        self.window_size = get_size_of_window(self.window, True)  # 不包括标题栏的大小
        self.udf_steps = {}
        if sim_mode is None:
            pass
        elif sim_mode == "大漠插件":
            self.dm = DM(key=sim_info.get("key"), add_key=sim_info.get("add_key"))
            if sim_info.get("guard_type") is not None:
                self.dm.DmGuard(1, sim_info.get("guard_type"))
            self.dm.set_bindmode(sim_info.get("display"), sim_info.get("mouse"),
                                 sim_info.get("keypad"), sim_info.get("public"),
                                 sim_info.get("mode"))
            self.dm.band_window(self.window)

    def press_key(self, key):
        if self.sim_mode == "大漠插件":
            self.dm.press_key(key)
        else:
            post_key(self.window, key)

    def left_click(self, x, y):
        if self.sim_mode == "大漠插件":
            self.dm.left_click(x, y)
        else:
            do_click(x, y, self.window)

    def right_click(self, x, y):
        if self.sim_mode == "大漠插件":
            self.dm.right_click(x, y)
        else:
            do_click(x, y, self.window, right=True)

    def show_snapshot(self):
        show_pic(self.snapshot)

    def define_set_window_size(self, steps: Steps):
        self.set_window_size_steps = steps

    def define_steps(self, steps_name, steps):
        self.udf_steps.update({steps_name: steps})

    def capture_window_xywh(self, x=0, y=0, w=0, h=0):
        """
        按照xywh四个点的坐标截取屏幕区域的图片
        """
        if w == 0:
            w = self.get_window_size()[0]
        if h == 0:
            h = self.get_window_size()[1]
        x2 = x + w
        y2 = y + h
        self.snapshot = capture_pic_undecorated(self.window, x, y, x2, y2)
        return self.snapshot

    def capture_window_xyxy(self, x1, y1, x2, y2):
        """
        按照xyxy四个点的坐标截取屏幕区域的图片，第一个xy是区域左上角坐标，第二个xy是区域右下角坐标
        """
        self.snapshot = capture_pic_undecorated(self.window, x1, y1, x2, y2)
        return self.snapshot

    def set_window_size(self, width=None, height=None):
        """
        将游戏窗口设置为指定大小
        @return:
        """
        # show_pic(self.capture_window())
        self.run_steps(self.set_window_size_steps)

    def run_steps(self, steps: Steps | str):
        if isinstance(steps, Steps):
            steps.run(self)
        else:
            if self.udf_steps.get(steps) is not None:
                self.run_steps(self.udf_steps.get(steps))

    def run_steps_forever(self, steps: Steps | str, interval=5):
        """
        无限执行指定按键步骤，常用于卡键盘按键
        """

        while True:
            random_sec = random.randint(1, 10) / 10
            self.run_steps(steps)
            time.sleep(random_sec + interval)
            # logger.debug(f"运行步骤{steps=}")

    def get_text(self, region=None):
        if region is None:
            self.capture_window_xywh()
        else:
            if isinstance(region, Region):
                region = region.get_region(win_frame=self)

            self.capture_window_xywh(*region)

        return ocr(self.snapshot, paragraph=True)

    def get_text_position(self, text, region=None):
        """
        获取给定文字在画面上的位置
        """
        if region is not None:
            pic = self.capture_window_xywh(*region)
        else:
            pic = self.capture_window_xywh()

    def get_window_size(self, refresh=False):
        if refresh:
            self.window_size = get_size_of_window(self.window)
        return self.window_size


class Exist:
    def __init__(self, value: str | list = "查找的文字或列表", type_="text", op="or", region=None,
                 last_time=0, interval=1):
        """
        判断画面中是否存在某个元素的类，如果条件判断过之后，可以通过对象的pos和obj成员变量获取具体的位置和对象信息.
        在last_time时间段内，任意一次查询找到了value，则Exist对象的satisfied方法返回True，否则返回False。默认1s查找一次

        @param type_: 元素的类型，可取值为text或pic，分别表示文字与图片
        @param value: 元素的值的列表
        @param op: 元素值列表存在于画面中的条件是 与还是或
        @param region: 可以通过该参数指定画面区域
        @param last_time: 判断的持续时间，取值单位为s，例如10表示10s内一直满足存在判断条件时，则返回True。取值为0则只判断一次
        """
        self.type_ = type_
        self.value = value if isinstance(value, list) else [value]
        self.op = op
        self.region = region
        self.last_time = last_time
        self.interval = interval
        self.pos = None
        self.obj = None

    def _satisfied(self, win_frame: "Frame"):
        """
        画面中存在某个元素的条件是否满足，该方法执行后，可以通过对象的pos和obj成员变量获取具体的位置和对象信息

        @param win_frame:
        @return:
        """
        if self.type_ == "text":
            text = win_frame.get_text(self.region)
            if self.op == "or":
                for v in self.value:
                    if v in text:
                        logger.debug(f"当前画面中找到【{v}】 in 【{text}】")
                        return True
                return False
            else:
                for v in self.value:
                    if v not in text:
                        return False
                return True
        elif self.type_ == "pic":
            if self.region is None:
                pic = win_frame.capture_window_xywh()
            else:
                pic = win_frame.capture_window_xywh()

            if len(self.value) == 1:
                small_pic_path = os.path.abspath(self.value[0])
                res = find_pic(small_pic_path, pic)
                self.pos = res[1]
                self.obj = self.value[0]
                return res[0]
            else:
                if self.op == "or":
                    for v in self.value:
                        small_pic_path = os.path.abspath(v)
                        res = find_pic(small_pic_path, pic)
                        if res[0]:
                            self.obj = v
                            self.pos = res[1]
                            return True
                    return False
                elif self.op == "and":
                    for v in self.value:
                        small_pic_path = os.path.abspath(v)
                        res = find_pic(small_pic_path, pic)
                        if not res[0]:
                            return False
                        self.obj = v
                        self.pos = res[1]
                    return True

    def satisfied(self, win_frame: "Frame", interval=1):
        if interval != 1 and self.interval == 1:
            self.interval = interval
        if self.last_time == 0:
            return self._satisfied(win_frame)
        else:
            for t in range(self.last_time + 1):
                if self._satisfied(win_frame):
                    return True
                time.sleep(self.interval)
            return False

    def __str__(self):
        return f"exist {self.value}"


class NotExist:
    def __init__(self, value: str | list = "查找的文字或列表", type_="text", op="or",
                 region=None,
                 last_time=0):
        """
        在last_time时间内一直找不到value，则NotExist对象的satisfied()方法返回True。任意一次找到则返回False。默认1s查找一次
        """
        self.exist = Exist(value=value, type_=type_, op=op, region=region, last_time=last_time)
        self.pos = self.exist.pos
        self.obj = self.exist.obj

    def satisfied(self, win_frame: "Frame", interval=1):
        return not self.exist.satisfied(win_frame, interval=interval)

    def __str__(self):
        return f"not exist {self.exist.value}"


class Align:
    def __init__(self, x_offset, y_offset=0):
        """
        ALign对象记录了一个元素相对另一个元素的偏移量或其他对齐信息
        """
        self.dx = x_offset
        self.dy = y_offset

    def get_window_pos(self, rx, ry):
        """
        rx, ry是Align对象参考的其他元素的坐标
        """
        x = self.dx + rx
        y = self.dy + ry
        return x, y

    def get_screen_pos(self, rx, ry):
        return 0, 0


class Position:
    def __init__(self, value, align: str | Align = 'center', region=None):
        """
        定义画面上的位置对象

        @param value:
        @param align:
        """
        self.value = value
        self.region = region

    def get_point(self, win_frame: "Frame"):
        """
        获取位置在画面上的相对坐标
        @param win_frame:
        @return:
        """
        if isinstance(self.value, str):
            pos = win_frame.get_text_position(self.value)
            return pos
        else:
            return None


class Region:
    def __init__(self, win_frame: "Frame | None" = None, align="center", width_child=0, height_child=0):
        """
        定义窗口中的某个区域，通过该类可以获取(x,y,w,h)这种类型的相对区域坐标
        示例：
        region = Region(frame)
        r.get_region(align="center", width_child=100, height_child=110)

        示例2：
        region = Region(align="center", width_child=100, height_child=110).get_region(win_frame)

        get_region()方法返回的是区域表示的(x,y,w,h)四个参数的tuple
        """
        self.frame = win_frame
        if self.frame is not None:
            self.width_window, self.height_window = win_frame.get_window_size()
            self.align = None
            self.width_child = None
            self.height_child = None
        else:
            self.width_window, self.height_window = None, None
            self.align = align
            self.width_child = width_child
            self.height_child = height_child

    def get_region(self, win_frame=None, align=None, width_child=None, height_child=None):
        """
        根据传入的区域定义，获取区域的数字范围，默认返回整个窗口区域。例如：
        region.get_region("center", 100, 100)  # 表示窗口中间100*100范围的(x,y,w,h)定义
        return (x,y,w,h)
        """
        if win_frame is not None:
            self.frame = win_frame
            self.width_window, self.height_window = win_frame.get_window_size()
        self.align = align or self.align or "center"
        self.width_child = width_child or self.width_child
        self.height_child = height_child or self.height_child

        if self.width_child is None or self.width_child == 0:  # 如果不指定区域的宽和高，则默认宽和高等于窗口的宽和高
            self.width_child = self.width_window
        if self.height_child is None or self.height_child == 0:
            self.height_child = self.height_window
        if self.align == "center":
            left_pad = int((self.width_window - self.width_child) / 2)
            top_pad = int((self.height_window - self.height_child) / 2)
        elif align == "left":
            left_pad = 0
            top_pad = int((self.height_window - self.height_child) / 2)
        elif align == "right":
            left_pad = self.width_window - self.width_child
            top_pad = int((self.height_window - self.height_child) / 2)
        elif align == "top":
            left_pad = int((self.width_window - self.width_child) / 2)
            top_pad = 0
        elif align == "bottom":
            left_pad = int((self.width_window - self.width_child) / 2)
            top_pad = self.height_window - self.height_child
        else:
            left_pad = 0
            top_pad = 0
        return left_pad, top_pad, self.width_child, self.height_child


if __name__ == "__main__":
    # logger.debug(ocr("temp.png", paragraph=False))
    frame = Frame('天谕-无束缚3D')
    # frame = Frame('舒海云')
    # frame = Frame('天谕-无束缚3D幻想网游', sim_mode="大漠插件", sim_info={
    #     "display": "dx.graphic.opengl",
    #     "mouse": "dx.mouse.position.lock.api|dx.mouse.position.lock.message|dx.mouse.clip.lock.api|"
    #              "dx.mouse.input.lock.api|dx.mouse.state.api|dx.mouse.api|dx.mouse.cursor",
    #     "keypad": "windows",
    #     "public": "dx.public.active.api|dx.public.active.message|dx.public.hide.dll|dx.public.active.api2|dx."
    #               "public.anti.api|dx.public.km.protect|dx.public.inject.super|dx.public.memory|"
    #               "dx.public.inject.c",
    #     "mode": 11,
    #     "key": "mmdlljafd8c5cbf193e99306e9eb61ceb5bd44",
    #     "add_key": "ewdSEKFZP",
    #     "guard_type": "memory4",
    # })
    # frame = Frame('记事本')
    # frame = Frame('炎火前哨, 宁梦')
    r = Region(frame)
    # steps_1 = Steps(
    #     steps=[
    #         # 按Esc键，直到窗口中心区域(317, 532)大小范围内出现文字"游戏设置"
    #         Step("press", "escape", "until", Exist(value="游戏设置", region=r.get_region("center", 317, 532))),
    #
    #         # 单击中心区域的【游戏设置】，直到中心区域(874, 609)出现【分辨率】
    #         Step("left-click", Position("游戏设置", region=r.get_region("center", 874, 609)), "until",
    #              Exist(value="分辨率", region=r.get_region("center", 874, 609))),
    #
    #         # 单机
    #         Step("left-click", Position("分辨率", align=Align(20)), "until", Exist())
    #     ])
    # frame.define_set_window_size(steps=steps_1)
    # frame.set_window_size()

    steps_2 = Steps(
        steps=[
            Step("press", "numpad0", "until", Exist(value='pic1.png', type_='pic'), wait_method="repeat"),
            Step("left-click", Align(397, 16), "until", Exist("门派"), wait_method="repeat"),
            Step("left-click", Align(0, 0), "until", Exist("苏澜郡"), wait_method="repeat"),
            Step("left-click", Align(0, 0), "until", Exist("汐族"), wait_method="repeat"),
        ]
    )
    frame.define_steps("打开苏澜郡声望面板", steps_2)
    # frame.run_steps("打开苏澜郡声望面板")

    steps_重复按键 = Steps(
        steps=[
            # Step("press", "R", None),
            Step("press", "R", "until",
                 NotExist("竹林偷伐者", last_time=20, region=Region(align="center", width_child=600)),
                 wait_method="repeat"),
            Step("double-press", "space", "until",
                 Exist("竹林偷伐者", last_time=60, interval=10, region=Region(align="center", width_child=600)),
                 wait_method="repeat"),
            # Step(None, None, "until",
            #      Exist("草药", last_time=60, interval=5),
            #      wait_method="repeat"),  # 等待场景中出现【草药】
            # Step("right-click", "草药", "until",
            #      Exist(),
            #      wait_method=None
            #      )
        ]
    )

    # frame.run_steps(steps_重复按键)
    frame.run_steps_forever(steps_重复按键, interval=8)
    # frame.capture_window()
    # logger.debug(frame.get_text())
