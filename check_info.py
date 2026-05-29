import os
from pathlib import Path
import soundfile as sf
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# 設定資料集根目錄路徑
dataset_path = Path("/share/nas169/wago/data/Emotion Speech Dataset")

# 1. 精準鎖定 0011 ~ 0020 的資料夾
target_folders = [f"{i:04d}" for i in range(11, 21)]

# 2. 收集所有候選的 .wav 檔案路徑
wav_files = []
for folder in target_folders:
    folder_path = dataset_path / folder
    if folder_path.exists():
        # rglob 會遞迴往下一層 (例如 Angry, Happy 等資料夾) 尋找
        wav_files.extend(folder_path.rglob("*.wav"))

# 3. 定義檢查音檔長度的函數 (僅讀取 header)
def get_long_audio(file_path):
    try:
        # sf.info 非常快，不會將 PCM 數據載入記憶體
        info = sf.info(file_path)
        if info.duration > 5.0:
            return file_path
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return None

# 4. 使用多執行緒平行掃描 (I/O 密集型任務，Thread 比 Process 更適合)
long_audio_files = []
# workers 數量可以設為 CPU 核心數的 2~4 倍來榨乾 I/O 效能
max_workers = min(32, (os.cpu_count() or 1) * 4) 

print(f"總共找到 {len(wav_files)} 個候選檔案，開始掃描長度...")

with ThreadPoolExecutor(max_workers=max_workers) as executor:
    # 搭配 tqdm 顯示進度條
    results = list(tqdm(executor.map(get_long_audio, wav_files), total=len(wav_files)))

# 過濾掉 None 的結果
long_audio_files = [res for res in results if res is not None]

print(f"\n掃描完成！大於 5 秒的音檔共有 {len(long_audio_files)} 個。")
# print(long_audio_files[:5]) # 印出前 5 個檢查看看
# print(long_audio_files)

from collections import defaultdict

# 建立一個字典來分類結構：grouped_files[語者][情緒] = [檔名1, 檔名2...]
grouped_files = defaultdict(lambda: defaultdict(list))

for path in long_audio_files:
    speaker = path.parent.parent.name  # 取得 "0012"
    emotion = path.parent.name         # 取得 "Angry"
    filename = path.name               # 取得 "0012_000363.wav"
    grouped_files[speaker][emotion].append(filename)

print("\n📊 大於 5 秒的音檔清單 (依語者與情緒分類)：")
print("=" * 50)

# 依序印出整理好的結果
for speaker in sorted(grouped_files.keys()):
    print(f"\n👤 語者: {speaker}")
    for emotion in sorted(grouped_files[speaker].keys()):
        files = sorted(grouped_files[speaker][emotion])
        print(f"  🎭 {emotion} (共 {len(files)} 個):")
        
        # 每行印 5 個檔名，方便閱讀
        for i in range(0, len(files), 5):
            chunk = files[i:i+5]
            print("    " + ", ".join(chunk))