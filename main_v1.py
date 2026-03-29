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
        "user_prompt": """Bạn là Tom, một Senior Python Developer. 
    Nhiệm vụ của bạn là giải quyết yêu cầu và đảm bảo code CHẠY ĐƯỢC. Hãy lấy giá Bitcoin hiện tại từ Coindesk API. 
        Sau đó, giả sử tôi có 0.5 BTC, hãy tính giá trị tài sản của tôi theo USD.
        YÊU CẦU: Trình bày kết quả thật đẹp mắt, Hãy dùng thư viện rich để trình bày kết quả dưới dạng Table cho dễ đọc trong Terminal.
    
    QUY ĐỊNH BẮT BUỘC:
    1. Nếu code của bạn sử dụng bất kỳ thư viện ngoài nào (như requests, pandas, openpyxl...), bạn PHẢI liệt kê tên thư viện đó vào danh sách `required_libs`.
    2. Tuyệt đối không yêu cầu người dùng cài đặt thủ công. Hệ thống sẽ tự động cài chúng dựa trên danh sách bạn cung cấp.
    3. "QUY ĐỊNH: Bạn PHẢI sử dụng lệnh print() để in kết quả cuối cùng ra màn hình (stdout). Nếu không in, hệ thống sẽ coi như nhiệm vụ thất bại.""",
        "scratchpad": [], 
        "task_type": "", 
        "required_libs": [],
        "execution_result": "",
        "error_traceback": "",
        "loop_count": 0,
        "history": []
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