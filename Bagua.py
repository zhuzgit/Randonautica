import os
import json
import requests
import secrets
import time

# ==========================================
# 💾 离线古籍数据库路径
# ==========================================
JSON_FILE_PATH = "gua_matrix.json"

# ==========================================
# 基础易理梅花数位元映射表
# ==========================================
BAGUA_DATA = {
    0b000: {"name": "坤", "nature": "地", "direction": "西南方"},
    0b100: {"name": "震", "nature": "雷", "direction": "正东方"},
    0b010: {"name": "坎", "nature": "水", "direction": "正北方"},
    0b110: {"name": "兑", "nature": "泽", "direction": "正西方"},
    0b001: {"name": "艮", "nature": "山", "direction": "东北方"},
    0b101: {"name": "离", "nature": "火", "direction": "正南方"},
    0b011: {"name": "巽", "nature": "风", "direction": "东南方"},
    0b111: {"name": "乾", "nature": "天", "direction": "西北方"}
}

def load_local_matrix():
    """纯离线加载抓取上线的全息矩阵"""
    if not os.path.exists(JSON_FILE_PATH):
        raise FileNotFoundError(f"❌ [冷启动失败] 未在当前目录下找到古籍库 {JSON_FILE_PATH}！请先运行抓取程序。")
    
    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
        db = json.load(f)
        print(f"【系统校验】离线全息易理大库加载成功！包含 {len(db)} 门纯正古籍卦象。")
        return db

def fetch_quantum_source():
    """获取真随机信号（国内公网直连 ANU 量子实验室，超时1.2秒自动切换本地硬件热噪声）"""
    try:
        url = "https://qrng.anu.edu.au/API/jsonI.php?length=6&type=uint8"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        # ⚡ 纯直连，不加任何 proxies 参数，缩短超时以提升响应速度
        response = requests.get(url, headers=headers, timeout=1.2)
        if response.status_code == 200 and response.json().get("success"):
            print("【系统】[量子纠缠态] 公网直连成功，捕获澳大利亚国立大学真空零点能涨落！")
            return [x % 4 for x in response.json()["data"]]
    except:
        pass
    print("【系统】[硬件级自愈] 直连通道超时，自动切入本地主板芯片热噪声密码学安全物理硬随机源。")
    return [secrets.randbelow(4) for _ in range(6)]

def get_gua_by_bits(lower_bits, upper_bits, db):
    """通过位运算的二进制 ID 精准桥接古籍大库的命名键值"""
    lower_name = BAGUA_DATA[lower_bits]["name"]
    upper_name = BAGUA_DATA[upper_bits]["name"]
    
    fixed_names = {
        (0b111, 0b111): "乾为天", (0b000, 0b000): "坤为地", 
        (0b100, 0b010): "雷水解", (0b010, 0b100): "水雷屯",
        (0b111, 0b000): "天地否", (0b000, 0b111): "地天泰", 
        (0b010, 0b101): "水火既济", (0b101, 0b010): "火水未济"
    }
    
    gua_name = fixed_names.get((lower_bits, upper_bits), f"{BAGUA_DATA[upper_bits]['nature']}{BAGUA_DATA[lower_bits]['nature']}卦")
    
    if gua_name not in db:
        gua_name = next((k for k in db.keys() if lower_name in k and upper_name in k), list(db.keys())[0])
        
    return gua_name, db[gua_name]

