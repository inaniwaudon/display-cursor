import pyautogui
from screeninfo import get_monitors


class CursorController:
    def __init__(self):
        self.cursors = {}
        self.current_monitor = None

    # カーソルを指定した画面に移動
    def switch(self, target: int):
        if self.current_monitor == target:
            return
        current = 1 if target == 0 else 0

        self.memorize_monitor_pos(current)
        pos = self.get_monitor_pos(target)
        if pos is not None:
            pyautogui.moveTo(pos[0], pos[1])
            print(f"Switched to monitor: {target}")
        self.current_monitor = target

    # 配置すべきカーソル位置を取得
    def get_monitor_pos(self, index: int):
        monitors = get_monitors()
        if index >= len(monitors):
            return None
        
        if index in self.cursors:
            return self.cursors[index]
        
        # 初期位置は画面中央に
        monitor = monitors[index]
        x = monitor.x + monitor.width // 2
        y = monitor.y + monitor.height // 2
        return x, y

    # 現在のカーソル位置を記憶
    def memorize_monitor_pos(self, index: int):
        monitors = get_monitors()
        if index >= len(monitors):
            return
        
        # 画面内にカーソルがある場合のみ記録
        x, y = pyautogui.position()
        monitor = monitors[index]
        if (
            monitor.x <= x <= monitor.x + monitor.width and
            monitor.y <= y <= monitor.y + monitor.height
        ):
            self.cursors[index] = (x, y)
