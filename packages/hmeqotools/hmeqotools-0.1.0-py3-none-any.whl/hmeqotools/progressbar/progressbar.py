import time as _time
import threading as _threading
import sys as _sys
from collections import deque as _deque
from typing import Type as _Type
try:
    from pip._vendor.colorama.ansi import Fore as _Fore
except ModuleNotFoundError:
    pass


TIMER_DEFAULT = _time.perf_counter


class Base:

    def __init__(self, total=1):
        self._total = total
        self._progress = 0

    def refresh(self):
        """刷新."""
        pass

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, value):
        if value < 0:
            value = 0
        self._total = value
        if self._progress > self._total:
            self._progress = self._total
        self.refresh()

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        if value < 0:
            value = 0
        self._progress = value
        if self._progress > self._total:
            self._progress = self._total
        self.refresh()

    def add_progress(self, value):
        """增加进度."""
        self.progress += value


class ProgressBar(Base):
    """进度条.

    Attributes:
        lattice: 进度条格子数
        left_fill: 进度条左侧填充
        right_fill: 进度条右侧填充
        timer: 计时函数
        complete_auto_close: 完成自动关闭
        output: 输出函数
        speed_pre: 平均速度的精度
        alive: 线程可以存活
        finished: 进度条是否结束
        activated: 线程是否可以刷新一次
        ended: 线程是否结束

    Method:
        start: 启动
        finish: 完成
        wait: 等待结束

    可以用for循环调用
    format格式:
    {graph}  图形
    {percent}  百分比
    {progress}  进度
    {total}  总数
    {speed}  平均速度
    {time}  计时
    """

    format = "|{graph}|{percent} [{progress}/{total} {speed}/s] {time}"

    def __init__(self, **kwargs):
        super().__init__()
        self._start_time = 0
        self._graph_cache = ()

        self.lattice = 25
        self.left_fill = ("▏", "▎", "▍", "▌", "▋", "▊", "▉", "█")
        self.right_fill = " "  # "　" or " "
        self.timer = TIMER_DEFAULT
        self.complete_auto_close = True
        self.output = _sys.stdout.write
        self.cover_mode = 1
        self.speed_pre = 1

        self.alive = False
        self.finished = False
        self.activated = _threading.Event()
        self.ended = _threading.Event()

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __iter__(self):
        self._start()
        self._progress = -1
        return self

    def __next__(self):
        if self._progress == self._total:
            self.wait(1)
            raise StopIteration()
        self._progress += 1
        self.refresh()
        return self._progress

    def _thr_main(self):
        try:
            self._main()
        except Exception as error:
            print(error)
        self.alive = False
        self.ended.set()

    def _main(self):
        progress = 0
        last_tmp_len = 0
        self._start_time = self.timer()
        while not self.finished and self.activated.wait() and self.alive:
            if progress == self._progress:
                self.activated.clear()
            # 进度
            progress = self._progress
            # 计时
            elapsed_time = self.timer() - self._start_time
            # 进度百分比
            percent = progress / self._total if self._total else 1
            # 速度
            speed = progress / elapsed_time
            # 剩余时间
            eta = elapsed_time / percent * (1 - percent) if percent else 0

            # 完成自动关闭
            if self.complete_auto_close and percent == 1:
                self.finish()

            if self.output:
                # 按照模板输出
                tmp = self.format.format(
                    graph=self.graph_handler(percent),
                    percent=self.percent_handler(percent),
                    progress=self.numeric_handler(progress),
                    total=self.numeric_handler(self._total),
                    speed=self.speed_handler(speed),
                    time=self.time_handler(elapsed_time, eta),
                )
                tmp_len = len(tmp)
                if self.cover_mode:
                    if self.cover_mode == 1:
                        tmp = tmp.ljust(last_tmp_len + 1)
                    elif self.cover_mode == 2:
                        tmp = "\033[K" + tmp
                    tmp = "\r" + tmp
                    if self.finished:
                        tmp += "\n"
                last_tmp_len = tmp_len
                self.output(tmp)

    def _initial(self):
        """初始化."""
        self._progress = 0
        # 预存好所有进度条形态，以空间换取时间
        self._graph_cache = [self.right_fill * self.lattice]
        for left_fill_num in range(self.lattice):
            right_fill_num = self.lattice - 1 - left_fill_num
            lfc = "".ljust(left_fill_num, self.left_fill[-1])
            rfc = self.right_fill * right_fill_num
            for mfc in self.left_fill:
                self._graph_cache.append(lfc + mfc + rfc)
        self._graph_cache = tuple(self._graph_cache)

        self.finished = False
        self.activated.clear()
        self.ended.clear()

    def _start(self):
        self._initial()
        self.alive = True
        _threading.Thread(target=self._thr_main, daemon=True).start()

    def start(self):
        """启动."""
        self._start()
        self.activated.set()

    def close(self):
        """关闭."""
        self.alive = False
        self.activated.set()

    def finish(self):
        """完成."""
        self.finished = True
        self.activated.set()

    def wait(self, timeout=None):
        """等待结束."""
        self.ended.wait(timeout=timeout)

    def refresh(self):
        """刷新."""
        if not self.activated.is_set():
            self.activated.set()

    def fill_up(self):
        """填满."""
        self.progress = self._total

    def configure(self, **kwargs):
        """配置."""
        for k, v in kwargs.items():
            setattr(self, k, v)

    def graph_handler(self, percent):
        return self._graph_cache[int(percent * (len(self._graph_cache) - 1))]

    @staticmethod
    def percent_handler(num):
        return "%d%%" % (num * 100)

    @staticmethod
    def numeric_handler(num):
        return num

    def speed_handler(self, num):
        return round(num, self.speed_pre)

    def time_handler(self, elapsed_time, eta):
        if self.finished:
            if elapsed_time < 360:
                times = "END:%.3fs" % elapsed_time
            else:
                times = "END:%.3fh" % (elapsed_time / 3600)
        else:
            if elapsed_time < 360:
                a = "%ss" % int(elapsed_time)
            else:
                a = "%.1fh" % (elapsed_time / 3600)
            if eta < 360:
                b = "%ss" % int(eta)
            else:
                b = "%.1fh" % (eta / 3600)
            times = "%s ETA:%s" % (a, b)
        return times


