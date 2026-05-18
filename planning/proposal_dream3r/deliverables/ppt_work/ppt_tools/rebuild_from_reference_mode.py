from pathlib import Path
import shutil

import win32com.client
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(r"E:\kykt\Dream\planning\proposal_dream3r")
WORK = ROOT / "deliverables" / "ppt_work"
REF = Path(r"E:\Work\HSY\气动系统泄漏检测迁移学习.pptx")
OUT = WORK / "proposal_dream3r_opening_report_reference_mode_v21.pptx"
PREVIEW = WORK / "previews_reference_mode_v21"
CONTACT = WORK / "contact_sheet_reference_mode_v21.png"
AI = ROOT / "ppt_assets" / "ai"
ASSETS = WORK / "reference_mode_assets"
FIGS = Path(r"E:\kykt\Dream\3R-mix\figures")


SLIDE_SOURCES = [1, 2, 3, 4, 5, 5, 10, 10, 10, 10, 10, 5, 10, 10, 10, 8, 10, 5, 10, 10, 5, 7, 5, 12]

TITLES = [
    "",
    "汇报提纲",
    "三维重建与 3R 模型的兴起",
    "3R 模型的优势",
    "3R 模型面临的共性缺陷",
    "设计思路：学习与补足",
    "设计目标与课题两条主线",
    "总体架构一览",
    "空间记忆模块",
    "几何校验模块",
    "多专家编排模块",
    "当前实现进展",
    "为什么需要一个聚合平台",
    "平台核心功能",
    "技术架构",
    "已接入模型与实测数据",
    "后续更新方向与应用场景",
    "平台如何支撑架构研究",
    "实验设计",
    "创新点总结",
    "已完成工作",
    "时间安排",
    "风险与应对",
    "",
]


def rgb(r, g, b):
    return r + g * 256 + b * 65536


BLUE = rgb(0, 70, 142)
DARK_BLUE = rgb(0, 40, 95)
MID_BLUE = rgb(40, 111, 185)
LIGHT_BLUE = rgb(232, 242, 251)
GRAY = rgb(245, 247, 250)
LINE = rgb(70, 120, 180)
ORANGE = rgb(235, 138, 46)
TEXT = rgb(8, 24, 48)
WHITE = rgb(255, 255, 255)


