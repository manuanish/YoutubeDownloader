# ui_shadows.py

from main import *


main_window_shadow = QGraphicsDropShadowEffect()
main_window_shadow.setBlurRadius(20)
main_window_shadow.setXOffset(0)
main_window_shadow.setYOffset(0)
main_window_shadow.setColor(QColor(0, 0, 0, 100))

download_frame_shadow = QGraphicsDropShadowEffect()
download_frame_shadow.setBlurRadius(20)
download_frame_shadow.setXOffset(0)
download_frame_shadow.setYOffset(0)
download_frame_shadow.setColor(QColor(0, 0, 0, 100))

error_frame_shadow = QGraphicsDropShadowEffect()
error_frame_shadow.setBlurRadius(20)
error_frame_shadow.setXOffset(0)
error_frame_shadow.setYOffset(0)
error_frame_shadow.setColor(QColor(0, 0, 0, 100))