import re
from core.llm_config import llm
from orchestrator.state import SAOS_State

def coder_node(state: SAOS_State) -> dict:
    print("\n[Coder Agent] Đang suy nghĩ và sinh mã...")
    prompt = state.get("user_prompt", "")
    error = state.get("error_traceback", "")

    # Khung mớm lời (Framework Context)
    system_msg = "Bạn là một Python Coder thực thi nhiệm vụ. CHỈ trả về mã Python thuần túy nằm trong block ```python ... ```. Không giải thích, không mở bài kết bài."
    
    if error:
        system_msg += f"\nLƯU Ý: Lần chạy trước code của bạn đã văng lỗi sau. Hãy đọc kỹ Traceback và sửa code:\n{error}"

    messages = [
        ("system", system_msg),
        ("human", prompt)
    ]

    # Gọi API
    response = llm.invoke(messages)
    content = response.content

    # Trích xuất code bằng Regex
    code_match = re.search(r'```python\n(.*?)\n```', content, re.DOTALL)
    if code_match:
        code = code_match.group(1)
    else:
        # Fallback nếu AI quên bọc code
        code = content.replace('```python', '').replace('```', '').strip()

    print("[Coder Agent] Đã viết xong code!")
    return {"generated_code": code}