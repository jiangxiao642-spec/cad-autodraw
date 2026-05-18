"""
一层平面图 — 6000×4000 砖混住宅
1:50 模型空间出图  所有标注×50比例
GB/T 50001-2017
"""
import ezdxf
from ezdxf import units
import math

doc = ezdxf.new(setup=True)
doc.units = units.MM
msp = doc.modelspace()

# ═══ 出图比例 ═══
SC = 50  # 1:50

# ═══ 线型 ═══
doc.linetypes.add('AXIS', pattern=[15,-1,0,-1,0.5,-1], description='定位轴线')

# ═══ 图层 ═══
LAY = {
    'A-AXIS':    {'c':1,  'lt':'AXIS',       'lw':18},
    'A-WALL':    {'c':7,  'lt':'Continuous', 'lw':70},
    'A-DOOR':    {'c':4,  'lt':'Continuous', 'lw':35},
    'A-WINDOW':  {'c':4,  'lt':'Continuous', 'lw':35},
    'A-DIM':     {'c':2,  'lt':'Continuous', 'lw':18},
    'A-DIM-ELEV':{'c':2,  'lt':'Continuous', 'lw':18},
    'A-TEXT':    {'c':6,  'lt':'Continuous', 'lw':18},
    'A-HATCH':   {'c':8,  'lt':'Continuous', 'lw':18},
    'A-STAIR':   {'c':3,  'lt':'Continuous', 'lw':35},
    'A-SECT':    {'c':7,  'lt':'Continuous', 'lw':70},
}
for n, p in LAY.items():
    lay = doc.layers.add(n, color=p['c'])
    lay.dxf.linetype = p['lt']; lay.dxf.lineweight = p['lw']

# ═══ 尺寸样式（按比例放大） ═══
dimstyle = doc.dimstyles.duplicate_entry('EZDXF', 'GB50')
dimstyle.dxf.dimtxt = 2.5 * SC        # 字高 125
dimstyle.dxf.dimasz = 2.0 * SC        # 箭头 100
dimstyle.dxf.dimexe = 2.0 * SC        # 界线超出 100
dimstyle.dxf.dimexo = 2.0 * SC        # 界线偏移 100
dimstyle.dxf.dimdli = 8.0 * SC        # 基线间距 400
dimstyle.dxf.dimtad = 1               # 文字在线上方
dimstyle.dxf.dimtih = 0               # 文字不强制水平
dimstyle.dxf.dimtoh = 0

# ═══ 快捷函数 ═══
def ln(lay, x1, y1, x2, y2):
    msp.add_line((x1,y1),(x2,y2), dxfattribs={'layer':lay})
def tx(lay, s, x, y, h=None, rot=0):
    msp.add_text(s, dxfattribs={'layer':lay, 'height':h or 3.5*SC,
                  'insert':(x,y), 'rotation':rot})
def cir(lay, cx, cy, r):
    msp.add_circle((cx,cy), r, dxfattribs={'layer':lay})
def dim(p1, p2, base, angle=0):
    msp.add_linear_dim(base=base, p1=p1, p2=p2, dimstyle='GB50',
                       dxfattribs={'layer':'A-DIM'}, angle=angle)

# ═══ 建筑参数 (mm) ═══
BL, BW = 6000, 4000
t = 240; a_off = 120

axes_x = [a_off, 3000, BL-a_off]
axes_y = [a_off, BW-a_off]

# 门
dw = 900; dx = (BL-dw)/2
# 窗
wtw, wtx = 1500, (BL-1500)/2
wrw, wry = 1200, (BW-1200)/2

# 散水 台阶
aw = 800
sn = 3; st = 300; sw = 1300
sl2 = dx+dw/2-sw/2; sr2 = dx+dw/2+sw/2

# ═══ 散水 ═══
ln('A-HATCH', -aw,-aw, sl2,-aw); ln('A-HATCH', sr2,-aw, BL+aw,-aw)
ln('A-HATCH', BL+aw,-aw, BL+aw,BW+aw)
ln('A-HATCH', BL+aw,BW+aw, -aw,BW+aw); ln('A-HATCH', -aw,BW+aw, -aw,-aw)
ln('A-HATCH', 0,-aw, dx,-aw); ln('A-HATCH', dx+dw,-aw, BL,-aw)
ln('A-HATCH', BL,0, BL,BW); ln('A-HATCH', 0,BW, 0,0)
ln('A-HATCH', 0,BW, BL,BW)
for sx in [1200, 4800]:
    ln('A-HATCH', sx,-aw+10*SC, sx,-aw+25*SC)
    ln('A-HATCH', sx,-aw+25*SC, sx-60,-aw+21*SC)
    ln('A-HATCH', sx,-aw+25*SC, sx+60,-aw+21*SC)