def make_assets():
    ASSETS.mkdir(parents=True, exist_ok=True)
    font_path = next((p for p in [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simsun.ttc"] if Path(p).exists()), None)
    f_title = ImageFont.truetype(font_path, 34) if font_path else ImageFont.load_default()
    f_head = ImageFont.truetype(font_path, 24) if font_path else ImageFont.load_default()
    f_body = ImageFont.truetype(font_path, 20) if font_path else ImageFont.load_default()

    # Coverage matrix, simplified to stay readable in the reference deck style.
    im = Image.new("RGB", (1400, 760), "white")
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 1400, 70), fill=(0, 83, 155))
    d.text((40, 18), "F3 四轴覆盖矩阵（精简）", font=f_title, fill="white")
    rows = [
        ("几何校验", "absent", "作为候选架构重点补足"),
        ("长序列内存", "first-class", "保留显式对照实验"),
        ("多专家组合", "partial", "从孤立比较转为组合机制"),
        ("动态场景", "partial", "作为扩展场景验证"),
        ("统一平台", "absent", "支柱 B 的直接动机"),
        ("测试时机制", "partial", "作为后续可接入分支"),
    ]
    x0, y0 = 60, 120
    widths = [360, 260, 620]
    headers = ["能力维度", "覆盖状态", "对本研究的启示"]
    for j, h in enumerate(headers):
        x = x0 + sum(widths[:j])
        d.rectangle((x, y0, x + widths[j], y0 + 55), fill=(232, 242, 251), outline=(70, 120, 180), width=2)
        d.text((x + 20, y0 + 15), h, font=f_head, fill=(0, 83, 155))
    colors = {"first-class": (64, 158, 105), "partial": (235, 138, 46), "absent": (205, 80, 70)}
    for i, row in enumerate(rows):
        y = y0 + 55 + i * 72
        for j, val in enumerate(row):
            x = x0 + sum(widths[:j])
            d.rectangle((x, y, x + widths[j], y + 72), fill="white", outline=(185, 210, 230), width=1)
            if j == 1:
                d.rounded_rectangle((x + 28, y + 18, x + 200, y + 52), radius=8, fill=colors[val])
                d.text((x + 48, y + 23), val, font=f_body, fill="white")
            else:
                d.text((x + 20, y + 22), val, font=f_body, fill=(35, 50, 75))
    d.text((60, 675), "结论：能力覆盖分布不均，研究目标是建立可对照、可复用的评测入口。", font=f_head, fill=(0, 83, 155))
    im.save(ASSETS / "coverage_matrix.png")

    # Timing bar chart.
    vals = [("Spann3R", 24.8), ("CUT3R", 26.2), ("Fast3R", 28.5), ("DUSt3R", 91.2), ("MASt3R", 95.0), ("MonST3R", 223.3)]
    im = Image.new("RGB", (1400, 760), "white")
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 1400, 70), fill=(0, 83, 155))
    d.text((40, 18), "F11 跨模型推理耗时（秒）", font=f_title, fill="white")
    max_v = max(v for _, v in vals)
    y = 135
    for name, val in vals:
        d.text((95, y + 8), name, font=f_head, fill=(35, 50, 75))
        w = int(880 * val / max_v)
        color = (235, 138, 46) if name == "MonST3R" else (64, 120, 180)
        d.rounded_rectangle((330, y, 330 + w, y + 36), radius=8, fill=color)
        d.text((330 + w + 20, y + 4), f"{val:.1f}s", font=f_head, fill=(35, 50, 75))
        y += 82
    d.text((95, 680), "结论：耗时差异用于调度与实验管理，不直接等同于模型质量排序。", font=f_head, fill=(0, 83, 155))
    im.save(ASSETS / "timing_bars.png")

    # Gantt-style timeline for the research plan.
    im = Image.new("RGB", (1400, 760), "white")
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, 1400, 70), fill=(0, 83, 155))
    d.text((40, 18), "F16 后续研究计划（M1-M8）", font=f_title, fill="white")
    left, top = 210, 145
    cell_w, row_h = 125, 74
    months = [f"M{i}" for i in range(1, 9)]
    for i, m in enumerate(months):
        x = left + i * cell_w
        d.rectangle((x, top - 45, x + cell_w, top), fill=(232, 242, 251), outline=(185, 210, 230))
        d.text((x + 42, top - 34), m, font=f_body, fill=(0, 83, 155))
    tasks = [
        ("基线复现与合同补齐", 1, 2, (64, 120, 180)),
        ("校验标定与模块消融", 2, 5, (235, 138, 46)),
        ("长序列与多专家评测", 4, 7, (64, 158, 105)),
        ("平台对比视图与报告", 2, 6, (86, 132, 191)),
        ("论文整理与系统固化", 7, 8, (45, 88, 145)),
    ]
    for r, (name, start, end, color) in enumerate(tasks):
        y = top + r * row_h
        d.text((42, y + 18), name, font=f_head, fill=(35, 50, 75))
        for i in range(8):
            x = left + i * cell_w
            d.rectangle((x, y, x + cell_w, y + row_h - 10), outline=(225, 232, 240))
        x1 = left + (start - 1) * cell_w + 16
        x2 = left + end * cell_w - 16
        d.rounded_rectangle((x1, y + 18, x2, y + 44), radius=10, fill=color)
    d.text((42, 675), "说明：时间表为候选安排，受算力授权、导师反馈和阶段评测结果影响。", font=f_head, fill=(0, 83, 155))
    im.save(ASSETS / "timeline_gantt.png")


def shape_text(shape):
    try:
        if shape.HasTextFrame and shape.TextFrame.HasText:
            return shape.TextFrame.TextRange.Text.strip()
    except Exception:
        return ""
    return ""


def set_title(slide, title):
    if not title:
        return
    candidates = []
    for s in slide.Shapes:
        t = shape_text(s)
        if t:
            try:
                if s.Top < 80 and s.Left < 760:
                    candidates.append(s)
            except Exception:
                pass
    candidates.sort(key=lambda s: (s.Top, s.Left))
    for s in candidates:
        try:
            if s.Width > 220 and "北京航空航天大学" not in shape_text(s):
                s.TextFrame.TextRange.Text = title
                s.TextFrame.TextRange.Font.Name = "Microsoft YaHei"
                s.TextFrame.TextRange.Font.Size = 31
                s.TextFrame.TextRange.Font.Bold = -1
                s.TextFrame.TextRange.Font.Color.RGB = DARK_BLUE
                return
        except Exception:
            pass


def clear_body(slide):
    doomed = []
    for s in slide.Shapes:
        try:
            if s.Top > 88:
                doomed.append(s)
        except Exception:
            pass
    for s in doomed:
        try:
            s.Delete()
        except Exception:
            pass


def add_box(slide, x, y, w, h, text="", fill=WHITE, line=LINE, font=20, bold=False, color=TEXT, align=1):
    shp = slide.Shapes.AddShape(1, x, y, w, h)
    shp.Fill.ForeColor.RGB = fill
    shp.Line.ForeColor.RGB = line
    shp.Line.Weight = 1
    if text:
        tr = shp.TextFrame.TextRange
        tr.Text = text
        tr.Font.Name = "Microsoft YaHei"
        tr.Font.Size = font
        tr.Font.Bold = -1 if bold else 0
        tr.Font.Color.RGB = color
        shp.TextFrame.MarginLeft = 8
        shp.TextFrame.MarginRight = 8
        shp.TextFrame.MarginTop = 6
        shp.TextFrame.MarginBottom = 4
        tr.ParagraphFormat.Alignment = align
    return shp


