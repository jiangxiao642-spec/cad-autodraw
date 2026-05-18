# cad-autodraw

基于 ezdxf + cad-gb-standard 规范的建筑平面图自动出图代码库。

## 当前完成度

- [x] 单房间平面图（墙/门/窗/尺寸/轴号/散水/台阶/标高/指北针）
- [x] 三道尺寸线自动生成
- [x] 1:50 模型空间缩放（全局 SCALE 变量切换比例）
- [x] 块化门定义（M_UNIT，支持铰链侧/开启方向/门宽参数化）
- [x] DIMSTYLE 全要素缩放
- [x] 敏感信息扫描通过
- [ ] 多房间批量出图
- [ ] 立面图/剖面图自动生成
- [ ] 门窗统计表
- [ ] 图框/标题栏自动生成

## 使用方法

```bash
pip install ezdxf
python floor_plan_single.py   # 输出 floor_plan.dxf，AutoCAD 直接打开
```

改比例：编辑脚本第一行 `SCALE = 50`（1:50）或 `100`（1:100）。

## 已知缺陷

1. 仅支持矩形房间，不支持 L 形/多边形/曲线墙
2. 字高依赖 SCALE 手动设定，AutoCAD 打开后不会自动适配视口
3. ezdxf 写入 Windows 桌面可能 PermissionError → 存临时目录再搬运
4. 门块内 ARC 在旧版本 AutoCAD 中可能渲染异常

## 完整版计划

- v0.2：多房间批量出图（JSON 驱动）
- v0.3：立面图/剖面图自动生成
- v0.4：楼梯/电梯井自动绘制
- v1.0：成套施工图一键生成

## 依赖

- Python 3.10+ / ezdxf >= 1.3
- 配套规范：[cad-gb-standard](https://github.com/chenyi-cad/cad-gb-standard)

## 联系方式

邮箱：jiangxiao642@gmail.com