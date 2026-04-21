# Live Japanese Caption + Translation

实时捕获日语语音，转录 + 翻译成中文，浮窗显示字幕。

- 转录：faster-whisper（本地，Apple Silicon 加速）
- 翻译：Ollama 本地 LLM（qwen2.5:7b）
- 零云端，零 API 费用

---

## 安装步骤

### 1. 安装 Ollama 并拉取翻译模型

```bash
brew install ollama
ollama pull qwen2.5:7b
```

### 2. 安装 Python 依赖

建议用虚拟环境：

```bash
cd ~/path/to/live-caption
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. 允许麦克风权限

首次运行时 macOS 会弹出麦克风权限请求，点击"允许"即可。

也可手动开启：**系统设置 → 隐私与安全性 → 麦克风 → 允许 Terminal**

---

## 捕获通话音频（非麦克风）

如果你想捕获电话/视频通话的系统音频而非麦克风：

1. 安装 **BlackHole** 虚拟声卡：
   ```bash
   brew install --cask blackhole-2ch
   ```
2. 在**音频 MIDI 设置**中创建"多输出设备"，包含扬声器 + BlackHole
3. 将系统输出切换到这个多输出设备
4. 用 `--device` 参数选择 BlackHole 作为输入：
   ```bash
   python main.py --list-devices   # 查看设备列表
   python main.py --device 3       # 用 BlackHole 的设备号
   ```

---

## 运行

```bash
# 启动 Ollama（新建终端）
ollama serve

# 运行字幕工具（默认麦克风）
python main.py

# 或使用 large-v3 模型（更准确，稍慢）
python main.py --model large-v3

# 列出所有音频输入设备
python main.py --list-devices
```

## 快捷键

- **Cmd+Q** 或 **Q** — 退出
- 拖动窗口任意位置移动

---

## 常见问题

**Ollama 没跑 / 翻译报错**：先运行 `ollama serve`，再启动字幕工具。

**听不到声音 / 没有转录**：检查 macOS 麦克风权限，或用 `--list-devices` 确认设备号正确。

**想换语言**：修改 `translator.py` 里的 `SYSTEM_PROMPT`，比如改成"翻译成英语"。
