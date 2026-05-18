## Slide 8
- idx=1 id=90 name=TextBox 89 type=17 top=19.2 left=9.1 w=60.9 h=41.2 text=02
- idx=2 id=92 name=TextBox 91 type=17 top=21.2 left=74.5 w=507.1 h=44.8 text=总体架构一览
- idx=3 id=2 name=Rectangle 1 type=1 top=130.0 left=0.0 w=960.0 h=410.0 text=
- idx=4 id=3 name=Rectangle 2 type=1 top=92.0 left=34.0 w=890.0 h=40.0 text=五个功能模块通过总线联动，输入图像序列后逐帧输出三维点图和校验证据。
- idx=5 id=5 name=Picture 4 type=13 top=138.0 left=213.5 w=533.0 h=300.0 text=
- idx=6 id=6 name=Rectangle 5 type=1 top=450.0 left=115.0 w=730.0 h=36.0 text=输出包括逐帧三维点图、动态掩码和用于复核的中间证据。

## Slide 9
- idx=1 id=90 name=TextBox 89 type=17 top=19.2 left=9.1 w=60.9 h=41.2 text=02
- idx=2 id=92 name=TextBox 91 type=17 top=21.2 left=74.5 w=507.1 h=44.8 text=空间记忆模块
- idx=3 id=2 name=Rectangle 1 type=1 top=130.0 left=0.0 w=960.0 h=410.0 text=
- idx=4 id=3 name=Rectangle 2 type=1 top=92.0 left=34.0 w=890.0 h=40.0 text=长序列不能全靠全局注意力，需要把远程、检索和局部三种记忆分开处理。
- idx=5 id=5 name=Picture 4 type=13 top=145.0 left=235.7 w=488.6 h=275.0 text=
- idx=6 id=6 name=Rectangle 5 type=1 top=445.0 left=95.0 w=770.0 h=38.0 text=压缩管远程状态，选择管空间锚点，滑窗管当前上下文。

## Slide 10
- idx=1 id=90 name=TextBox 89 type=17 top=19.2 left=9.1 w=60.9 h=41.2 text=02
- idx=2 id=92 name=TextBox 91 type=17 top=21.2 left=74.5 w=507.1 h=44.8 text=几何校验模块
- idx=3 id=2 name=Rectangle 1 type=1 top=130.0 left=0.0 w=960.0 h=410.0 text=
- idx=4 id=3 name=Rectangle 2 type=1 top=92.0 left=34.0 w=890.0 h=40.0 text=几何校验模块先聚合冲突信号，再按阈值触发重跑或模型切换。
- idx=5 id=5 name=Picture 4 type=13 top=150.0 left=240.1 w=479.7 h=270.0 text=
- idx=6 id=6 name=Rectangle 5 type=1 top=445.0 left=95.0 w=770.0 h=38.0 text=校验思路源自 Test3R，本课题将其嵌入架构内部，支持在线修复。
