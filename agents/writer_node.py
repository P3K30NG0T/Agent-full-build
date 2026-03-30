import os
import re
from pydantic import BaseModel, Field
from core.llm_config import llm
from orchestrator.state import SAOS_State

# 1. ĐÚC KHUNG BÁO CÁO (PYDANTIC)
class ReportOutput(BaseModel):
    status: str = Field(description="Ghi rõ 'SUCCESS (Vòng X)' hoặc 'FAILED'")
    root_cause: str = Field(description="Nguyên nhân gốc rễ ngắn gọn (Ví dụ: Lỗi NameResolutionError do Docker mất mạng)")
    action_taken: str = Field(description="Hành động đã làm để sửa (hoặc gợi ý cho user nếu thất bại)")

def writer_node(state: SAOS_State) -> dict:
    print("\n[📝] WRITER NODE ĐANG TỔNG HỢP DEBUG LOG (Pydantic Mode)...")
    code = state.get("generated_code", "")
    prompt_text = state.get("user_prompt", "")
    
    # --- PHẦN 1: XUẤT FILE ---
    filename_match = re.search(r'([a-zA-Z0-9_/\\]+\.py)', prompt_text)
    filepath = filename_match.group(1) if filename_match else "output_module.py"
    
    folder = os.path.dirname(filepath)
    if folder:
        os.makedirs(folder, exist_ok=True)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"   [📦] Đã lưu file code tại: {filepath}")

    # --- PHẦN 2: ÉP KHUNG BÁO CÁO ---
    raw_errors = []
    for item in state.get("history", []):
        if item.get("error"):
            err_snippet = str(item['error'])[-300:] 
            raw_errors.append(f"- Loop {item['loop']}:\n{err_snippet}")
            
    error_log_str = "\n".join(raw_errors) if raw_errors else "Không có lỗi."
    
    prompt = f"""
    Dựa vào lịch sử này, hãy điền vào Form báo cáo.
    Số vòng lặp: {state.get("loop_count", 0)}
    Lịch sử lỗi: {error_log_str}
    """
    
    # Sử dụng Pydantic để ép LLM trả về đúng Object
    structured_llm = llm.with_structured_output(ReportOutput)
    report: ReportOutput = structured_llm.invoke([("human", prompt)])
    
    # In ra Terminal với format cố định (Không cho LLM tự vẽ format nữa)
    report_string = f"""
============================================================
📋 BÁO CÁO KỸ THUẬT (DEBUG LOG)
============================================================
* STATUS     : {report.status}
* ROOT CAUSE : {report.root_cause}
* FIX/ACTION : {report.action_taken}
============================================================
"""
    # Lưu vào state để hiển thị
    state["final_report"] = report_string
    print(report_string)
    
    return {"final_report": report_string}