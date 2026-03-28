from langgraph.graph import StateGraph, END
from orchestrator.state import SAOS_State
from agents.coder_node import coder_node
from orchestrator.reviewer_node import sandbox_node, should_continue

# 1. Khởi tạo Bàn cờ LangGraph với cấu trúc Khay hồ sơ
workflow = StateGraph(SAOS_State)

# 2. Định nghĩa các Trạm (Nodes)
workflow.add_node("coder", coder_node)
workflow.add_node("sandbox", sandbox_node)

# 3. Kẻ đường đi (Edges)
workflow.set_entry_point("coder")           # Điểm bắt đầu
workflow.add_edge("coder", "sandbox")       # Coder viết xong -> Ném qua Sandbox chạy

# Thêm ngã ba điều kiện ở Sandbox
workflow.add_conditional_edges(
    "sandbox",
    should_continue,
    {
        "coder_node": "coder", # Nếu lỗi -> Quay lại Coder
        "__end__": END         # Nếu xong hoặc quá số lần -> Dừng
    }
)

# 4. Đóng gói hệ thống
app = workflow.compile()

# ==========================================
# BÀI TEST SỐ 1: KHỞI CHẠY "HELLO WORLD"
# ==========================================
if __name__ == "__main__":
    print("\n🚀 [SYSTEM] KÍCH HOẠT S-AOS BOT ĐÀN EM (V1) 🚀")
    print("="*60)
    
    # Khởi tạo dữ liệu ban đầu cho Khay hồ sơ
    initial_state = {
        "user_prompt": "Viết mã Python dùng thư viện openpyxl tạo file 'test_bot.xlsx'. Điền dòng chữ 'Bot Đàn Em đã sống!' vào ô A1. Sau đó in ra Terminal dòng chữ 'DONE_EXCEL'.",
        "generated_code": "",
        "execution_result": "",
        "error_traceback": "",
        "loop_count": 0
    }

    # Kích hoạt luồng chạy
    for event in app.stream(initial_state):
        for key, value in event.items():
            pass # Các Node đã tự in log, ta không cần in thêm ở đây
    
    print("="*60)
    print("🏁 QUÁ TRÌNH THỰC THI KẾT THÚC.")