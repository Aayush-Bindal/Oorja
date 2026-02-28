import os
import sys
import time
import tkinter as tk
import math
import random

# --- FIX: HARDCODE TCL/TK PATHS ---
base_path = r"C:\Users\abhin\AppData\Local\Programs\Python\Python313\tcl"
if os.path.exists(base_path):
    os.environ['TCL_LIBRARY'] = os.path.join(base_path, 'tcl8.6')
    os.environ['TK_LIBRARY'] = os.path.join(base_path, 'tk8.6')

class UltraTelemetry:
    def __init__(self, root):
        self.root = root
        self.root.title("NEXUS AI TELEMETRY")
        self.root.geometry("1000x600")
        self.root.configure(bg="#050a0d")

        self.canvas = tk.Canvas(self.root, bg="#050a0d", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Colors from your image
        self.color_cyan = "#00f2ff"
        self.color_cyan_glow = "#004a4d"
        self.color_orange = "#ff9100"
        self.color_orange_glow = "#4d2c00"
        self.color_dark_bg = "#0a1114"
        
        self.draw_ui()

    def draw_glow_arc(self, x, y, r, start, extent, color, glow_color, width):
        # Layer 1: The outer faint glow (widest)
        self.canvas.create_arc(x-r, y-r, x+r, y+r, start=start, extent=extent, 
                              style="arc", outline=glow_color, width=width+10)
        # Layer 2: The mid glow
        self.canvas.create_arc(x-r, y-r, x+r, y+r, start=start, extent=extent, 
                              style="arc", outline=glow_color, width=width+4)
        # Layer 3: The core bright line (thinnest)
        self.canvas.create_arc(x-r, y-r, x+r, y+r, start=start, extent=extent, 
                              style="arc", outline=color, width=width)

    def draw_ui(self):
        # 1. Main Speedometer (Fixed capstyle issue)
        # Background track
        self.canvas.create_arc(50, 80, 410, 440, start=-30, extent=240, 
                              style="arc", outline="#1a1a1a", width=18)
        
        # Speed Arc with Glow (88.2 km/h -> roughly 88% of 240 degrees)
        self.draw_glow_arc(230, 260, 180, 210, -210, self.color_cyan, self.color_cyan_glow, 12)

        # Speed Text
        self.canvas.create_text(230, 210, text="SPEED", fill=self.color_cyan, font=("Arial", 14, "bold"))
        self.canvas.create_text(230, 280, text="88.2", fill="white", font=("Arial", 72, "bold"))
        self.canvas.create_text(230, 350, text="km/h", fill="#777", font=("Arial", 16))

        # 2. Ticks (Mathematical placement)
        for i in range(11):
            angle = math.radians(210 - (i * 24))
            x_inner = 230 + 155 * math.cos(angle)
            y_inner = 260 - 155 * math.sin(angle)
            x_outer = 230 + 185 * math.cos(angle)
            y_outer = 260 - 185 * math.sin(angle)
            self.canvas.create_line(x_inner, y_inner, x_outer, y_outer, fill="white", width=2)
            
            # Numbers
            tx = 230 + 130 * math.cos(angle)
            ty = 260 - 130 * math.sin(angle)
            self.canvas.create_text(tx, ty, text=str(i*10), fill="#555", font=("Arial", 10))

        # 3. Power Bars (Right Side)
        self.draw_power_bar(750, 100, "Battery Voltage", "51.8 V", 0.8, ["#4dff00", "#ccff00"])
        self.draw_power_bar(750, 160, "Battery Current", "28.5 A", 0.5, ["#ff9100", "#ff4e00"])

    def draw_power_bar(self, x, y, label, value, percent, gradient):
        # Label & Value
        self.canvas.create_text(x, y, text=label, fill="white", anchor="w", font=("Arial", 10))
        self.canvas.create_text(x+200, y, text=value, fill=gradient[0], anchor="e", font=("Arial", 10, "bold"))
        
        # Bar Background
        self.canvas.create_rectangle(x, y+15, x+200, y+25, fill="#111", outline="#333")
        
        # Bar Fill (Simulating the gradient look with a simple color for now)
        self.canvas.create_rectangle(x, y+15, x+(200*percent), y+25, fill=gradient[0], outline="")

if __name__ == "__main__":
    root = tk.Tk()
    app = UltraTelemetry(root)
    root.mainloop()