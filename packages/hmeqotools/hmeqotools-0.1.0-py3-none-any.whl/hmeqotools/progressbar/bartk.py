import time as _time
import queue as _queue
import tkinter as _tk

from .progressbar import Base


def format_time(t):
    hour = int(t // 3600)
    t -= hour * 3600
    minute = int(t // 60)
    secend = int(t - minute*60)
    return "{:02d}:{:02d}:{:02d}".format(hour, minute, secend)


class TkTime(Base):
    """进度条, tkinter 部件."""

    def __init__(self, widget_master, **kwargs):
        super().__init__()
        self.draggable = True
        self._active = False
        self._q = _queue.Queue(1)

        self.frame = _tk.Frame(widget_master)
        # left message
        self.lm = _tk.Label(self.frame)
        # right message
        self.rm = _tk.Label(self.frame)
        # left progress
        self.lp = _tk.Frame(self.frame, bg="#9F9F9F")
        # right progress
        self.rp = _tk.Frame(self.frame, bg="#4F4F4F")
        self.pos_btn = _tk.Button(
            self.frame, bg="white", relief="ridge", state="disabled",
            takefocus=False)

        self.__initial_frame()
        self.__place_frame()

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __initial_frame(self):
        self.frame.pack_propagate(False)
        self.frame.configure(height=self.lm.winfo_reqheight() // 2)
        self.frame.bind("<Configure>", lambda x: self._update_layout())

        self.pos_btn.bind("<B1-Motion>", self._pos_btn_motion)
        self.pos_btn.bind("<ButtonPress-1>", self._pos_btn_press)
        self.pos_btn.bind("<ButtonRelease-1>", self._pos_btn_release)
        self.lp.bind("<ButtonPress-1>", self._lp_press)
        self.lp.bind("<ButtonRelease-1>", self._lp_release)
        self.lp.bind("<B1-Motion>", self._lp_motion)
        self.rp.bind("<ButtonPress-1>", self._rp_press)
        self.rp.bind("<ButtonRelease-1>", self._rp_release)
        self.rp.bind("<B1-Motion>", self._rp_motion)

    def __place_frame(self):
        self.lm.place(x=0, y=0, relheight=1.0, anchor="nw")
        self.rm.place(relx=1.0, y=0, relheight=1.0, anchor="ne")

    def _pos_btn_press(self, event):
        if self.draggable:
            self.pos_mouse_left_down(event)
            self.mouse_down(event)

    def _pos_btn_release(self, event):
        if self.draggable:
            self.pos_mouse_left_up(event)
            self.mouse_up(event)

    def _pos_btn_motion(self, event):
        if self.draggable:
            self.pos_mouse_left_motion(event)
            self.mouse_motion(event)
            self._main(event.x - self.pos_btn.winfo_width()//2)

    def _lp_press(self, event):
        if self.draggable:
            self.lp_mouse_left_down(event)
            self.mouse_down(event)
            self._main(event.x - self.lp.winfo_width())

    def _lp_release(self, event):
        if self.draggable:
            self.lp_mouse_left_up(event)
            self.mouse_up(event)

    def _lp_motion(self, event):
        if self.draggable:
            self.lp_mouse_left_motion(event)
            self.mouse_motion(event)
            self._main(event.x - self.lp.winfo_width())

    def _rp_press(self, event):
        if self.draggable:
            self.rp_mouse_left_down(event)
            self.mouse_down(event)
            self._main(event.x)

    def _rp_release(self, event):
        if self.draggable:
            self.rp_mouse_left_up(event)
            self.mouse_up(event)

    def _rp_motion(self, event):
        if self.draggable:
            self.rp_mouse_left_motion(event)
            self.mouse_motion(event)
            self._main(event.x)

    def _main(self, pos):
        if self._q.full():
            return None
        self._q.put(None)
        # 进度条整体宽度
        p_width = (self.frame.winfo_width()
                   - self.lm.winfo_width()
                   - self.rm.winfo_width())
        # 已过进度条宽度
        lp_width = int((self._progress / self._total
                        if self._total else 0) * p_width)
        # 已过进度条宽度 + 相对按钮左侧的x值 / 进度条整体宽度
        percent = (lp_width + pos) / p_width
        if percent > 1:
            progress = self._total
        elif percent < 0:
            progress = 0
        else:
            # 已过进度和总进度的像素比率乘以总进度，四舍五入为整数
            progress = round(percent * self._total)
        if progress != self._progress:
            self.progress = progress
            try:
                self.command(self.progress)
            except Exception as error:
                print(error)
        self._q.get()
        self._q.task_done()
        return None

    def _update_layout(self):
        progress = self._progress
        # 更新左右标签宽度
        self.lm.configure(width=len(self.lm["text"]))
        self.rm.configure(width=len(self.rm["text"]))
        # 当前框架、左右标签宽度
        frame_width = self.frame.winfo_width()
        lm_width = self.lm.winfo_width()
        rm_width = self.rm.winfo_width()
        # 进度条可用宽度
        p_width = frame_width - lm_width - rm_width
        # 进度百分比
        if self._total:
            percent = progress / self._total
        else:
            percent = 0
        # 左右进度条宽度
        lp_width = int(percent*p_width)
        rp_width = p_width - lp_width
        # 设置宽度
        self.lp.configure(width=lp_width)
        self.rp.configure(width=rp_width)

        # 放置
        # 已过进度
        if lp_width:
            self.lp.place(x=lm_width, y=0, relheight=1.0, anchor="nw")
        else:
            self.lp.place_forget()
        # 未过进度
        if rp_width:
            self.rp.place(x=frame_width - rm_width, y=0,
                          relheight=1.0, anchor="ne")
        else:
            self.rp.place_forget()
        # 进度指针
        self.pos_btn.place(x=lm_width + lp_width, y=0,
                           relheight=1.0, anchor="n")

    def pack(self, *args, **kwargs):
        self.frame.pack(*args, **kwargs)

    def place(self, *args, **kwargs):
        self.frame.place(*args, **kwargs)

    def grid(self, *args, **kwargs):
        self.frame.grid(*args, **kwargs)

    def start(self):
        """启动."""
        self._active = True
        self._progress = 0

    def close(self):
        """关闭."""
        if self._active:
            self._active = False

    def refresh(self):
        """刷新布局."""
        self.lm.configure(text=format_time(self._progress))
        self.rm.configure(text=format_time(self._total))
        self._update_layout()

    def mouse_down(self, event):
        pass

    def mouse_up(self, event):
        pass

    def mouse_motion(self, event):
        pass

    def pos_mouse_left_down(self, event):
        pass

    def pos_mouse_left_up(self, event):
        pass

    def pos_mouse_left_motion(self, event):
        pass

    def lp_mouse_left_down(self, event):
        pass

    def lp_mouse_left_up(self, event):
        pass

    def lp_mouse_left_motion(self, event):
        pass

    def rp_mouse_left_down(self, event):
        pass

    def rp_mouse_left_up(self, event):
        pass

    def rp_mouse_left_motion(self, event):
        pass

    def command(self, progress: int):
        ...


def main():
    # Tk time
    class MyWindow(_tk.Tk):

        def __init__(self):
            super().__init__()
            self.geometry("800x500")

            self.bar = TkTime(self, total=120)
            self.bar.command = lambda progress: print(progress)
            self.bar.start()
            self.bar.place(x=0, y=10, relwidth=1.0, relheight=0.05)
            # threading.Thread(target=self.test).start()

        def test(self):
            for _ in range(self.bar.total):
                self.bar.add_progress(1)
                _time.sleep(1 / 60)
            self.quit()

    window = MyWindow()
    window.mainloop()


if __name__ == "__main__":
    pass
