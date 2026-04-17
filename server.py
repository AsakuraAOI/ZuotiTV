#!/usr/bin/env python3
"""
做题蛆度量表 - Flask 中转后端
纯静态页面发请求到这里，server 转发给 AI，Key 不暴露在浏览器
"""

import os
import re
import json
import argparse
from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI

app = Flask(__name__, static_folder=".")

# ========== Config ==========
CONFIG_FILE = "config.json"


def load_config():
    defaults = {
        "api_key": "",
        "base_url": "https://api.siliconflow.cn/v1",
        "model": "deepseek-ai/DeepSeek-V3.2",
    }
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            for k in defaults:
                defaults[k] = cfg.get(k, defaults[k])
    return defaults


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "").strip()
    api_key = data.get("api_key", "").strip()
    base_url = data.get("base_url", "").strip()
    model = data.get("model", "").strip()

    if not text or len(text) < 5:
        return jsonify({"error": "文本至少需要5个字符"}), 400
    if not api_key:
        return jsonify({"error": "缺少 API Key"}), 400

    client = OpenAI(
        api_key=api_key,
        base_url=base_url or None,
    )

    SYSTEM_PROMPT = """You are a professional "做题蛆度量表" (Test Worm Scale) scoring expert.

"做题蛆" is Chinese internet slang for people who deeply believe that test-taking is the only path to success, with academic scores as the sole value metric.
Core ideology: 三位一体 = 穷人原罪论 + 做题万能论 + 社会达尔文主义

Grading scale:
- 0-15: Normal - loves learning but not obsessed, understands diverse values
- 16-35: Test-prone - has test-thinking but not solidified
- 36-60: Test-devotee - deeply believes test scores = success
- 61-80: Test-worm (mild) - triad ideology forming
- 81-100: Test-worm (severe) - full-blown social Darwinist
- 101+: 间桐樱 (Matomer) - completely blackpilled, self-destruction mode

Analyze across 11 dimensions (0-10 each, weighted sum + burst bonus):
1. 穷人原罪论 (12%): poverty = deserved/lazy; enjoying life is sinful
2. 做题万能论 (12%): high scores = total success; low-scorers have no right to judge
3. 社会达尔文主义 (12%): survival of fittest; mental illness/suicide is "growing pain"
4. 做题行为模式 (10%): question-bank dependency, knowledge hoarding, standard-answer obsession
5. 炫耀/凡尔赛 (10%): flexing grades, humble-brag humble-flexing, reverse flexing
   CRITICAL: "只考了班级前十" / "没考好才70分" = humble-brag using negative words to wrap positive scores
6. 权威崇拜 (8%): blind worship of "study gods", method cults
7. 权力滥用 (6%): micro-power abuse, school-defending
8. 心理/情绪 (8%): score-obsession, ranking anxiety, "破防" (being triggered)
9. 价值观 (7%): suffering-worship, exam-worship, path-dependency, "莫欺少年穷" mentality
10. 经典话术 (8%): Each phrase matched = 3pts, max 10pts
    - "查查学信网"
    - "我的xxx就是你的一辈子了"
    - "600分以下不配和我讨论"
    - "你不努力，活该被淘汰"
    - "累就对了，舒服是留给死人的"
    - "gap一年？你疯了，落后一整年！"
    - "莫欺少年穷"
    - "1450籍"
    - Referring to 985/211 as "五道口职业技术学院" / "沙河镇大洼村" / "黄渡理工大学"
    - Self-deprecating nicknames like "小菜鸡" + "mol佬" for reverse flexing
    - Corporate buzzword stacking: "复盘" "打法对比" "数据溯源" "优化"
11. 性/亲密关系扭曲 (7%): sexual repression, warped attitudes toward romance/intimacy; treating relationships as status competition; using sexual references to assert dominance; inability to form genuine intimate connections; obsessive fixation on virginity/"母胎solo" status; viewing opposite gender purely as conquests or status symbols

Output JSON with:
- score: 0-100+ total (weighted + burst bonuses)
- level: level name
- dimension_scores: dict of all 11 dimensions with numeric scores (must include all keys)
- dimension_analysis: dict of all 11 dimensions with brief text explanation in Chinese for each (must include all keys)
- analysis: brief overall analysis under 50 chars
- matching_indicators: list of matched indicators

Output JSON only, no other text."""

    try:
        response = client.chat.completions.create(
            model=model or "deepseek-ai/DeepSeek-V3.2",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Analyze this text for 做题目蛆 characteristics:\n\n---\n{text}\n---\n\nOutput JSON."},
            ],
            temperature=0.1,
        )
        content = response.choices[0].message.content
        if not content:
            return jsonify({"error": "API 返回内容为空"}), 500

        clean = content.strip()
        if clean.startswith("```"):
            clean = re.sub(r"^```[a-z]*\n?", "", clean)
        clean = re.sub(r"\n?```$", "", clean)

        return jsonify(json.loads(clean))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="做题蛆度量表服务器")
    parser.add_argument("--port", type=int, default=7860, help="端口号（默认 7860）")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    args = parser.parse_args()

    print(f"\n启动中 → http://localhost:{args.port}/  或  http://0.0.0.0:{args.port}/\n")
    app.run(host="0.0.0.0", port=args.port, debug=args.debug)