class BaseDeq:

    def __init__(self, skippable=True):
        self.deq = _deque([])
        self.event = _threading.Event()
        self.lock = _threading.Lock()
        self.skippable = skippable

    def put(self, obj):
        self.lock.acquire()
        if self.skippable and self.deq and self.deq[-1]["skippable"]:
            self.deq.pop()
        self.deq.append(obj)
        if not self.event.is_set():
            self.event.set()
        self.lock.release()

    def get(self):
        self.event.wait()
        self.lock.acquire()
        obj = self.deq.popleft()
        if not self.deq:
            self.event.clear()
        self.lock.release()
        return obj


class BaseDetail:
    """自定义程度更高的进度条"""

    def __init__(self, total=1, skippable=True, **kwargs):
        # 进度
        self._total = total
        self._progress = 0
        # 控制输出
        self.deq = BaseDeq(skippable=skippable)
        self.ended = _threading.Event()
        self.alive = _threading.Event()
        self.finished = _threading.Event()
        self.auto_finish = True
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __iter__(self):
        self.start()
        self._progress = -1
        return self

    def __next__(self):
        if self._progress == self._total:
            self.wait(1)
            raise StopIteration
        self._progress += 1
        self.refresh()
        return self._progress

    def _mainloop(self):
        """循环更新"""
        self.on_start()
        self._put_update_info()
        info = self._get_update_info()
        while self.alive.is_set():
            self.on_update(info)
            if info["finished"]:
                break
            info = self._get_update_info()
        self.on_end()
        self.ended.set()

    def _get_update_info(self):
        """获取信息"""
        return self.deq.get()

    def _put_update_info(self, skippable=True, **info):
        """添加信息"""
        if (self.auto_finish
                and not self.finished.is_set()
                and self._progress == self._total):
            self.finished.set()
        self.deq.put({
            "total": self._total,
            "progress": self._progress,
            "skippable": skippable,
            "finished": self.finished.is_set(),
            **info,
        })

    def on_start(self):
        pass

    def on_update(self, info):
        pass

    def on_end(self):
        pass

    def start(self, daemon=True):
        self.alive.set()
        thr = _threading.Thread(target=self._mainloop, daemon=daemon)
        thr.start()
        return thr

    def refresh(self):
        """刷新"""
        self._put_update_info()

    def fill_up(self):
        """填满"""
        self.progress = self.total

    def finish(self):
        """完成"""
        self.finished.set()
        self._put_update_info()

    def close(self):
        """关闭"""
        self.alive.clear()
        self._put_update_info()

    def wait(self, timeout=None):
        """等待结束"""
        self.ended.wait(timeout=timeout)

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, value):
        if value < 0:
            value = 0
        self._total = value
        if self._progress > self._total:
            self._progress = self._total
        self._put_update_info()

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, value):
        if value < 0:
            value = 0
        self._progress = value
        if self._progress > self._total:
            self._progress = self._total
        self._put_update_info()

    def add_progress(self, value):
        """增加进度."""
        self.progress += value