tx('A-TEXT', '3%', sx-25, -aw+19*SC, 3.5*SC)
tx('A-TEXT', 'C15混凝土散水 宽800', BL/2-70*SC/50, -aw-9*SC, 3.5*SC)

# ═══ 台阶 ═══
so = -aw; sy_end = so-sn*st
for i in range(sn):
    ln('A-STAIR', sl2, so-(i+1)*st, sr2, so-(i+1)*st)
ln('A-STAIR', sl2, so, sl2, sy_end)
ln('A-STAIR', sr2, so, sr2, sy_end)
ay = sy_end - 250
ln('A-STAIR', dx+dw/2, so, dx+dw/2, ay)
ln('A-STAIR', dx+dw/2, ay, dx+dw/2-60, ay+120)
ln('A-STAIR', dx+dw/2, ay, dx+dw/2+60, ay+120)
tx('A-TEXT', '上', dx+dw/2+40, ay+100, 3.5*SC)

# ═══ 轴线 ═══
ax_ext = 65 * SC  # 32.5mm纸上
for ax in axes_x:
    ln('A-AXIS', ax, -aw-ax_ext, ax, BW+aw+ax_ext)
for ay in axes_y:
    ln('A-AXIS', -aw-ax_ext, ay, BL+aw+ax_ext, ay)

# ═══ 轴号（下方+左侧，Ø8mm×50=Ø400绘图单位） ═══
r_axis = 4.0 * SC  # 200
ax_y0 = -aw - ax_ext - 3*SC  # 距轴线端3mm
ax_x0 = -aw - ax_ext - 3*SC
for i, ax in enumerate(axes_x):
    cir('A-AXIS', ax, ax_y0, r_axis)
    tx('A-TEXT', str(i+1), ax-1.2*SC, ax_y0-1.5*SC, 3.5*SC)
for i, ay in enumerate(axes_y):
    cir('A-AXIS', ax_x0, ay, r_axis)
    tx('A-TEXT', chr(65+i), ax_x0-1.2*SC, ay-1.5*SC, 3.5*SC)

# ═══ 墙体 ═══
ln('A-WALL', 0,0, dx,0); ln('A-WALL', dx+dw,0, BL,0)
ln('A-WALL', t,t, dx,t); ln('A-WALL', dx+dw,t, BL-t,t)
ln('A-WALL', 0,BW, wtx,BW); ln('A-WALL', wtx+wtw,BW, BL,BW)
ln('A-WALL', t,BW-t, wtx,BW-t); ln('A-WALL', wtx+wtw,BW-t, BL-t,BW-t)
ln('A-WALL', 0,0, 0,BW); ln('A-WALL', t,t, t,BW-t)
ln('A-WALL', BL,0, BL,wry); ln('A-WALL', BL,wry+wrw, BL,BW)
ln('A-WALL', BL-t,t, BL-t,wry); ln('A-WALL', BL-t,wry+wrw, BL-t,BW-t)

# ═══ 门 ═══
ln('A-DOOR', dx,0, dx,t); ln('A-DOOR', dx+dw,0, dx+dw,t)
ln('A-DOOR', dx,0, dx,dw)
for deg in range(0,91,5):
    r1=math.radians(deg); r2=math.radians(deg+5)
    ln('A-DOOR', dx+dw*math.cos(r1), dw*math.sin(r1),
                 dx+dw*math.cos(r2), dw*math.sin(r2))

# ═══ 窗 ═══
g=80
ln('A-WINDOW', wtx,BW-t, wtx,BW); ln('A-WINDOW', wtx+wtw,BW-t, wtx+wtw,BW)
ln('A-WINDOW', BL-t,wry, BL,wry); ln('A-WINDOW', BL-t,wry+wrw, BL,wry+wrw)
ln('A-WINDOW', wtx,BW-g, wtx+wtw,BW-g); ln('A-WINDOW', wtx,BW-t+g, wtx+wtw,BW-t+g)
ln('A-WINDOW', BL-g,wry, BL-g,wry+wrw); ln('A-WINDOW', BL-t+g,wry, BL-t+g,wry+wrw)

