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
        "user_prompt": """Hãy viết một đoạn code Python thực hiện 2 việc: 
Yêu cầu:
1. In ra dòng chữ 'Hello from Docker!'.
2. Dùng thư viện `os` để lấy và in ra tên của hệ điều hành đang chạy code này (dùng os.name hoặc platform.system()).""",
        "execution_result": "",
        "error_traceback": "",
        "loop_count": 0,
        "history": []
    }

    for event in app.stream(initial_state):
        pass
    
    print(f"\n💻 [KẾT QUẢ TỪ DOCKER]:\n{initial_state.get('execution_result', 'Không có output')}")
    print("="*60)
    print("🏁 QUÁ TRÌNH THỰC THI KẾT THÚC.")