from langgraph.graph import StateGraph, END
from orchestrator.state import SAOS_State
from agents.coder_node import coder_node
from orchestrator.reviewer_node import sandbox_node, should_continue
from agents.writer_node import writer_node # [MỚI]

# 1. Khởi tạo Bàn cờ LangGraph
workflow = StateGraph(SAOS_State)

# 2. Định nghĩa Trạm
workflow.add_node("coder", coder_node)
workflow.add_node("sandbox", sandbox_node)
workflow.add_node("writer", writer_node) # [MỚI]

# 3. Kẻ đường
workflow.set_entry_point("coder")
workflow.add_edge("coder", "sandbox")

# ... (Giữ nguyên phần trên) ...

# Trạm KCS: Sửa lại lối đi (Cả Thành công lẫn Thất bại đều dồn về Writer)
workflow.add_conditional_edges(
    "sandbox",
    should_continue,
    {
        "coder_node": "coder", 
        "writer_node": "writer" # Đón cả 2 case về đây
    }
)

workflow.add_edge("writer", END) # Viết xong báo cáo thì đóng gói nghỉ ngơi

app = workflow.compile()
# ... (Giữ nguyên phần dưới) ...

if __name__ == "__main__":
    print("\n🚀 [SYSTEM] KÍCH HOẠT TOM V2 (BUILDER MODE) 🚀")
    print("="*60)
    
    # GIAO TASK: Bắt Tom tự xây Sandbox Docker cho tương lai!
    initial_state = {
        "user_prompt": """Hãy viết một đoạn code Python thực hiện phân tích dữ liệu giả lập.
        YÊU CẦU:
        1. Tạo một DataFrame bằng thư viện `pandas` chứa dữ liệu doanh thu của 3 cửa hàng:
           - Store A: 500, 600, 750 (tháng 1, 2, 3)
           - Store B: 400, 450, 400
           - Store C: 800, 850, 900
        2. Tính tổng doanh thu của từng cửa hàng.
        3. Sử dụng thư viện `rich` để in một bảng (Table) thật đẹp báo cáo tổng doanh thu này.
        4. KHÔNG DÙNG Internet, KHÔNG gọi API.""",
        "generated_code": "",
        "execution_result": "",
        "error_traceback": "",
        "loop_count": 0,
        "history": [],
        "required_libs": [],
        "scratchpad": [],
        "task_type": ""
    }

    # Tạo một biến để hứng State cuối cùng
    final_state = initial_state.copy()
    
    for event in app.stream(initial_state):
        for node_name, value in event.items():
            # 2. Quan trọng: Gộp (Merge) dữ liệu mới vào Khay hồ sơ thay vì chép đè
            final_state.update(value) 
    
    print("="*60)
    # 3. Bây giờ ta lấy kết quả từ final_state đã được tổng hợp đầy đủ
    output = final_state.get('execution_result', 'Không có output')
    print(f"💻 [KẾT QUẢ TỪ DOCKER]:\n{output}")
    print("="*60)
    print("🏁 QUÁ TRÌNH THỰC THI KẾT THÚC.")