def main():
    try:
        local_db = load_local_matrix()
    except Exception as e:
        print(e)
        return

    print("=" * 65)
    print("       RANDONAUTICA 量子引力场 · 文王六十四卦终极完全体系统       ")
    print("=" * 65)
    
    print("\n【第一步：意识意图校准（Intent Calibration）】")
    print("请在脑海中清晰默想你当下的困惑或目的地，正在将你的意识波长注入微观熵源...")
    time.sleep(0.5)  # 缩短无意义的等待时间，提升极客效率
        
    raw_signals = fetch_quantum_source()
    
    yaos = []
    print("\n【第二步：观测者干预（六爻自下而上坍缩）】")
    for idx, sig in enumerate(raw_signals):
        if sig == 0:   yaos.append((0, True, "—— —— ☯ [老阴·变爻]"))
        elif sig == 1: yaos.append((1, False, "————— ⚪ [少阳·静爻]"))
        elif sig == 2: yaos.append((0, False, "—— —— ⚪ [少阴·静爻]"))
        elif sig == 3: yaos.append((1, True, "————— ☯ [老阳·变爻]"))
        print(f"  第 {idx+1} 爻 (维度 {idx+1}): {yaos[-1][2]}")
        
    lower_bits = (yaos[2][0] << 2) | (yaos[1][0] << 1) | yaos[0][0]
    upper_bits = (yaos[5][0] << 2) | (yaos[4][0] << 1) | yaos[3][0]
    
    ben_gua, ben_data = get_gua_by_bits(lower_bits, upper_bits, local_db)
    
    # 变卦位运算推演
    changed_lower_bits, changed_upper_bits = lower_bits, upper_bits
    change_list = []
    
    for i in range(3):
        if yaos[i][1]:
            changed_lower_bits ^= (1 << i)
            change_list.append(i + 1)
    for i in range(3, 6):
        if yaos[i][1]:
            changed_upper_bits ^= (1 << (i - 3))
            change_list.append(i + 1)
            
    zhi_gua, _ = get_gua_by_bits(changed_lower_bits, changed_upper_bits, local_db)
    
    # ==========================================
    # 第三步：一体化正统古籍全息报告输出
    # ==========================================
    print("\n" + "═"*65)
    print(f" 🔮 【量子演化结论】 本卦：=== {ben_gua} === ──> 之卦（终局）：=== {zhi_gua} ===")
    print(f" 空间架构：外卦【{BAGUA_DATA[upper_bits]['name']}】({BAGUA_DATA[upper_bits]['nature']}) / 内卦【{BAGUA_DATA[lower_bits]['name']}】({BAGUA_DATA[lower_bits]['nature']})")
    print("═"*65)
    
    print(f" 🌟 【意图共振指数】：{ben_data['级别']}")
    print(f" 🗺️ 【Randonautica 时空坐标方位】（以当前所在地为中心点）：")
    print(f"     🟢 吸引力汇聚区（吉方）：前往 【{BAGUA_DATA[lower_bits]['direction']}】 寻找时空暗示")
    print(f"     🔴 能量波形斥力（忌方）：尽量避免前往 【{BAGUA_DATA[upper_bits]['direction']}】 做重大决策")
    print("-" * 65)
    
    print(f"【大象传·宇宙之律】\n ❖ {ben_data['大象']}\n")
    print(f"【历史正统总论】\n ❖ {ben_data['总论']}\n")
    
    print("【📊 现代场景四维分类解码】")
    for key, value in ben_data["维度解析"].items():
        print(f"   {key}: {value}")
    print("-" * 65)
    
    print("【时空维度交错：古籍原版动爻提示】")
    if not change_list:
        print(" ❖ 六爻皆静：本地量子场极度稳定。因果链无剧烈变量产生，请直接遵循【现代场景解码】核心建议稳妥执行。")
    else:
        print(f" ❖ 观测到 {len(change_list)} 个量子变动点（动爻），事物正沿历史轨迹发生质变：")
        for ch in change_list:
            raw_yao_ci = ben_data['爻辞'].get(str(ch), ben_data['爻辞'].get(ch, '【爻辞】经典记载，守正无咎。'))
            print(f"  👉 变位第 {ch} 爻：{raw_yao_ci}")
            
        print(f"\n【🔮 未来推演·因果坍缩终局】")
        print(f"  经二进制逆转推演，当前事件的能量波动最终会演化至【{zhi_gua}】。")
        print(f"  请对照古籍原文细细揣摩，有意识地调整你的‘意图’以修正未来轨迹。")
    print("═"*65)

if __name__ == "__main__":
    main()
    
    # ⚡ 核心改进点：在此处注入时空锁，阻止终端自动销毁
    print("\n" + "─" * 65)
    input("【系统悬停】因果波形已稳定。按下 [Enter] 回车键关闭赛博控制台...")