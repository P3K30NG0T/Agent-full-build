from core.llm_config import llm
from orchestrator.state import SAOS_State
from pydantic import BaseModel, Field

# 1. KHUÔN ĐÚC MỚI (Dành cho Debugger)
class TomOutput(BaseModel):
    diagnosis: str = Field(description="Chẩn đoán ngắn gọn (1 câu) nguyên nhân gốc rễ của lỗi hoặc mục tiêu cốt lõi.")
    plan: str = Field(description="Các bước hành động gạch đầu dòng ngắn gọn.")
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

    system_msg = "Bạn là Tom, một Senior Python Developer. Hãy viết code giải quyết vấn đề."
    if error:
        system_msg += f"\nLỖI LẦN TRƯỚC:\n{error}\nHãy đọc Traceback và sửa lỗi."

    messages = [("system", system_msg), ("human", prompt)]

    structured_llm = llm.with_structured_output(TomOutput)
    response: TomOutput = structured_llm.invoke(messages)

    # In ra Terminal theo format chuẩn để copy-paste
    print(f"🔎 DIAGNOSIS: {response.diagnosis}")
    print(f"🛠️ PLAN: {response.plan}")
    print("-" * 40)

    new_history = history + [{
        "loop": loop, 
        "diagnosis": response.diagnosis, 
        "plan": response.plan, 
        "error": error
    }]

    return {"generated_code": response.code, "history": new_history}