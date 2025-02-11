import os
import json

settings_path = "./settings.json"

# 패키지 경로 찾기
package_dirs = []
for root, dirs, files in os.walk("/mnt/sda1"):
    for d in dirs:
        if d in ["site-packages", "dist-packages"]:
            package_dirs.append(os.path.join(root, d))

# 기존 설정 불러오기
if os.path.exists(settings_path):
    with open(settings_path, "r") as f:
        settings = json.load(f)
else:
    settings = {}

# 업데이트할 필드
settings["python.autoComplete.extraPaths"] = package_dirs
settings["python.analysis.extraPaths"] = package_dirs
settings["ros.distro"] = "humble"
settings["cmake.sourceDirectory"] = "/mnt/sda1/rokey_project/4week/2024-2_ROKEYBOOTCAMP_intelligence_AI_project_2/rosws/src/military_interface"

# 설정 파일 저장
os.makedirs(os.path.dirname(settings_path), exist_ok=True)
with open(settings_path, "w") as f:
    json.dump(settings, f, indent=4)

print(f"VS Code settings.json 파일이 업데이트되었습니다: {settings_path}")
