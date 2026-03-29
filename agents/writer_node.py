from orchestrator.state import SAOS_State
from core.llm_config import llm

def writer_node(state: SAOS_State) -> dict:
    print("\n[📝] WRITER NODE ĐANG VIẾT BÁO CÁO TỔNG KẾT...")
    
    error = state.get("error_traceback", "")
    is_success = not bool(error)
    
    # 1. Bóc tách lịch sử an toàn (Vá lỗi KeyError)
    history_list = []
    for h in state.get('history', []):
        err_msg = str(h.get('error', ''))[:50]
        act_msg = h.get('action', 'N/A')
        history_list.append(f"Loop {h.get('loop', '?')}: Lỗi '{err_msg}' -> Giải pháp: {act_msg}")
    
    history_str = "\n".join(history_list)
    
    # 2. Phân loại kịch bản để viết Prompt
    if is_success:
        prompt = f"""Code đã chạy thành công sau {state.get('loop_count', 0)} lần. 
        Lịch sử:
        {history_str}
        
        Hãy tóm tắt cách bạn đã giải quyết, và đánh giá xem hệ thống tổng thể chạy đoạn code này thế nào. Trình bày ngắn gọn, rõ ràng."""
        title = "BÁO CÁO THÀNH CÔNG"
    else:
        prompt = f"""Code THẤT BẠI sau 4 lần thử. 
        Lịch sử:
        {history_str}
        Lỗi cuối cùng:
        {error}
        
        Hãy viết Post-Mortem Report: 1. Tóm tắt các lỗi gặp phải. 2. Phân tích nguyên nhân và cách bạn đã thử sửa. 3. Đề xuất giải pháp."""
        title = "BÁO CÁO THẤT BẠI (POST-MORTEM)"

    # 3. Gọi LLM sinh báo cáo
    report_content = llm.invoke([("human", prompt)]).content

    # 4. In ấn đẹp đẽ ra Terminal
    print("\n" + "="*60)
    print(f"📋 {title}")
    print("="*60)
    print(report_content)
    print("="*60 + "\n")
    
    # 5. Cập nhật State hợp lệ (Chỉ có Node mới được làm việc này)
    return {"final_report": report_content}