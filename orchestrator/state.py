from typing import TypedDict, List, Dict

class SAOS_State(TypedDict):
    """Khay hồ sơ lưu trữ trạng thái của luồng thực thi"""
    user_prompt: str
    generated_code: str
    execution_result: str
    error_traceback: str
    loop_count: int
    history: List[Dict[str, str]] # [MỚI] Lưu lịch sử: {"loop": 1, "thought": "...", "error": "..."}
    final_report: str             # [MỚI] Báo cáo tổng kết cuối cùng