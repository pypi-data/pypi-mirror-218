from PyQt6.QtWidgets import QWidget


_old_widget_init = QWidget.__init__
widget_count = 0

def _widget_init(*args, **kwargs):
    global _old_widget_init, widget_count
    _old_widget_init(*args, **kwargs)
    widget_count += 1
    print(f'QWidget.__init__(): {widget_count} widget instances')

def _widget_del(self, *args, **kwargs):
    global widget_count
    widget_count -= 1
    print(f'QWidget.__del__(): {widget_count} widget instances')


QWidget.__init__ = _widget_init
QWidget.__del__ = _widget_del
