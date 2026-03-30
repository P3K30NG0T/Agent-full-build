from core.llm_config import llm
from orchestrator.state import SAOS_State
from pydantic import BaseModel, Field

# 1. KHUÔN ĐÚC MỚI (Dành cho Debugger)
class TomOutput(BaseModel):
    diagnosis: str = Field(description="Chẩn đoán ngắn gọn (1 câu) nguyên nhân gốc rễ.")
    plan: str = Field(description="Các bước hành động gạch đầu dòng ngắn gọn.")
    required_libs: list[str] = Field(description="Danh sách thư viện cần cài (vd: ['pandas', 'requests']). Để trống [] nếu chỉ dùng thư viện chuẩn có sẵn của Python.") # [MỚI]
    code: str = Field(description="Mã Python thuần túy. KHÔNG bọc trong markdown.")

def coder_node(state: SAOS_State) -> dict:
    prompt = state.get("user_prompt", "")
    error = state.get("error_traceback", "")
    history = state.get("history", [])
    loop = state.get("loop_count", 0) + 1

    # Format lại Console Log để bạn dễ copy cho tôi
    print(f"\n" + "="*40)
    print(f"🔄 [LOOP {loop}/4] TOM'S EXECUTION LOG")
    print("="*40)

    system_msg = """BẠN LÀ TOM - HỆ THỐNG TỰ TRỊ S-AOS.
    
    QUY TẮC SINH TỒN:
    1. Kiểm tra kỹ xem code có dùng thư viện ngoài không. NẾU CÓ, PHẢI điền vào `required_libs`.
    2. Nếu CÓ, bạn BẮT BUỘC phải ghi tên thư viện đó vào danh sách `required_libs`. 
       - Ví dụ: required_libs = ["requests", "pandas"]
    3. [QUAN TRỌNG] NGUYÊN TẮC FAIL FAST: Tuyệt đối KHÔNG dùng try...except để in ra lỗi rồi kết thúc chương trình êm đẹp. Nếu gọi API thất bại hoặc tính toán sai, hãy dùng lệnh `raise` để quăng thẳng lỗi ra ngoài, HOẶC không dùng try...except. Hệ thống KCS cần bắt được Traceback (Crash) để đánh giá.
    4. TRÌNH BÀY KẾT QUẢ (Stdout): 
       - Kết quả in ra Terminal PHẢI được định dạng chuyên nghiệp.
       - Sử dụng các đường kẻ ngang (==========) để phân tách các phần.
       - Có tiêu đề rõ ràng cho từng loại dữ liệu.
       - Nếu là dữ liệu số/danh sách, hãy dùng bảng hoặc bullet points.
       - VÍ DỤ: 
         ========== BÁO CÁO GIÁ BITCOIN ==========
         - Nguồn: Coindesk API
         - Giá hiện tại: 65,000 USD
         =========================================
    """
    if error:
        system_msg += f"\nLỖI LẦN TRƯỚC:\n{error}\nHãy đọc Traceback và sửa lỗi."

    messages = [("system", system_msg), ("human", prompt)]

    structured_llm = llm.with_structured_output(TomOutput)
    response: TomOutput = structured_llm.invoke(messages)

    # In ra Terminal theo format chuẩn để copy-paste
    print(f"🔎 DIAGNOSIS: {response.diagnosis}")
    print(f"🛠️ PLAN: {response.plan}")
    print(f"📦 LIBS: {response.required_libs}") # [MỚI] In ra cho dễ theo dõi
    print("-" * 40)

    new_history = history + [{
        "loop": loop, 
        "diagnosis": response.diagnosis, 
        "plan": response.plan, 
        "error": error
    }]

    # Trả về thêm danh sách thư viện
    return {"generated_code": response.code, "history": new_history, "required_libs": response.required_libs}