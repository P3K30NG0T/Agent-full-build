import subprocess
import os
import tempfile
import sys

def execute_code(code: str) -> dict:
    # 1. Tạo file python tạm thời
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(code)
        temp_path = f.name

    try:
        # 2. Bóp cò chạy code và chờ tối đa 30s

        result = subprocess.run(
            [sys.executable, temp_path], 
            capture_output=True,
            text=True
        )
        
        # 3. Đánh giá kết quả (Mã 0 là thành công)
        if result.returncode == 0:
            return {"success": True, "output": result.stdout}
        else:
            return {"success": False, "error": result.stderr}
            
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Lỗi: Code chạy quá 30 giây (Có thể bị lặp vô hạn)."}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        # 4. Xóa dấu vết
        if os.path.exists(temp_path):
            os.remove(temp_path)