class GraphStyle:

    lattice = 25
    left_fill = ("━",)
    right_fill = " "

    def __init__(self):
        self.graph_cache = ()

    @staticmethod
    def process_left(text) -> str:
        return text

    @staticmethod
    def process_right(text) -> str:
        return text

    def init(self):
        # 预存好所有进度条形态，以空间换取时间
        f_left = self.process_left("")
        f_right = self.process_right(self.right_fill * self.lattice)
        graph_cache = [(f_right, f_left, f_right)]
        for left_fill_num in range(self.lattice):
            right_fill_num = self.lattice - 1 - left_fill_num
            lfc = "".ljust(left_fill_num, self.left_fill[-1])
            f_right = self.right_fill * right_fill_num
            for mfc in self.left_fill:
                f_left = self.process_left(lfc + mfc)
                f_right = self.process_right(f_right)
                graph_cache.append((f_left + f_right, f_left, f_right))
        self.graph_cache = tuple(graph_cache)

    def product(self, percent):
        return self.graph_cache[int(percent * (len(self.graph_cache) - 1))]


class ColorfulGraphStyle(GraphStyle):

    @staticmethod
    def process_left(text) -> str:
        return _Fore.GREEN + text + _Fore.RESET


class PrecisionGraphStyle(GraphStyle):

    left_fill = ("▏", "▎", "▍", "▌", "▋", "▊", "▉", "█")
    right_fill = " "


class PrecisionGraphStyle2(PrecisionGraphStyle):

    right_fill = "　"


class DetailHandler:

    format = "|{graphLeft}{graphRight}|{percent} [{progress}/{total} {speed}] {timeHint}"

    def __init__(self, graph: _Type[GraphStyle] = ColorfulGraphStyle):
        self.graph = graph()
        self._last_text = ""
        self.handles = {
            "graphLeft": None,
            "graphRight": None,
            "total": None,
            "progress": None,
            "percent": lambda x: "{:.0%}".format(x["percent"]),
            "speed": lambda x: "%.1f/s" % x["speed"],
            "timeHint": None,
        }

    def __call__(self, info):
        if info.get("text"):
            self.detail_output(info["text"])

        info = self.info_handle(info)
        text = self.format.format(
            **{k: v(info) if v else info[k]
               for k, v in self.handles.items()})
        self.output(text)
        self._last_text = text

    @staticmethod
    def end():
        print()

    def info_handle(self, info):
        finished = info["finished"]
        total = info["total"]
        progress = info["progress"]
        percent = progress / total if total else 1.0
        graph = self.graph.product(percent)
        elapsed_time = info["t"]
        eta = elapsed_time / percent * (1 - percent) if percent else 0
        speed = progress / elapsed_time
        if finished:
            if elapsed_time < 360:
                time_hint = "END:%.3fs" % elapsed_time
            else:
                time_hint = "END:%.3fh" % (elapsed_time / 3600)
        else:
            if elapsed_time < 360:
                a = "%ss" % int(elapsed_time)
            else:
                a = "%.1fh" % (elapsed_time / 3600)
            if eta < 360:
                b = "%ss" % int(eta)
            else:
                b = "%.1fh" % (eta / 3600)
            time_hint = "%s ETA:%s" % (a, b)
        return {
            "total": total,
            "progress": progress,
            "percent": percent,
            "graph": graph[0],
            "graphLeft": graph[1],
            "graphRight": graph[2],
            "time": elapsed_time,
            "eta": eta,
            "speed": speed,
            "timeHint": time_hint,
            "finished": finished,
        }

    def init(self):
        self.graph.init()

    def detail_output(self, x):
        self.output(x)
        print()

    def output(self, x):
        print(end="\r" + x.ljust(len(self._last_text) + 1))


class Detail(BaseDetail):

    def __init__(self, total=1, handler=None, **kwargs):
        self.auto_finish = True
        self.timer = TIMER_DEFAULT
        self.handler = handler if handler else DetailHandler()
        self.on_update = self.handler
        self.on_end = self.handler.end
        super().__init__(total, **kwargs)
        self._start_time = 0

    def _put_update_info(self, skippable=True, **info):
        super()._put_update_info(
            skippable=skippable,
            t=self.timer() - self._start_time,
            **info)

    def on_start(self):
        self.handler.init()
        self._start_time = self.timer()

    def print(self, obj):
        """输出信息"""
        if not isinstance(obj, str):
            obj = str(obj)
        self._put_update_info(skippable=False, text=obj)

    def print_text(self, text=""):
        """输出文本"""
        self._put_update_info(skippable=False, text=text)


def main():
    n = 1000000
    # Detail
    det = Detail(total=n)
    for i in det:
        if not i % 111111:
            det.print_text("text: %s" % i)
    # ProgressBar
    pgb = ProgressBar(total=n, lattice=25, cover_mode=1)
    for _ in pgb:
        pass


if __name__ == "__main__":
    main()
