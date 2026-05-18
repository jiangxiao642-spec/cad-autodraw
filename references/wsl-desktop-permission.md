# WSL → Windows 桌面文件写入绕行方案

## 问题

WSL 内 `ezdxf.saveas('/mnt/c/Users/xxx/Desktop/file.dxf')` 经常报 `PermissionError: [Errno 13]`。

## 原因

WSL 通过 drvfs 挂载 Windows 文件系统，桌面文件夹有特殊 ACL 限制，Python 进程跨文件系统写入可能被拒绝。

## 绕行

```python
# 步骤1：写到 C 盘普通目录
doc.saveas('/mnt/c/Users/xxx/hermes-temp/output.dxf')

# 步骤2：通过 Windows 桥接 PowerShell 搬到桌面
# mcp_windows_bridge_run_powershell:
#   Remove-Item 'C:\Users\xxx\Desktop\output.dxf' -Force -ErrorAction SilentlyContinue
#   Move-Item 'C:\Users\xxx\hermes-temp\output.dxf' 'C:\Users\xxx\Desktop\output.dxf' -Force
```

## 注意

- 如果桌面已有同名文件，Move-Item -Force 会覆盖但报错，实际已移动
- 优先用 Copy-Item 而非 Move-Item，避免跨卷问题
- hermes-temp 目录需预先 `mkdir -p`
