import tkinter as tk, threading, random, time, json
from datetime import datetime
from pathlib import Path

APP_TITLE = "SmartShield X — AI-Powered Firewall Monitor"
TAGLINE = "Detect Before It's Too Late"
RULES_PATH = Path("rules.json")

COLORS = {"Safe": "#00e6e6", "Suspicious": "#ffff66", "Critical": "#ff5555"}

def load_rules():
    if not RULES_PATH.exists():
        json.dump({"block_ips": [], "block_ports": [], "block_protocols": []},
                  open(RULES_PATH, "w"))
    return json.load(open(RULES_PATH))

# --- AI Risk Engine ---
def ai_assess_packet(ip, port, proto):
    score = 0
    # Port sensitivity
    if port in [21, 22, 23, 25, 3389]: score += 55
    elif port in [80, 443]: score += 25
    else: score += random.randint(5, 20)
    # Protocol factor
    if proto == "UDP": score += 15
    elif proto == "ICMP": score += 30
    # IP heuristics
    if not ip.startswith("192.168.") and not ip.startswith("10."):
        score += 10
    # Random noise to mimic adaptive learning
    score += random.randint(-10, 10)
    # Clamp score
    score = max(0, min(score, 100))
    # Classification
    if score < 40: lvl = "Safe"
    elif score < 70: lvl = "Suspicious"
    else: lvl = "Critical"
    return score, lvl

