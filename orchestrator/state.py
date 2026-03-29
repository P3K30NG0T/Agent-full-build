from typing import TypedDict, List, Dict, Any

class SAOS_State(TypedDict):
    """Khay hồ sơ lưu trữ trạng thái của luồng thực thi"""
    user_prompt: str
    generated_code: str
    execution_result: str
    error_traceback: str
    loop_count: int
    history: List[Dict[str, Any]]
    final_report: str
    
    # [MỚI THÊM]
    scratchpad: List[Dict[str, str]] 
    task_type: str                   
    required_libs: List[str]