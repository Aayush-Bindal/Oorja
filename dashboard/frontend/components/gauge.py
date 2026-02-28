import math
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QPolygonF, QRadialGradient, QBrush, QFont, QConicalGradient
from PyQt6.QtCore import Qt, QPointF, QRectF

class AnalogueGauge(QWidget):
    def __init__(self, title="GAUGE", min_val=0, max_val=100, units=""):
        super().__init__()
        self.title = title
        self.min_val = min_val
        self.max_val = max_val
        self.units = units
        self.current_value = min_val
        
        # Design Config
        self.accent_color = QColor(0, 200, 255)  # Cyan/Blue
        self.warning_color = QColor(255, 50, 50) # Red
        self.text_color = QColor(220, 220, 220)  # Off-white
        
        self.setMinimumSize(250, 250)

    def update_value(self, value):
        # Clamp value
        self.current_value = max(self.min_val, min(value, self.max_val))
        self.update()  # Triggers paintEvent
    def draw_progress_arc(self, painter):
        start_angle = -225 * 16
        sweep_angle = -270 * 16  # clockwise

        pct = (self.current_value - self.min_val) / (self.max_val - self.min_val)
        pct = max(0.0, min(1.0, pct))

        rect = QRectF(-85, -85, 170, 170)

        pen = QPen(self.accent_color, 12)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        painter.drawArc(rect, start_angle, int(sweep_angle * pct))
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        painter.translate(w / 2, h / 2)
        side = min(w, h)
        painter.scale(side / 200, side / 200)

        self.draw_face(painter)
        self.draw_progress_arc(painter)   
        self.draw_ticks_and_labels(painter)
        self.draw_needle(painter)
        self.draw_digital_readout(painter)
        self.draw_glass_reflection(painter)

    def draw_face(self, painter):
        # Dark Background Gradient
        grad = QRadialGradient(0, 0, 100)
        grad.setColorAt(0.0, QColor(40, 40, 45))
        grad.setColorAt(1.0, QColor(10, 10, 15))
        painter.setBrush(QBrush(grad))
        painter.setPen(QPen(QColor(60, 60, 65), 2))
        painter.drawEllipse(-95, -95, 190, 190)
        pen = QPen(QColor(0, 220, 255, 60), 6)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(-92, -92, 184, 184)
    def draw_ticks_and_labels(self, painter):
        start_angle = 135
        end_angle = 405
        total_angle = end_angle - start_angle

        val_range = self.max_val - self.min_val

        # Number of labeled ticks (EXACT numbers only)
        steps = 10
        step_value = val_range / steps

        painter.setFont(QFont("Arial", 8, QFont.Weight.Bold))

        for i in range(steps + 1):
            val = self.min_val + i * step_value
            pct = i / steps
            angle_deg = start_angle + pct * total_angle

            # ---- DRAW TICK ----
            painter.save()
            painter.rotate(angle_deg + 90)

            is_redline = val >= self.max_val * 0.8
            tick_color = self.warning_color if is_redline else QColor(160, 160, 160)

            painter.setPen(QPen(tick_color, 2))
            painter.drawLine(0, -85, 0, -95)
            painter.restore()

            # ---- DRAW NUMBER (ONLY THESE TICKS EXIST) ----
            angle_rad = math.radians(angle_deg + 90)
            radius = 70

            x = radius * math.cos(angle_rad)
            y = radius * math.sin(angle_rad)

            painter.setPen(self.text_color)
            rect = QRectF(x - 15, y - 10, 30, 20)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, f"{int(val)}")
            start_angle = -225  
            sweep_angle = 270

            step = 10
            steps = int((self.max_val - self.min_val) / step)

            painter.setFont(QFont("Arial", 9, QFont.Weight.Bold))

            for i in range(steps + 1):
                val = self.min_val + i * step
                pct = i / steps
                angle = start_angle + pct * sweep_angle

                # ---------- TICKS ----------
                painter.save()
                painter.rotate(angle)

                is_red = val >= 70
                tick_color = QColor(255, 60, 60) if is_red else QColor(180, 180, 180)

                painter.setPen(QPen(tick_color, 3))
                painter.drawLine(0, -82, 0, -95)
                painter.restore()

                # ---------- LABELS ----------
                angle_rad = math.radians(angle)
                radius = 68

                x = radius * math.cos(angle_rad)
                y = radius * math.sin(angle_rad)

                painter.setPen(QColor(230, 230, 230))
                painter.drawText(
                    QRectF(x - 16, y - 12, 32, 24),
                    Qt.AlignmentFlag.AlignCenter,
                    str(val)
                )
            start_angle = -225        # degrees
            sweep_angle = 270         # degrees

            step = 10
            steps = int((self.max_val - self.min_val) / step)

            painter.setFont(QFont("Arial", 9, QFont.Weight.Bold))

        for i in range(steps + 1):
            val = self.min_val + i * step
            pct = i / steps
            angle = start_angle + pct * sweep_angle

            painter.save()
            painter.rotate(angle)

            # Major tick every 10
            is_redline = val >= 100
            tick_color = QColor(255, 60, 60) if is_redline else QColor(180, 180, 180)

            painter.setPen(QPen(tick_color, 3))
            painter.drawLine(0, -82, 0, -95)
            painter.restore()

            # --- Label positioning ---
            angle_rad = math.radians(angle)
            radius = 68
            x = radius * math.cos(angle_rad)
            y = radius * math.sin(angle_rad)

            painter.setPen(QColor(220, 220, 220))
            painter.drawText(
                QRectF(x - 18, y - 12, 36, 24),
                Qt.AlignmentFlag.AlignCenter,
                str(val)
            )
    def draw_needle(self, painter):
        painter.save()

        # Map current value to angle
        val_range = self.max_val - self.min_val
        if val_range == 0: val_range = 1 # Prevent div/0
        
        pct = (self.current_value - self.min_val) / val_range
        angle = -225 + (pct * 270) # Map 0..1 to -225..45 degrees

        painter.rotate(angle)

        # Dynamic Color: Turn red if near max
        is_warning = pct > 0.8
        color = self.warning_color if is_warning else self.accent_color

        painter.setBrush(color)
        painter.setPen(Qt.PenStyle.NoPen)

        # Needle Shape
        needle = QPolygonF([
            QPointF(-3, 0),    # Base Left
            QPointF(0, -85),   # Tip
            QPointF(3, 0)      # Base Right
        ])
        painter.drawPolygon(needle)
        
        painter.restore()
        
        # Draw Center Cap (Pivot)
        painter.setBrush(QColor(30, 30, 30))
        painter.setPen(QPen(QColor(60, 60, 60), 1))
        painter.drawEllipse(-8, -8, 16, 16)

    def draw_digital_readout(self, painter):
        # SPEED VALUE
        painter.setPen(QColor(230, 255, 255))
        painter.setFont(QFont("Orbitron", 22, QFont.Weight.Bold))
        painter.drawText(QRectF(-60, -10, 120, 40),
                        Qt.AlignmentFlag.AlignCenter,
                        f"{self.current_value:.1f}")

        # UNITS
        painter.setFont(QFont("Orbitron", 10))
        painter.setPen(QColor(120, 200, 200))
        painter.drawText(QRectF(-60, 30, 120, 20),
                        Qt.AlignmentFlag.AlignCenter,
                        self.units)

    def draw_glass_reflection(self, painter):
        # Adds a subtle "shine" to the top half to simulate glass
        grad = QConicalGradient(0, 0, -45)
        grad.setColorAt(0.0, QColor(255, 255, 255, 0))
        grad.setColorAt(0.1, QColor(255, 255, 255, 15)) # Slight glare
        grad.setColorAt(0.2, QColor(255, 255, 255, 0))
        
        painter.setBrush(QBrush(grad))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(-90, -90, 180, 180)