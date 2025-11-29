import os
import json

from typing import List, Dict

from dotenv import load_dotenv

from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GENAI_API_KEY")

def process_event_data(raw_data: List[Dict]) -> List[Dict]:

    prompt_template = f"""
    我将给你一个包含 Pokémon GO 活动数据的 JSON 格式列表。
    我的目标是执行以下数据清理和时间点精确化操作：

    1.  **时间点分解 (提取子事件):** 仔细阅读每个活动字典中的 `description` 字段。如果描述文本中明确列出了特定日期或短时间窗口的子事件（例如："每周周末的影子突袭" 或 "连续三天的城市活动"），请将这些子事件分解成列表中独立的、时间精确的新条目。
    2.  **数据保留:** 对于通过分解创建的新条目，请将 `name` 字段更新为更具体的名称（例如：原名 + "(第一天)"），并使用从描述中提取或推断出的精确 `start` 和 `end` 时间替换原始的时间字段。
    3.  **移除容器事件:** 在完成分解后，请移除那些时间跨度很大、仅作为容器或系列事件使用的原始条目（例如：整个季度/赛季的活动，或描述中列出了具体子日期但本身时间范围很广的事件）。
    4.  **保留精确事件:** 对于本身已经拥有精确开始和结束时间，且描述中没有列出额外子日期需要分解的事件（例如：聚光灯小时、突袭日），请保持其原样，但确保其 `description` 字段中与时间相关的细节被简化或整合。
    5.  **输出格式:** 最终结果必须只包含一个新的、经过处理的 JSON 格式列表，并且不包含任何解释性的文字或注释。不需要使用 Markdown 代码块来包裹输出文本。

    **数据输入:**
    {json.dumps(raw_data, ensure_ascii=False, indent=2)}
    """

    client = genai.Client(api_key=api_key)
    print("🚀 Sending request to Gemini API...")
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt_template,
        config=types.GenerateContentConfig(
            temperature=0.1
        )
    )

    return json.loads(response.text)
