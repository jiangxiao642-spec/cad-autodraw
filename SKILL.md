---
name: cad-autodraw
description: 基于 ezdxf + cad-gb-standard 的建筑平面图自动出图。触发：cad出图、画平面图、生成DXF、自动标注。
category: software-development
triggers:
  - cad出图
  - 画平面图
  - 生成dxf
  - 自动标注
  - 建筑图
  - 施工图生成
---

# CAD 自动出图

基于 ezdxf 库 + cad-gb-standard 规范生成建筑平面图 DXF 文件。

## 当前能力

- 单房间平面图：墙线/门窗/三道尺寸/轴号/散水/台阶/标高/指北针
- DIMSTYLE 全要素缩放（dimtxt/dimasz/dimexe/dimexo/dimdli）
- 全局 SCALE 变量切换出图比例
- 块化门定义（M_UNIT，参数化门宽/铰链侧/开启方向）

## 使用方法

```bash
pip install ezdxf
python floor_plan_single.py   # → floor_plan.dxf
```

改 `SCALE = 50` 切换比例。

## 已知缺陷

1. 仅支持矩形房间
2. WSL 内 `saveas('/mnt/c/Desktop/')` 可能 PermissionError → 存 `/mnt/c/Users/.../hermes-temp/` 再 PowerShell 搬
3. 门块 ARC 在旧版本 AutoCAD 可能渲染异常
4. 中文字体跨平台可能缺 shx

## 配套规范

见 `cad-gb-standard` skill。

## 文件索引

- `floor_plan_single.py` — 单房间平面图出图脚本
- `references/wsl-desktop-permission.md` — WSL→桌面写入权限绕行方案
