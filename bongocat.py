import sys
import pygame
import numpy as np
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow


class TransparentOverlay(QMainWindow):
    def __init__(self, width=1200, height=400):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(200, 200, width, height)

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, width, height)

        # Init Pygame
        pygame.init()
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.clock = pygame.time.Clock()

        # Load Bongo Cat
        self.idle_img = pygame.image.load("bongo_idle.png")
        self.hit_img = pygame.image.load("bongo_hit.png")

        self.idle_img = pygame.transform.scale(self.idle_img, (300, 200))
        self.hit_img = pygame.transform.scale(self.hit_img, (300, 200))
        self.idle_img = pygame.transform.rotate(self.idle_img, 10)

        self.current_img = self.idle_img
        self.hit_timer = 0

        # Keyboard layout and rectangles
        self.key_layout = [
            ["ESC", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "BACKSPACE"],
            ["TAB", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
            ["CAPS", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "ENTER"],
            ["SHIFT", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "SHIFT"],
            ["CTRL", "WIN", "ALT", "SPACE", "ALTGR", "MENU", "CTRL"]
        ]
        self.special_width = {
            "SPACE": 6, "SHIFT": 2.5, "ENTER": 2.5, "BACKSPACE": 2.5,
            "TAB": 2, "CAPS": 2, "CTRL": 1.5, "WIN": 1.5, "ALT": 1.5, "ALTGR": 1.5, "MENU": 1.5, "ESC": 1.5
        }
        self.key_rects = self.generate_keys()

        # Track key presses
        self.pressed_keys = set()
        self.last_hit_rect = None

        # Dragging
        self.drag_pos = None

        # Start update loop
        self.timer = QTimer()
        self.timer.timeout.connect(self.render)
        self.timer.start(16)

    def generate_keys(self):
        font = pygame.font.SysFont("Arial", 16)
        key_w, key_h = 60, 40
        spacing = 5
        start_y = 180
        keys = []

        for row_i, row in enumerate(self.key_layout):
            x = 30
            y = start_y + row_i * (key_h + spacing)
            for key in row:
                width = int(key_w * self.special_width.get(key.upper(), 1))
                rect = pygame.Rect(x, y, width - 2, key_h)
                keys.append({'key': key.upper(), 'rect': rect, 'font': font})
                x += width + spacing
        return keys

    def render(self):
        dt = self.clock.tick(60)
        self.surface.fill((0, 0, 0, 0))  # Transparent

        # Draw keys
        for k in self.key_rects:
            color = (200, 100, 100, 180) if k['key'] in self.pressed_keys else (255, 255, 255, 180)
            pygame.draw.rect(self.surface, color, k['rect'], border_radius=5)
            pygame.draw.rect(self.surface, (0, 0, 0), k['rect'], 2, border_radius=5)
            label = k['font'].render(k['key'], True, (0, 0, 0))
            label_rect = label.get_rect(center=k['rect'].center)
            self.surface.blit(label, label_rect)

        # Draw Bongo Cat
        # Draw Bongo Cat
        if self.hit_timer > 0 and self.last_hit_rect:
            cat_x = self.last_hit_rect.centerx - self.hit_img.get_width() // 2
            cat_y = self.last_hit_rect.top - self.hit_img.get_height() + 10
            self.surface.blit(self.hit_img, (cat_x, cat_y))
            self.hit_timer -= dt
        else:
            center_x = self.width() // 2 - self.idle_img.get_width() // 2
            self.surface.blit(self.idle_img, (center_x, 10))


        self.update_label()

    def update_label(self):
        raw = pygame.image.tostring(self.surface, "RGBA", False)
        img = QImage(raw, self.surface.get_width(), self.surface.get_height(), QImage.Format_RGBA8888)
        self.label.setPixmap(QPixmap.fromImage(img))

    def keyPressEvent(self, event):
        key = event.text().upper()
        if key == ' ':
             key = 'SPACE'
        elif event.key() == Qt.Key_Backspace:
             key = 'BACKSPACE'
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
             key = 'ENTER'
        elif event.key() == Qt.Key_Shift:
            key = 'SHIFT'
        elif event.key() == Qt.Key_Control:
            key = 'CTRL'
        elif event.key() == Qt.Key_Tab:
            key = 'TAB'
        elif event.key() == Qt.Key_Escape:
            key = 'ESC'
        elif event.key() == Qt.Key_CapsLock:
            key = 'CAPS'
        elif event.key() == Qt.Key_Alt:
            key = 'ALT'
        elif event.key() == Qt.Key_Meta:
            key = 'WIN'

        self.pressed_keys.add(key)
        self.hit_timer = 150

    # Find the rect of the key that was hit
        for k in self.key_rects:
            if k['key'] == key:
                self.last_hit_rect = k['rect']
                break


    def keyReleaseEvent(self, event):
        key = event.text().upper()
        if key == ' ':
            key = 'SPACE'
        elif event.key() == Qt.Key_Backspace:
            key = 'BACKSPACE'
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            key = 'ENTER'
        elif event.key() == Qt.Key_Shift:
            key = 'SHIFT'
        elif event.key() == Qt.Key_Control:
            key = 'CTRL'
        elif event.key() == Qt.Key_Tab:
            key = 'TAB'
        elif event.key() == Qt.Key_Escape:
            key = 'ESC'
        elif event.key() == Qt.Key_CapsLock:
            key = 'CAPS'
        elif event.key() == Qt.Key_Alt:
            key = 'ALT'
        elif event.key() == Qt.Key_Meta:
            key = 'WIN'

        if key in self.pressed_keys:
            self.pressed_keys.remove(key)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self.drag_pos:
            self.move(event.globalPos() - self.drag_pos)

    def mouseReleaseEvent(self, event):
        self.drag_pos = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransparentOverlay()
    window.show()
    sys.exit(app.exec_())