def add_bar(slide, text, y=92):
    return add_box(slide, 34, y, 890, 40, text, fill=BLUE, line=BLUE, font=20, bold=True, color=WHITE, align=2)


def add_label(slide, x, y, w, h, text):
    return add_box(slide, x, y, w, h, text, fill=BLUE, line=BLUE, font=20, bold=True, color=WHITE, align=2)


def add_picture(slide, path, x, y, w, h):
    path = Path(path)
    if not path.exists():
        add_box(slide, x, y, w, h, f"待补充：{path.name}", fill=GRAY, line=LINE, font=16, color=TEXT, align=2)
        return
    im = Image.open(path)
    iw, ih = im.size
    scale = min(w / iw, h / ih)
    nw, nh = iw * scale, ih * scale
    slide.Shapes.AddPicture(str(path), False, True, x + (w - nw) / 2, y + (h - nh) / 2, nw, nh)


def add_arrow(slide, x, y, w=36, h=22):
    shp = slide.Shapes.AddShape(33, x, y, w, h)
    shp.Fill.ForeColor.RGB = MID_BLUE
    shp.Line.ForeColor.RGB = MID_BLUE
    return shp


def bullets(slide, x, y, w, items, head=None):
    if head:
        add_label(slide, x, y, w, 30, head)
        y += 34
    for it in items:
        add_box(slide, x, y, w, 42, it, fill=WHITE, line=LINE, font=15, color=TEXT)
        y += 48


def big_card(slide, x, y, w, h, head, body, accent=BLUE):
    add_box(slide, x, y, w, 34, head, fill=accent, line=accent, font=19, bold=True, color=WHITE, align=2)
    return add_box(slide, x, y + 36, w, h - 36, body, fill=WHITE, line=accent, font=19, color=TEXT, align=2)


def slide_cover(slide):
    for s in slide.Shapes:
        if not shape_text(s):
            continue
        try:
            if s.Top < 45 and s.Width > 300:
                s.TextFrame.TextRange.Text = "开题报告"
            elif 90 < s.Top < 260 and s.Width > 500:
                tr = s.TextFrame.TextRange
                tr.Text = "面向前馈式三维重建的\n新型架构设计与聚合管理平台"
                tr.Font.Size = 40
            elif 330 < s.Top < 380 and s.Left < 430:
                s.TextFrame.TextRange.Text = "汇报人"
            elif 330 < s.Top < 380 and s.Left >= 430:
                tr = s.TextFrame.TextRange
                tr.Text = "崔昊喆  纪博闻"
                tr.Font.Size = 24
            elif s.Top > 390:
                s.TextFrame.TextRange.Text = "2026春科研课堂"
            else:
                s.TextFrame.TextRange.Text = ""
        except Exception:
            pass


AGENDA_ITEMS = ["研究背景", "架构设计", "软件平台", "实验计划与总结"]


def clear_agenda_content(slide):
    doomed = []
    for s in slide.Shapes:
        try:
            # Preserve the copied background images and left blue field, rebuild only the agenda widgets.
            if s.Top > 80 and s.Left > 300:
                doomed.append(s)
            elif s.Top > 80 and 80 < s.Left < 230:
                doomed.append(s)
        except Exception:
            pass
    for s in doomed:
        try:
            s.Delete()
        except Exception:
            pass


