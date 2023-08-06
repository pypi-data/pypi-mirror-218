# dm_ret = dm.BindWindowEx(hwnd,"dx.graphic.opengl","dx.mouse.position.lock.api|dx.mouse.position.lock.message|dx.mouse.clip.lock.api|dx.mouse.input.lock.api|dx.mouse.state.api|dx.mouse.api|dx.mouse.cursor","windows","dx.public.active.api|dx.public.active.message|dx.public.hide.dll|dx.public.active.api2|dx.public.anti.api|dx.public.km.protect|dx.public.inject.super|dx.public.memory|dx.public.inject.c",11)
from yangke.common.config import logger
import win32com.client
import ctypes


class DM:
    def __init__(self, key="mmdlljafd8c5cbf193e99306e9eb61ceb5bd44", add_key="ewdSEKFZP"):
        self.dm = None
        self.key = key
        self.add_key = add_key
        self.bind_mode: list | None = None
        self.load_dm()
        self.is_bind = False

    def load_dm(self):
        try:
            self.dm = win32com.client.Dispatch('dm.dmsoft')
            print('本机系统中已经安装大漠插件，版本为:', self.dm.ver())
        except:
            print('本机并未安装大漠，正在免注册调用')
            dms = ctypes.windll.LoadLibrary('C://Users/DmReg.dll')
            location_dmreg = 'C://Users/dmyk/dm.dll'
            dms.SetDllPathW(location_dmreg, 0)
            self.dm = win32com.client.Dispatch('dm.dmsoft')

            # dm = CreateObject('dm.dmsoft')
            print('免注册调用成功 版本号为:', self.dm.Ver())

            res = self.dm.Reg(self.key, self.add_key)
            if res == 1:
                print('大漠注册成功！')
            elif res == -1:
                logger.error("大漠插件无法连接网络")
            elif res == -2:
                logger.error("进程没有以管理员方式运行. (出现在win7 win8 vista 2008.建议关闭uac)")
            elif res == 2:
                logger.error("大漠余额不足")
            elif res == 3:
                logger.error("绑定了本机器，但是账户余额不足50元.")
            elif res == 4:
                logger.error("注册码错误")
            elif res == 5:
                logger.error("你的机器或者IP在黑名单列表中或者不在白名单列表中")
            elif res == 6:
                logger.error(
                    "非法使用插件. 一般出现在定制插件时，使用了和绑定的用户名不同的注册码.  也有可能是系统的语言设置不是中文简体,也可能有这个错误.")
            elif res == 7:
                logger.error(
                    "你的帐号因为非法使用被封禁. （如果是在虚拟机中使用插件，必须使用Reg或者RegEx，不能使用RegNoMac或者RegExNoMac,否则可能会造成封号，或者封禁机器）")
            elif res == 8:
                logger.error("ver_info不在你设置的附加白名单中.")

    def DmGuard(self, enable, type_="memory4"):
        res = self.dm.DmGuard(1, "memory4")
        if res == 1:
            print("大漠防护盾开启成功")
        else:
            logger.warning(f"大漠防护盾开启失败，错误码：{res}")

    def set_bindmode(self, display="dx.graphic.opengl",
                     mouse="dx.mouse.position.lock.api|dx.mouse.position.lock.message|dx.mouse.clip.lock.api|"
                           "dx.mouse.input.lock.api|dx.mouse.state.api|dx.mouse.api|dx.mouse.cursor",
                     keypad="windows",
                     public="dx.public.active.api|dx.public.active.message|dx.public.hide.dll|dx.public.active.api2|dx."
                            "public.anti.api|dx.public.km.protect|dx.public.inject.super|dx.public.memory|"
                            "dx.public.inject.c",
                     mode=11):
        """
        设置大漠的窗口绑定方式，参考BindWindow参数说明
        """
        self.bind_mode = [display, mouse, keypad, public, mode]

    def band_window(self, hwnd):
        if self.dm is None:
            self.load_dm()
        res = self.dm.BindWindowEx(hwnd, self.bind_mode[0], self.bind_mode[1], self.bind_mode[2], self.bind_mode[3],
                                   self.bind_mode[4])
        if res == 1:
            self.is_bind = True
        else:
            code = self.dm.GetLastError()
            logger.error(f"大漠绑定窗口失败，错误码：{code}")

    def press_key(self, key):
        """
        按键
        """
        self.dm.KeyPress(key)

    def left_click(self, x, y):
        self.dm.LeftClick(x, y)

    def right_click(self, x, y):
        self.dm.RightClick(x, y)