class SmartShieldX(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("1180x670")
        self.configure(bg="#05070a")
        self.running = False
        self.rules = load_rules()
        self.stats = {"Safe":0,"Suspicious":0,"Critical":0,"Packets":0}
        self.after(0, self.splash_screen)

    # --- Splash ---
    def splash_screen(self):
        splash = tk.Toplevel(self, bg="#05070a")
        splash.overrideredirect(True)
        w,h=500,240
        x=(self.winfo_screenwidth()-w)//2
        y=(self.winfo_screenheight()-h)//2
        splash.geometry(f"{w}x{h}+{x}+{y}")
        tk.Label(splash,text="SMARTSHIELD X",fg="#00e6e6",bg="#05070a",
                 font=("Segoe UI Semibold",28)).pack(expand=True)
        tk.Label(splash,text=TAGLINE,fg="#9be7ff",bg="#05070a",
                 font=("Segoe UI",12)).pack()
        splash.after(1800,lambda:(splash.destroy(),self.main_ui()))

    # --- Main UI ---
    def main_ui(self):
        tk.Label(self,text=APP_TITLE,fg="#00e6e6",bg="#05070a",
                 font=("Segoe UI",17,"bold")).pack(pady=(8,0))
        tk.Label(self,text=TAGLINE,fg="#a8eaff",bg="#05070a",
                 font=("Segoe UI",10)).pack(pady=(0,5))

        # Controls
        ctrl=tk.Frame(self,bg="#05070a"); ctrl.pack(pady=6)
        style={"font":("Segoe UI",10,"bold"),"fg":"#bff",
               "bg":"#0d141b","activebackground":"#18222d",
               "width":16,"bd":0}
        self.start_btn=tk.Button(ctrl,text="▶ Start Monitoring",
                                 command=self.start_monitor,**style)
        self.stop_btn=tk.Button(ctrl,text="⏸ Stop",
                                command=self.stop_monitor,**style)
        self.reset_btn=tk.Button(ctrl,text="🔁 Reset",
                                 command=self.reset_monitor,**style)
        self.start_btn.grid(row=0,column=0,padx=5)
        self.stop_btn.grid(row=0,column=1,padx=5)
        self.reset_btn.grid(row=0,column=2,padx=5)

        body=tk.Frame(self,bg="#05070a"); body.pack(fill=tk.BOTH,expand=True,padx=10,pady=5)

        # Left: console + mini-graph
        self.log_frame=tk.Frame(body,bg="#05070a")
        self.log_frame.pack(side=tk.LEFT,fill=tk.BOTH,expand=True,padx=(0,10))
        self.log_box=tk.Text(self.log_frame,bg="#05070a",fg="#bff",
                             font=("Consolas",10),relief="flat",wrap="none")
        self.log_box.pack(fill=tk.BOTH,expand=True)
        self.log_box.insert(tk.END,"[SmartShield X AI Console Ready]\n")

        # Right: glass stats
        self.glass=tk.Frame(body,bg="#111820",
                            highlightbackground="#00e6e6",highlightthickness=1)
        self.glass.pack(side=tk.RIGHT,fill=tk.BOTH)
        self.stats_box=tk.Label(self.glass,bg="#111820",fg="#00e6e6",
                                font=("Segoe UI",10),justify="left",anchor="nw")
        self.stats_box.place(relx=0.05,rely=0.05)
        tk.Label(self.glass,text="Live Stats",bg="#111820",fg="#bff",
                 font=("Segoe UI",11,"bold")).place(relx=0.05,rely=0.01)

        footer=tk.Label(self,text="Mode: AI Heuristic Simulation (3 Threat Levels)",
                        fg="#66ffff",bg="#05070a",font=("Segoe UI",9))
        footer.pack(side=tk.BOTTOM,pady=5)

        self.update_stats()
        self.start_monitor()

    # --- Controls ---
    def start_monitor(self):
        if not self.running:
            self.running=True
            self.log_box.insert(tk.END,"\n[AI Monitoring Started]\n")
            threading.Thread(target=self.simulate_traffic,daemon=True).start()

    def stop_monitor(self):
        self.running=False
        self.log_box.insert(tk.END,"[Monitoring Paused]\n")

    def reset_monitor(self):
        self.running=False
        self.log_box.delete("1.0",tk.END)
        self.log_box.insert(tk.END,"[SmartShield X Reset]\n")
        self.stats={"Safe":0,"Suspicious":0,"Critical":0,"Packets":0}

    # --- Simulation ---
    def simulate_traffic(self):
        while self.running:
            ip=f"192.168.{random.randint(0,255)}.{random.randint(1,254)}"
            port=random.choice([21,22,80,443,3389,random.randint(1000,9999)])
            proto=random.choice(["TCP","UDP","ICMP"])
            score,level=ai_assess_packet(ip,port,proto)
            self.stats[level]+=1; self.stats["Packets"]+=1
            log=f"{datetime.now().strftime('%H:%M:%S')} | {proto:<4} | {ip}:{port:<5} | Risk:{score:03d} → {level}"
            self.after(0,self.add_log,log,score,level)
            time.sleep(0.8)

    # --- Logs + graph ---
    def add_log(self,text,score,level):
        color=COLORS[level]
        self.log_box.insert(tk.END,text+"\n")
        self.log_box.tag_add(level,"end-2l linestart","end-2l lineend")
        self.log_box.tag_config(level,foreground=color)
        # Draw tiny bar
        self.log_box.window_create(tk.END, window=self.make_bar(score,color))
        self.log_box.insert(tk.END,"\n")
        self.log_box.see(tk.END)

    def make_bar(self,score,color):
        frame=tk.Frame(self.log_box,bg="#05070a")
        canvas=tk.Canvas(frame,width=100,height=8,bg="#222831",highlightthickness=0)
        canvas.pack()
        canvas.create_rectangle(0,0,score,8,fill=color,width=0)
        return frame

    # --- Stats ---
    def update_stats(self):
        s=self.stats
        text=(f"Packets : {s['Packets']}\n"
              f"Safe : {s['Safe']}\n"
              f"Suspicious : {s['Suspicious']}\n"
              f"Critical : {s['Critical']}")
        self.stats_box.config(text=text)
        self.after(600,self.update_stats)

if __name__=="__main__":
    SmartShieldX().mainloop()
