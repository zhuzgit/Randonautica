import tkinter as tk
from tkinter import font
import math
import requests
import secrets
import webbrowser
import threading
import time

# ==========================================
# 探索半径配置 (单位：米)
# ==========================================
RADIUS = 2000 

def fetch_dynamic_anchor():
    """
    通过底层网络出口 IP 逆向推算当前设备的物理坐标。
    """
    try:
        # 使用 ipapi 开放接口探测当前公网 IP 的物理位置
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get('https://ipapi.co/json/', headers=headers, timeout=4)
        data = response.json()
        
        lat = data.get('latitude')
        lon = data.get('longitude')
        city = data.get('city', '未知城市')
        region = data.get('region', '未知区域')
        
        if lat and lon:
            return float(lat), float(lon), f"{region} {city}"
            
    except Exception:
        # 代理拦截或超时，默默降级
        pass
        
    # 如果一切探测失败，回退到系统默认的最后已知安全坐标（深圳南山）
    return 22.5333, 113.9300, "网络遮蔽 (默认节点:深圳)"

class RandoQApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RANDO-Q | 量子游侠")
        # 调整窗口高度以容纳动态位置信息
        self.root.geometry("380x640")
        self.root.configure(bg="#0B0F19")
        self.root.resizable(False, False)
        
        self.is_computing = False
        self.pulse_state = 0
        self.pulse_direction = 1

        # 启动时动态捕获当前宇宙锚点
        self.START_LAT, self.START_LON, self.location_name = fetch_dynamic_anchor()

        self.setup_ui()
        self.animate_core()

    def setup_ui(self):
        # 1. 顶部标题
        title_font = font.Font(family="Helvetica", size=24, weight="bold")
        sub_font = font.Font(family="Helvetica", size=10)
        
        tk.Label(self.root, text="RANDO-Q", font=title_font, fg="#38BDF8", bg="#0B0F19", pady=20).pack()
        tk.Label(self.root, text="真·随机物理网格探测", font=sub_font, fg="#64748B", bg="#0B0F19").pack()

        # 2. 量子核心动画区 (Canvas)
        self.canvas = tk.Canvas(self.root, width=200, height=200, bg="#0B0F19", highlightthickness=0)
        self.canvas.pack(pady=20)
        # 绘制外圈和内核心
        self.outer_circle = self.canvas.create_oval(20, 20, 180, 180, outline="#38BDF8", width=1)
        self.inner_circle = self.canvas.create_oval(60, 60, 140, 140, fill="#818CF8", outline="")

        # 3. 信息面板
        self.info_frame = tk.Frame(self.root, bg="#1E293B", bd=0, padx=20, pady=15)
        self.info_frame.pack(fill="x", padx=30, pady=10)
        
        # 物理锚点行
        tk.Label(self.info_frame, text="物理空间锚点 :", fg="#94A3B8", bg="#1E293B", font=("Helvetica", 9)).grid(row=0, column=0, sticky="w", pady=5)
        tk.Label(self.info_frame, text=self.location_name, fg="#E2E8F0", bg="#1E293B", font=("Helvetica", 9)).grid(row=0, column=1, sticky="e", pady=5)

        # 状态行
        self.status_var = tk.StringVar(value="系统静默待命中")
        tk.Label(self.info_frame, text="当前系统状态 :", fg="#94A3B8", bg="#1E293B", font=("Helvetica", 9)).grid(row=1, column=0, sticky="w", pady=5)
        tk.Label(self.info_frame, textvariable=self.status_var, fg="#F8FAFC", bg="#1E293B", font=("Helvetica", 9)).grid(row=1, column=1, sticky="e", pady=5)
        
        # 数据源行
        self.source_var = tk.StringVar(value="-")
        tk.Label(self.info_frame, text="数据熵源接入 :", fg="#94A3B8", bg="#1E293B", font=("Helvetica", 9)).grid(row=2, column=0, sticky="w", pady=5)
        self.source_label = tk.Label(self.info_frame, textvariable=self.source_var, fg="#34D399", bg="#1E293B", font=("Helvetica", 9, "bold"))
        self.source_label.grid(row=2, column=1, sticky="e", pady=5)
        
        # 强制两列拉伸对齐
        self.info_frame.columnconfigure(1, weight=1)

        # 4. 触发按钮
        self.btn = tk.Button(
            self.root, 
            text="开启坍缩 | 生成盲点", 
            font=("Helvetica", 12, "bold"), 
            fg="white", 
            bg="#0284C7", 
            activebackground="#4F46E5", 
            activeforeground="white",
            relief="flat",
            command=self.start_collapse
        )
        self.btn.pack(fill="x", padx=40, pady=20, ipady=8)

    def animate_core(self):
        """利用 Canvas 实现量子核心的呼吸脉冲动画"""
        if self.is_computing:
            step = 4
            max_size = 30
        else:
            step = 1
            max_size = 10

        self.pulse_state += step * self.pulse_direction
        if self.pulse_state >= max_size or self.pulse_state <= 0:
            self.pulse_direction *= -1

        offset = self.pulse_state
        self.canvas.coords(self.outer_circle, 20 - offset, 20 - offset, 180 + offset, 180 + offset)