def agenda_page(slide, active=None):
    clear_agenda_content(slide)
    # Right grey panel, matching the reference outline page.
    panel = slide.Shapes.AddShape(1, 292, 96, 570, 400)
    panel.Fill.ForeColor.RGB = rgb(235, 236, 238)
    try:
        panel.Fill.Transparency = 0.08
    except Exception:
        pass
    panel.Line.ForeColor.RGB = rgb(230, 230, 230)
    panel.Shadow.Visible = -1
    try:
        panel.Shadow.Transparency = 0.55
        panel.Shadow.Blur = 8
    except Exception:
        pass

    # Vertical title on the left blue area.
    v = slide.Shapes.AddTextbox(1, 120, 205, 75, 210)
    tr = v.TextFrame.TextRange
    tr.Text = "汇\n报\n提\n纲"
    tr.Font.Name = "Microsoft YaHei"
    tr.Font.Size = 30
    tr.Font.Bold = -1
    tr.Font.Color.RGB = WHITE
    tr.ParagraphFormat.Alignment = 2
    line = slide.Shapes.AddLine(112, 250, 112, 450)
    line.Line.ForeColor.RGB = rgb(210, 225, 245)
    try:
        line.Line.Transparency = 0.35
    except Exception:
        pass

    y0 = 112
    for i, item in enumerate(AGENDA_ITEMS, 1):
        y = y0 + (i - 1) * 73
        is_active = active == i
        fill = BLUE if is_active else WHITE
        text_color = WHITE if is_active else rgb(190, 190, 190)
        border = BLUE if is_active else rgb(220, 220, 220)
        add_box(slide, 365, y, 460, 58, "", fill=fill, line=border)
        n = slide.Shapes.AddTextbox(1, 405, y + 7, 70, 44)
        nt = n.TextFrame.TextRange
        nt.Text = f"{i:02d}"
        nt.Font.Name = "Microsoft YaHei"
        nt.Font.Size = 27
        nt.Font.Bold = -1
        nt.Font.Color.RGB = text_color
        nt.ParagraphFormat.Alignment = 2
        div = slide.Shapes.AddLine(486, y + 12, 486, y + 46)
        div.Line.ForeColor.RGB = WHITE if is_active else rgb(210, 210, 210)
        title = slide.Shapes.AddTextbox(1, 510, y + 9, 280, 42)
        tt = title.TextFrame.TextRange
        tt.Text = item
        tt.Font.Name = "Microsoft YaHei"
        tt.Font.Size = 25
        tt.Font.Bold = -1
        tt.Font.Color.RGB = text_color


def slide_outline(slide):
    agenda_page(slide, active=1)


def section_slide(slide, no, title, items):
    agenda_page(slide, active=int(no))


