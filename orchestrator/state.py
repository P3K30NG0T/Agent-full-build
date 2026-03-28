from typing import TypedDict

class SAOS_State(TypedDict):
    """Khay hồ sơ lưu trữ trạng thái của luồng thực thi"""
    user_prompt: str
    generated_code: str
    execution_result: str
    error_traceback: str
    loop_count: int