# ═══ 文字 ═══
tx('A-TEXT', 'M0921', dx+dw/2-14*SC, 350, 3.5*SC)
tx('A-TEXT', 'C1518', wtx+wtw/2-14*SC, BW+150, 3.5*SC)
tx('A-TEXT', 'C1218', BL+150, wry+wrw/2-5, 3.5*SC)
tx('A-TEXT', '卧室', BL/2-12*SC, BW/2+50, 5.0*SC)

# ═══ 标高 ═══
eh=3.0*SC
ex,ey=500,500
msp.add_lwpolyline([(ex,ey+eh),(ex+eh,ey),(ex+eh,ey+eh)], close=True,
                   dxfattribs={'layer':'A-DIM-ELEV'})
ln('A-DIM-ELEV', ex+eh, ey+eh, ex+eh+15*SC, ey+eh)
tx('A-TEXT', '%%p0.000', ex+eh+2*SC, ey+eh-1*SC, 2.5*SC)

# ═══ 指北针 Ø24mm×50 ═══
nd=24.0*SC; nr=nd/2
ncx,ncy=BL-12*SC, BW+60*SC
cir('A-TEXT', ncx, ncy, nr)
ln('A-TEXT', ncx, ncy+nr-2*SC, ncx, ncy-nr+2*SC)
ln('A-TEXT', ncx-1.5*SC, ncy-nr+2*SC, ncx+1.5*SC, ncy-nr+2*SC)
tx('A-TEXT', 'N', ncx-3.5*SC, ncy+nr+3*SC, 5.0*SC)

# ═══ 剖面符号 ═══
sx,sy=-aw-20*SC, BW/2
ln('A-SECT', sx,sy, sx+8*SC,sy)
ln('A-SECT', sx+8*SC,sy, sx+8*SC,sy-5*SC)
ln('A-SECT', sx+8*SC,sy, sx+8*SC,sy+5*SC)
tx('A-TEXT', '1', sx+8*SC-1*SC, sy-7*SC, 5.0*SC)

# ═══ 三道尺寸线 ═══
dy0 = -aw - 10*SC         # 距散水外缘10mm纸上
dy1 = dy0 - 16*SC         # 第一道: 细部 (16mm纸上间距)
dy2 = dy1 - 16*SC         # 第二道: 轴距
dy3 = dy2 - 16*SC         # 第三道: 总长

# 底边第一道
dim((0,0), (dx,0), base=(0,dy1))
dim((dx,0), (dx+dw,0), base=(dx,dy1))
dim((dx+dw,0), (BL,0), base=(dx+dw,dy1))
# 第二道
dim((axes_x[0],0), (axes_x[1],0), base=(axes_x[0],dy2))
dim((axes_x[1],0), (axes_x[2],0), base=(axes_x[1],dy2))
# 第三道
dim((0,0), (BL,0), base=(0,dy3))

# 右边
dx0 = BL + aw + 10*SC
dx1 = dx0 + 16*SC; dx2 = dx1 + 16*SC; dx3 = dx2 + 16*SC
dim((BL,0), (BL,wry), base=(dx1,0), angle=90)
dim((BL,wry), (BL,wry+wrw), base=(dx1,wry), angle=90)
dim((BL,wry+wrw), (BL,BW), base=(dx1,wry+wrw), angle=90)
dim((BL,axes_y[0]), (BL,axes_y[1]), base=(dx2,axes_y[0]), angle=90)
dim((BL,0), (BL,BW), base=(dx3,0), angle=90)

# ═══ 图名 ═══
ty = dy3 - 12*SC
tx('A-TEXT', '一层平面图', BL/2-35*SC, ty, 7.0*SC)
ln('A-TEXT', BL/2-35*SC, ty-2*SC, BL/2+40*SC, ty-2*SC)
ln('A-TEXT', BL/2-35*SC, ty-3*SC, BL/2+40*SC, ty-3*SC)
tx('A-TEXT', '1:50', BL/2+50*SC, ty, 3.5*SC)

# ═══ 保存 ═══
path = 'floor_plan.dxf'  # 输出路径，按需修改
doc.saveas(path)
print(f'OK → {path} (1:{SC})')
