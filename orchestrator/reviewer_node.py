from core.basic_sandbox import execute_code
from orchestrator.state import SAOS_State

def sandbox_node(state: SAOS_State) -> dict:
    print("\n[Sandbox Node] Nhận code. Đang khởi chạy...")
    code = state.get("generated_code", "")
    current_loop = state.get("loop_count", 0)
    
    if not code:
        return {"error_traceback": "Không có code để chạy."}

    result = execute_code(code)
    
    if result["success"]:
        print("[Sandbox Node] ✅ Chạy mượt mà, không có lỗi!")
        return {
            "execution_result": result["output"], 
            "error_traceback": "",
            "loop_count": current_loop + 1
        }
    else:
        # Chỉ in ra 200 ký tự đầu của lỗi cho gọn Terminal
        print(f"[Sandbox Node] ❌ LỖI VĂNG RA: {result['error'][:200]}...")
        return {
            "execution_result": "", 
            "error_traceback": result["error"],
            "loop_count": current_loop + 1
        }

def should_continue(state: SAOS_State) -> str:
    """Hàm dẫn đường cho LangGraph"""
    error = state.get("error_traceback", "")
    loop_count = state.get("loop_count", 0)

    if error and loop_count < 3:
        print(f"[Reviewer] ⚠️ Phát hiện lỗi! Đẩy Khay hồ sơ về lại Coder (Chu kỳ: {loop_count+1}/3)")
        return "coder_node"
    else:
        if error:
            print("[Reviewer] 🚨 Quá 3 lần thử vẫn lỗi. DỪNG HỆ THỐNG.")
        else:
            print("[Reviewer] 🎉 Code hoàn hảo. NHIỆM VỤ HOÀN THÀNH.")
        return "__end__"