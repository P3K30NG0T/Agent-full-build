from core.docker_manager import run_code_in_docker # [MỚI] Gọi từ lõi Docker
from orchestrator.state import SAOS_State
from core.llm_config import llm

def sandbox_node(state: SAOS_State) -> dict:
    print("🐳 [DOCKER] ĐANG KHỞI TẠO CONTAINER & CHẠY CODE...")
    code = state.get("generated_code", "")
    current_loop = state.get("loop_count", 0)
    
    # [THAY TIM] Sử dụng hàm Docker chuẩn Enterprise
    result = run_code_in_docker(code) 
    
    if result["success"]:
        print("✅ [DOCKER STATUS] SUCCESS!")
        return {"execution_result": result["output"], "error_traceback": "", "loop_count": current_loop + 1}
    else:
        err_msg = result['error']
        print(f"❌ [DOCKER STATUS] FAILED. Error snippet: {err_msg[:200]}...")
        return {"execution_result": "", "error_traceback": result["error"], "loop_count": current_loop + 1}

# ... (Giữ nguyên các hàm generate_report và should_continue ở bên dưới) ...

def generate_report(state: SAOS_State, is_success: bool) -> str:
    print("\n[📝] TOM ĐANG VIẾT BÁO CÁO TỔNG KẾT...")
    history_str = "\n".join([f"Loop {h['loop']}: Lỗi '{h['error'][:50]}' -> Giải pháp: {h['action']}" for h in state['history']])
    
    if is_success:
        prompt = f"Code đã chạy thành công sau {state['loop_count']} lần. Lịch sử:\n{history_str}\nHãy tóm tắt cách bạn đã giải quyết, và đánh giá xem hệ thống tổng thể chạy đoạn code này thế nào. Trình bày ngắn gọn, rõ ràng."
    else:
        prompt = f"Code THẤT BẠI sau 4 lần thử. Lịch sử:\n{history_str}\nLỗi cuối cùng:\n{state['error_traceback']}\nHãy viết Post-Mortem Report: 1. Tóm tắt các lỗi gặp phải. 2. Phân tích nguyên nhân và cách bạn đã thử sửa từng loop. 3. Kết luận lý do thất bại cuối cùng và đề xuất giải pháp cho người dùng."

    return llm.invoke([("human", prompt)]).content

# ... (Giữ nguyên phần sandbox_node) ...

def should_continue(state: SAOS_State) -> str:
    error = state.get("error_traceback", "")
    loop_count = state.get("loop_count", 0)

    if error:
        if loop_count < 4:
            return "coder_node"
        else:
            print("\n🚨 TOM ĐÃ ĐẦU HÀNG SAU 4 LẦN THỬ! Đang chuyển hồ sơ sang Trạm Báo Cáo...")
            # Chỉ trả về tên Node tiếp theo, KHÔNG gọi generate_report ở đây
            return "writer_node"
    else:
        print("\n🎉 CODE CHẠY THÀNH CÔNG! Đang chuyển hồ sơ sang Trạm Báo Cáo...")
        return "writer_node"