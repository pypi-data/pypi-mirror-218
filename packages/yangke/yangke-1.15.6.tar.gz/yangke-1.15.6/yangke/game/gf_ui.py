from yangke.common.qt import YkWindow, run_app, logger, QApplication
from yangke.game.gf import Step, Steps, Frame, NotExist, Exist, Region
from yangke.base import start_threads, stop_threads


class MainWindow(YkWindow):
    def __init__(self):
        super().__init__()
        self.add_input_panel("ui/ui_panel.yaml")
        self.thread = None
        self.running = False
        self.set_status_bar_label("天谕")

    def run(self):
        settings = self.get_value_of_panel(need_dict=True, need_unit=False)
        key = settings.get("打怪技能按键")
        role = settings.get("游戏角色名").strip()
        frame = Frame(role)
        steps_重复按键 = Steps(
            steps=[
                Step("press", key, "until",
                     NotExist("竹林偷伐者", last_time=20, region=Region(align="center", width_child=600)),
                     wait_method="repeat"),
                Step("double-press", "space", "until",
                     Exist("竹林偷伐者", last_time=60, interval=10, region=Region(align="center", width_child=600)),
                     wait_method="repeat"),
                # Step(QApplication.processEvents(), None, None, None)  # 处理图形界面
            ]
        )
        self.thread = start_threads(frame.run_steps_forever, args_list=[steps_重复按键, 8])
        self._input_panel.get_button("运行").setDisabled(True)
        self._input_panel.get_button("停止").setDisabled(False)

    def stop(self):
        stop_threads(self.thread)
        self.running = False
        logger.debug(f"停止挂机")
        self._input_panel.get_button("停止").setDisabled(True)
        self._input_panel.get_button("运行").setDisabled(False)


run_app(MainWindow)