def build_slide(slide, idx):
    clear_body(slide)
    add_box(slide, 0, 130, 960, 410, "", fill=WHITE, line=WHITE)
    if idx == 3:
        add_bar(slide, "DUSt3R 将未标定图像对直接映射为稠密三维点图，是 3R 路线的代表起点。")
        big_card(slide, 60, 165, 250, 185, "传统三维重建", "特征提取\n特征匹配\n位姿估计\n三角化与稠密重建", accent=BLUE)
        add_arrow(slide, 325, 235, 40, 24)
        add_picture(slide, FIGS / "dust3r_fig1.png", 390, 148, 500, 235)
        add_box(slide, 85, 435, 790, 38, "3R 的价值在于统一输入输出；后续问题集中转向长序列、动态场景和结果可靠性。", fill=LIGHT_BLUE, line=LINE, font=17, bold=True, color=DARK_BLUE, align=2)
    elif idx == 4:
        add_bar(slide, "3R 模型的优势集中在速度、端到端学习、统一输出和特色机制。")
        cards = [
            ("速度快", "单次前向\n无需迭代优化"),
            ("端到端学习", "几何先验\n隐式写入权重"),
            ("统一输出", "pointmap 支持\n深度 / 位姿 / 法线"),
            ("特色机制", "记忆、递推\n校验、匹配增强"),
        ]
        for i, (h, b) in enumerate(cards):
            big_card(slide, 60 + i * 220, 165, 180, 150, h, b, accent=BLUE if i in (0, 3) else MID_BLUE)
        add_box(slide, 90, 380, 780, 52, "Spann3R、CUT3R、Test3R、MASt3R 等工作提供了可借鉴的机制来源。", fill=LIGHT_BLUE, line=LINE, font=19, bold=True, color=DARK_BLUE, align=2)
    elif idx == 5:
        add_bar(slide, "现有 3R 模型在长序列、动态场景、自检查和多模型协同方面仍有短板。")
        rows = [
            ("长序列漂移", "视频长度增加后几何逐渐跑偏"),
            ("动态场景干扰", "移动物体破坏静态重建假设"),
            ("缺乏自检查", "结果错误难以及时发现和修复"),
            ("单模型上限", "弱纹理、镜面、快速运动各有短板"),
            ("模型之间孤立", "缺少统一对比与组合框架"),
        ]
        for i, (h, b) in enumerate(rows):
            y = 145 + i * 55
            add_label(slide, 75, y, 165, 40, h)
            add_box(slide, 260, y, 620, 40, b, fill=WHITE if i % 2 == 0 else LIGHT_BLUE, line=LINE, font=17, color=DARK_BLUE, align=2)
        add_box(slide, 110, 435, 740, 38, "课题目标由这些短板自然引出：记忆、校验、多专家编排和统一平台。", fill=BLUE, line=BLUE, font=17, bold=True, color=WHITE, align=2)
    elif idx == 6:
        add_bar(slide, "设计思路分为两步：提取 3R 有效机制，再引入新方法补足短板。")
        big_card(slide, 55, 160, 390, 185, "从 3R 中学习", "空间记忆：保留已见区域\n流式递推：支持长视频\n几何校验：推理时自检查\n多模型互补：专家各取所长", accent=BLUE)
        add_arrow(slide, 465, 230, 42, 26)
        big_card(slide, 525, 160, 390, 185, "用新方法补足", "稀疏注意力：管理长序列\nMamba：线性复杂度递推\nSlot Attention：动静分离\n能力描述符：多专家路由", accent=MID_BLUE)
        add_box(slide, 95, 405, 770, 42, "本课题的架构由这些机制组合自然推出，并通过实验检验各模块作用。", fill=LIGHT_BLUE, line=LINE, font=18, bold=True, color=DARK_BLUE, align=2)
    elif idx == 7:
        add_bar(slide, "课题包含新架构设计和聚合管理平台两条主线，二者服务于同一组实验目标。")
        big_card(slide, 70, 165, 350, 175, "主线一：新架构", "空间记忆\n几何校验\n多专家编排\n长序列与动态场景评测", accent=BLUE)
        add_arrow(slide, 450, 230, 50, 30)
        big_card(slide, 540, 165, 350, 175, "主线二：管理平台", "模型统一调度\n结果统一归集\n跨模型对比\n新模型快速接入", accent=MID_BLUE)
        add_box(slide, 95, 400, 770, 48, "平台提供统一实验条件；新架构完成后可作为新模型接入平台进行同条件比较。", fill=LIGHT_BLUE, line=LINE, font=18, bold=True, color=DARK_BLUE, align=2)
    elif idx == 8:
        add_bar(slide, "总体架构以总线为核心，把感知、记忆、动静分离、校验和专家编排串联起来。")
        add_picture(slide, AI / "F05_candidate_architecture_x_3840x2160.png", 55, 138, 850, 300)
        add_box(slide, 115, 450, 730, 36, "输出包括逐帧三维点图、动态掩码和用于复核的中间证据。", fill=LIGHT_BLUE, line=LINE, font=17, bold=True, color=DARK_BLUE, align=2)
    elif idx == 9:
        add_bar(slide, "空间记忆模块把长序列上下文拆成压缩状态、空间锚点和局部滑窗三条路径。")
        add_picture(slide, AI / "F08_memory_three_branch_3840x2160.png", 80, 145, 800, 275)
        add_box(slide, 95, 445, 770, 38, "压缩管远程状态，选择管空间锚点，滑窗管当前上下文。", fill=LIGHT_BLUE, line=LINE, font=17, bold=True, color=DARK_BLUE, align=2)
    elif idx == 10:
        add_bar(slide, "几何校验模块先聚合冲突信号，再按阈值触发重跑或专家切换。")
        add_picture(slide, AI / "F06_critic_module_flow_3840x2160.png", 95, 150, 770, 270)
        add_box(slide, 95, 445, 770, 38, "校验理念来自 Test3R，本课题把它接入架构内部的修复动作。", fill=LIGHT_BLUE, line=LINE, font=17, bold=True, color=DARK_BLUE, align=2)
    elif idx == 11:
        add_bar(slide, "多专家编排模块根据输入条件和校验结果在七个模型专家之间切换。")
        experts = [
            ("MASt3R", "静态对"), ("Fast3R", "多视图"), ("Spann3R", "流式"), ("CUT3R", "动态容忍"),
            ("MoGe-2", "单目"), ("DepthAnything", "深度先验"), ("Test3R", "校验"),
        ]
        for i, (name, role) in enumerate(experts):
            x = 48 + (i % 4) * 215
            y = 150 + (i // 4) * 75
            add_box(slide, x, y, 180, 50, f"{name}\n{role}", fill=WHITE if i % 2 == 0 else LIGHT_BLUE, line=LINE, font=15, bold=True, color=DARK_BLUE, align=2)
        add_box(slide, 145, 330, 210, 58, "能力匹配度跨度", fill=LIGHT_BLUE, line=LINE, font=18, bold=True, color=DARK_BLUE, align=2)
        add_arrow(slide, 365, 348, 40, 24)
        add_box(slide, 415, 330, 210, 58, "成本调整解析平局", fill=LIGHT_BLUE, line=LINE, font=18, bold=True, color=DARK_BLUE, align=2)
        add_arrow(slide, 635, 348, 40, 24)
        add_box(slide, 685, 330, 150, 58, "失败退化", fill=LIGHT_BLUE, line=LINE, font=18, bold=True, color=DARK_BLUE, align=2)
        add_box(slide, 95, 430, 770, 38, "单模型各有优势场景，多专家路由用于提升复杂输入下的适应能力。", fill=BLUE, line=BLUE, font=17, bold=True, color=WHITE, align=2)
    elif idx == 12:
        add_bar(slide, "架构原型 v0.3 已跑通端到端流水线，当前为集成验证阶段。")
        rows0 = [
            ("原型状态", "v0.3 端到端流水线已跑通"),
            ("技术里程碑", "18 项完成：视觉骨干、三维检索、校验流程、Mamba 循环等"),
            ("KITTI 验证", "端到端运行无崩溃，点图 L2 = 20.47"),
            ("阶段边界", "集成验证数据，非训练后质量指标"),
        ]
        for i, (h, b) in enumerate(rows0):
            y = 145 + i * 62
            add_label(slide, 80, y, 150, 44, h)
            add_box(slide, 255, y, 610, 44, b, fill=WHITE if i % 2 == 0 else LIGHT_BLUE, line=LINE, font=17, bold=(i == 3), color=DARK_BLUE if i % 2 or i == 3 else TEXT, align=2)
        return
    elif idx == 13:
        add_bar(slide, "3R 模型缺少统一的部署、对比和调用基础设施，实验效率和应用落地都受限。")
        rows = [
            ("部署成本高", "每个模型各有环境和依赖，部署一次耗时长"),
            ("对比困难", "输入输出格式不统一，横向比较需手动对齐"),
            ("工具不适用", "Nerfstudio 面向 NeRF，商业产品闭源"),
            ("难以调用", "模型能力停留在脚本级，缺少标准接口"),
        ]
        for i, (h, b) in enumerate(rows):
            y = 150 + i * 62
            add_label(slide, 80, y, 150, 44, h)
            add_box(slide, 255, y, 610, 44, b, fill=WHITE if i % 2 == 0 else LIGHT_BLUE, line=LINE, font=17, bold=(i == 3), color=DARK_BLUE, align=2)
        add_box(slide, 115, 430, 730, 38, "统一部署、统一对比、标准化输出与 API 封装。", fill=BLUE, line=BLUE, font=17, bold=True, color=WHITE, align=2)
    elif idx == 14:
        add_bar(slide, "平台覆盖从模型部署、实验运行到能力输出的完整链路。")
        funcs = [("命令中心", "一键部署\n提交任务\n查看状态"), ("任务工作台", "上传→运行\n回传→完成"), ("样本矩阵", "同一输入\n多模型并排对比"), ("模型注册", "标准接口\n新模型快速上线"), ("能力输出", "统一格式导出\nAPI 封装调用")]
        for i, (h, b) in enumerate(funcs):
            x = 42 + i * 175
            big_card(slide, x, 165, 145, 145, h, b, accent=BLUE if i in (0, 3) else MID_BLUE)
        add_box(slide, 90, 380, 780, 52, "部署→实验→对比→输出，覆盖研究到应用的完整路径。", fill=LIGHT_BLUE, line=LINE, font=19, bold=True, color=DARK_BLUE, align=2)
    elif idx == 15:
        add_bar(slide, "平台通过统一执行合同，把桌面前端、后端调度和模型执行器连接起来。")
        add_picture(slide, AI / "F09_platform_four_layer_architecture_3840x2160.png", 70, 145, 820, 285)
        add_box(slide, 95, 455, 770, 34, "执行器封装模型差异，平台层统一提交和归集，顶层预留 API 导出接口。", fill=BLUE, line=BLUE, font=16, bold=True, color=WHITE, align=2)
    elif idx == 16:
        add_bar(slide, "6 个模型端到端验证通过，统一输入下的推理耗时差异明显。")
        bullets(slide, 60, 145, 255, ["DUSt3R / MASt3R", "MonST3R / Spann3R", "Fast3R / CUT3R", "Align3R 权重待补"], "接入模型")
        add_picture(slide, ASSETS / "timing_bars.png", 345, 135, 520, 270)
        add_box(slide, 70, 435, 820, 38, "统一输入为 13 帧 1920×1080；耗时差异体现统一调度与记录的必要性。", fill=LIGHT_BLUE, line=LINE, font=17, bold=True, color=DARK_BLUE, align=2)
    elif idx == 17:
        add_bar(slide, "平台从辅助实验到快速部署，再到 API 化服务下游应用。")
        rows = [
            ("短期", "辅助实验：完善对比视图，支撑消融和对照实验"),
            ("中期", "快速部署：新模型一键接入、即时对比，结果可导出"),
            ("长期", "API 服务：封装模型能力，供 SLAM / AR / 机器人调用"),
            ("应用场景", "科研实验 → 模型评估 → 下游应用集成"),
        ]
        for i, (h, b) in enumerate(rows):
            y = 150 + i * 62
            add_label(slide, 90, y, 135, 44, h)
            add_box(slide, 250, y, 610, 44, b, fill=WHITE if i % 2 == 0 else LIGHT_BLUE, line=LINE, font=17, color=DARK_BLUE, align=2)
    elif idx == 18:
        add_bar(slide, "平台支撑架构验证，验证通过的模型能力可进一步 API 化输出。")
        big_card(slide, 80, 165, 300, 155, "架构研究需求", "多专家对照\n模块消融\n长序列评测\n新架构接入", accent=BLUE)
        add_arrow(slide, 400, 220, 50, 30)
        big_card(slide, 520, 165, 320, 155, "平台支撑方式", "统一调度\n统一输出格式\n同条件对比\n运行数据记录\nAPI 导出", accent=rgb(38, 145, 95))
        add_box(slide, 95, 390, 770, 48, "平台支撑验证，验证通过的架构可直接封装为 API 对外输出。", fill=LIGHT_BLUE, line=LINE, font=18, bold=True, color=DARK_BLUE, align=2)
    elif idx == 19:
        add_bar(slide, "实验设计分为架构有效性验证和平台支撑能力验证两部分。")
        big_card(slide, 55, 150, 400, 230, "架构侧验证", "模块消融：记忆 / 校验 / 路由\n长序列对照：短序列到长序列\n专家对照：单模型 vs 多专家\n失败场景复核：动态 / 弱纹理 / 反射", accent=BLUE)
        big_card(slide, 505, 150, 400, 230, "平台侧验证", "模型接入是否稳定\n任务状态是否可追踪\n结果格式是否统一\n对比报告是否可导出", accent=MID_BLUE)
        add_box(slide, 115, 420, 730, 38, "先完成小规模可复现实例，再逐步扩展到长序列和多模型对照。", fill=LIGHT_BLUE, line=LINE, font=17, bold=True, color=DARK_BLUE, align=2)
    elif idx == 20:
        add_bar(slide, "创新点围绕几何校验、多专家编排、长序列记忆和聚合平台展开。")
        ips = [("1", "几何校验作为架构内置组件"), ("2", "异构多专家组合与路由"), ("3", "三分支稀疏注意力记忆统一"), ("4", "统一 3R 模型聚合管理平台")]
        for i, (n, text) in enumerate(ips):
            x = 90 + (i % 2) * 410
            y = 165 + (i // 2) * 112
            add_label(slide, x, y, 70, 52, n)
            add_box(slide, x + 90, y, 270, 52, text, fill=WHITE if i % 2 == 0 else LIGHT_BLUE, line=LINE, font=18, bold=True, color=DARK_BLUE, align=2)
        add_box(slide, 115, 420, 730, 38, "各创新点均需通过后续消融和对比实验支撑。", fill=BLUE, line=BLUE, font=17, bold=True, color=WHITE, align=2)
    elif idx == 21:
        add_bar(slide, "当前已完成架构文档、原型验证、平台代码和阶段综述。")
        big_card(slide, 70, 155, 380, 200, "架构侧", "7 份设计文档\n跨模块信号规约 v2.1\n原型 v0.3 跑通\n18 项技术里程碑完成", accent=BLUE)
        big_card(slide, 510, 155, 380, 200, "平台侧", "约 15000 行代码\n7 个执行器完成\n6 个端到端验证\n跨模型对比数据已生成", accent=rgb(38, 145, 95))
        add_box(slide, 115, 415, 730, 38, "同期完成 18 页中文综述，包含 44 篇引用、6 图和 5 表。", fill=LIGHT_BLUE, line=LINE, font=17, bold=True, color=DARK_BLUE, align=2)
    elif idx == 22:
        add_bar(slide, "后续时间安排分为近期准备、中期实验和后期论文三个阶段。")
        x0, y0 = 230, 155
        month_w, row_h = 72, 42
        labels = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8"]
        stages = [("近期准备", 230, 144, 144, BLUE), ("中期实验", 374, 144, 288, MID_BLUE), ("后期论文", 662, 144, 144, BLUE)]
        for text, x, y, w, color0 in stages:
            add_box(slide, x, y, w, 28, text, fill=color0, line=color0, font=13, bold=True, color=WHITE, align=2)
        for i, m in enumerate(labels):
            add_box(slide, x0 + i * month_w, y0 + 34, month_w, 30, m, fill=LIGHT_BLUE, line=LINE, font=13, bold=True, color=DARK_BLUE, align=2)
        tasks = [
            ("开题定稿与平台补充", 1, 2, BLUE),
            ("校验标定与模块消融", 2, 5, ORANGE),
            ("长序列与多专家评测", 4, 6, rgb(38, 145, 95)),
            ("平台对比视图与报告", 2, 6, MID_BLUE),
            ("论文整理与系统固化", 7, 8, rgb(32, 82, 145)),
        ]
        for r, (task, start, end, color0) in enumerate(tasks):
            y = y0 + 68 + r * row_h
            add_box(slide, 70, y, 150, 28, task, fill=WHITE, line=LINE, font=12, bold=True, color=DARK_BLUE, align=2)
            for i in range(8):
                add_box(slide, x0 + i * month_w, y, month_w, 28, "", fill=WHITE, line=rgb(218, 230, 242))
            bar_x = x0 + (start - 1) * month_w + 9
            bar_w = (end - start + 1) * month_w - 18
            shp = slide.Shapes.AddShape(5, bar_x, y + 7, bar_w, 14)
            shp.Fill.ForeColor.RGB = color0
            shp.Line.ForeColor.RGB = color0
        add_box(slide, 90, 440, 780, 40, "近期完成开题与平台补齐，中期集中做训练消融，后期整理论文并补充实验。", fill=LIGHT_BLUE, line=LINE, font=17, bold=True, color=DARK_BLUE, align=2)
    elif idx == 23:
        add_bar(slide, "主要风险来自训练质量、算力约束、多专家效果和校验标定复杂度。")
        risks = [
            ("训练质量未知", "消融实验逐步推进，每一步保留独立结论"),
            ("GPU 算力限制", "优先小规模验证，按阶段逐步扩展"),
            ("多专家收益不稳定", "保留单模型 baseline 作为对照"),
            ("阈值标定复杂", "先标定主要失败模式，再逐步扩展"),
        ]
        for i, (r, m) in enumerate(risks):
            y = 150 + i * 68
            add_label(slide, 70, y, 190, 48, r)
            add_box(slide, 285, y, 590, 48, m, fill=WHITE if i % 2 == 0 else LIGHT_BLUE, line=LINE, font=17, color=DARK_BLUE, align=2)
        add_box(slide, 115, 430, 730, 38, "后续按优先级推进，确保每个阶段都有可复核产出。", fill=BLUE, line=BLUE, font=17, bold=True, color=WHITE, align=2)


def slide_thanks(slide):
    texts = [s for s in slide.Shapes if shape_text(s)]
    texts.sort(key=lambda s: (s.Top, s.Left))
    for s in texts:
        try:
            s.TextFrame.TextRange.Text = ""
        except Exception:
            pass
    add_box(slide, 90, 165, 780, 70, "总结致谢\n敬请批评指正！", fill=rgb(255, 255, 255), line=rgb(255, 255, 255), font=34, bold=True, color=BLUE, align=2)
    add_box(slide, 150, 275, 660, 126, "本课题从 3R 模型的优势出发，针对长序列漂移、缺乏校验和单模型局限三个问题，设计融合空间记忆、几何校验和多专家编排的新型架构。\n同时开发聚合管理平台，支撑多模型对比实验和后续架构评测。", fill=rgb(255, 255, 255), line=rgb(255, 255, 255), font=18, bold=True, color=TEXT, align=2)


def export_contact():
    def key(p):
        ds = "".join(ch for ch in p.stem if ch.isdigit())
        return int(ds) if ds else 0
    imgs = sorted(PREVIEW.glob("*.png"), key=key)
    thumbs = []
    for i, p in enumerate(imgs, 1):
        im = Image.open(p).convert("RGB")
        im.thumbnail((320, 180))
        c = Image.new("RGB", (320, 210), "white")
        c.paste(im, ((320 - im.width) // 2, 0))
        d = ImageDraw.Draw(c)
        d.text((6, 186), f"Slide {i:02d}", fill=(0, 0, 0))
        thumbs.append(c)
    cols = 4
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 320, rows * 210), "white")
    for i, t in enumerate(thumbs):
        sheet.paste(t, ((i % cols) * 320, (i // cols) * 210))
    sheet.save(CONTACT)


def main():
    make_assets()
    if OUT.exists():
        OUT.unlink()
    if PREVIEW.exists():
        shutil.rmtree(PREVIEW)
    PREVIEW.mkdir(parents=True, exist_ok=True)

    app = win32com.client.Dispatch("PowerPoint.Application")
    app.Visible = True
    pres = app.Presentations.Add()
    for src in SLIDE_SOURCES:
        pres.Slides.InsertFromFile(str(REF), pres.Slides.Count, src, src)
    while pres.Slides.Count > len(SLIDE_SOURCES):
        pres.Slides(1).Delete()

    for i, title in enumerate(TITLES, 1):
        slide = pres.Slides(i)
        if i == 1:
            slide_cover(slide)
        elif i == 2:
            set_title(slide, title)
            slide_outline(slide)
        elif i == 24:
            slide_thanks(slide)
        else:
            set_title(slide, title)
            build_slide(slide, i)

    pres.SaveAs(str(OUT))
    pres.Export(str(PREVIEW), "PNG")
    try:
        pres.Close()
    except Exception:
        pass
    try:
        app.Quit()
    except Exception:
        pass
    export_contact()
    print(OUT)
    print(PREVIEW)
    print(CONTACT)


if __name__ == "__main__":
    main()
