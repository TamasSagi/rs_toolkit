import cv2
import sys
import win32con
import win32gui
import win32ui

import numpy as np

from scripts.base_screenshot_taker import ScreenshotTaker


class ScreenshotTaker_Windows(ScreenshotTaker):
    def __init__(self, window_name: str = "RuneScape") -> None:
        self.hwnd = win32gui.FindWindow(None, window_name)

        if self.hwnd == 0:
            sys.exit(f'Window "{window_name}" not found')

        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        self.h = bottom - top
        self.w = right - left
        self.offset_y = 31
        self.shape = (self.h, self.w, 4)
        self.border = (slice(31, -8), slice(8, -8), slice(0, 3))
        self.rgb = (slice(None, None, None), slice(None, None, None), slice(None, None, -1))

        # Create win32 magic variables to take screenshot
        self.window_handle_device_context = win32gui.GetWindowDC(self.hwnd)
        self.window_device_context = win32ui.CreateDCFromHandle(self.window_handle_device_context)
        self.compatible_dc = self.window_device_context.CreateCompatibleDC()
        self.bitmap = win32ui.CreateBitmap()
        self.bitmap.CreateCompatibleBitmap(self.window_device_context, self.w, self.h)
        self.compatible_dc.SelectObject(self.bitmap)

    def take_screenshot(self, debug: bool = False) -> None:
        self.compatible_dc.BitBlt((0, 0), (self.w, self.h), self.window_device_context, (0, 0), win32con.SRCCOPY)

        # Create a numpy array from the bitmap, convert from RGBA to RGB and remove "border" from the image
        self.frame = np.fromstring(self.bitmap.GetBitmapBits(True), np.uint8).reshape(self.shape)[self.border][self.rgb]

        if debug:
            cv2.imwrite("frame.png", self.frame)

    def __del__(self):
        # Free win32 magic variables
        self.window_device_context.DeleteDC()
        self.compatible_dc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, self.window_handle_device_context)
        win32gui.DeleteObject(self.bitmap.GetHandle())
