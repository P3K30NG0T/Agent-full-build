import docker
import os
import tempfile

def run_code_in_docker(code_string):
    """Chạy mã Python an toàn qua Docker container"""
    client = None
    temp_path = None
    
    try:
        client = docker.from_env()
        host_workspace = os.getcwd()
        container_workspace = '/workspace'

        # 1. Tạo file python tạm thời trong workspace hiện tại
        with tempfile.NamedTemporaryFile(dir=host_workspace, mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(code_string)
            temp_filename = os.path.basename(f.name)
            temp_path = f.name

        # 2. Khởi chạy Docker và thực thi file vừa tạo
        output_bytes = client.containers.run(
            image='python:3.10-slim',
            command=f"python {temp_filename}", # Gọi chạy file thay vì chạy chuỗi
            volumes={host_workspace: {'bind': container_workspace, 'mode': 'rw'}},
            working_dir=container_workspace,
            remove=True,
            stderr=True,
            stdout=True
        )
        
        return {"success": True, "output": output_bytes.decode('utf-8')}

    except docker.errors.ContainerError as e:
        # Code bị lỗi (Syntax, Runtime...)
        stderr_text = e.stderr.decode('utf-8') if e.stderr else str(e)
        return {"success": False, "error": stderr_text}
    except Exception as e:
        # Lỗi hệ thống Docker
        return {"success": False, "error": f"Lỗi hệ thống Docker: {str(e)}"}
    finally:
        # 3. Dọn dẹp chiến trường
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        if client:
            client.close()