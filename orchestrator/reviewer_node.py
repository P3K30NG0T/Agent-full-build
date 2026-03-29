from core.docker_manager import run_code_in_docker # [MỚI] Gọi từ lõi Docker
from orchestrator.state import SAOS_State
from core.llm_config import llm

def sandbox_node(state: SAOS_State) -> dict:
    print("🐳 [DOCKER] ĐANG KHỞI TẠO CONTAINER & CHẠY CODE...")
    code = state.get("generated_code", "")
    libs = state.get("required_libs", []) # [MỚI] Rút danh sách thư viện
    current_loop = state.get("loop_count", 0)
    
    # [THAY TIM] Sử dụng hàm Docker chuẩn Enterprise
    result = run_code_in_docker(code, required_libs=libs) 
    
# ... trong hàm sandbox_node
    if result["success"]:
        print("✅ [DOCKER STATUS] SUCCESS!")
        return {"execution_result": result["output"], "error_traceback": "", "loop_count": current_loop + 1}
    else:
        err_msg = result['error']
        print(f"❌ [DOCKER STATUS] FAILED. Lỗi: {err_msg[:100]}...")
        # Cập nhật error_traceback ĐẦY ĐỦ để vòng lặp sau và Trạm báo cáo có cái để đọc
        return {"execution_result": "", "error_traceback": err_msg, "loop_count": current_loop + 1}

# ... (Giữ nguyên các hàm generate_report và should_continue ở bên dưới) ...

def generate_report(state: SAOS_State, is_success: bool) -> str:
    # Nếu dòng chữ này hiện lên, nghĩa là code mới ĐÃ ĂN
    print("\n[📝] TRẠM KCS ĐANG TỔNG HỢP DEBUG LOG...") 
    
    # 1. Trích xuất toàn bộ lỗi thô từ History
    raw_errors = []
    for item in state.get("history", []):
        if item.get("error"):
            # Lấy 500 ký tự cuối cùng của mỗi Traceback để tiết kiệm token
            err_snippet = str(item['error'])[-500:] 
            raw_errors.append(f"- Loop {item['loop']}:\n{err_snippet}")
            
    error_log_str = "\n".join(raw_errors) if raw_errors else "Không có lỗi (Chạy 1 phát ăn ngay)."

    status = "SUCCESS" if is_success else "FAILED"
    
    # 2. Prompt siêu tối giản, ép định dạng
    prompt = f"""
    Bạn là hệ thống System Admin của S-AOS. Hãy viết một báo cáo Debug NGẮN GỌN (tối đa 150 chữ).
    
    THÔNG TIN ĐẦU VÀO:
    - Trạng thái cuối: {status}
    - Số vòng lặp: {state.get("loop_count", 0)}
    - Lịch sử Lỗi (Raw Traceback):
    {error_log_str}
    
    YÊU CẦU BÁO CÁO:
    Không chào hỏi. Không giải thích lằng nhằng. Trả về đúng 3 mục sau:
    * STATUS: (Thành công ở vòng mấy / Thất bại)
    * ROOT CAUSE: (Tên lỗi kỹ thuật hoặc dòng code gây lỗi)
    * FIX APPLIED: (Hành động đã xử lý)
    """
    
    from core.llm_config import llm # Đảm bảo đã import llm
    messages = [("human", prompt)]
    response = llm.invoke(messages)
    return response.content

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