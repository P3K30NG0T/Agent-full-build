import docker
import os
import tempfile

def run_code_in_docker(code_string, required_libs=None):
    client = None
    temp_path = None
    try:
        client = docker.from_env()
        host_workspace = os.getcwd()

        with tempfile.NamedTemporaryFile(dir=host_workspace, mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(code_string)
            temp_filename = os.path.basename(f.name)
            temp_path = f.name

        # [CẢI TIẾN] Tạo lệnh cài đặt và chạy rõ ràng
        if required_libs:
            libs_to_install = " ".join(required_libs)
            # Dùng 2>/dev/null để nuốt luôn các dòng WARNING rác
            cmd = f"python -m pip install -q --no-cache-dir --disable-pip-version-check {libs_to_install} 2>/dev/null && python {temp_filename}"
        else:
            cmd = f"python {temp_filename}"
            
        print(f"   [DOCKER_LOG] Đang thực thi lệnh: {cmd}")

        output_bytes = client.containers.run(
            image='python:3.10-slim',
            command=["sh", "-c", cmd], # Dùng List để tránh lỗi Quoting trên Windows
            volumes={host_workspace: {'bind': '/workspace', 'mode': 'rw'}},
            working_dir='/workspace',
            remove=True,
            stdout=True,
            stderr=True,
            network_mode='host'
            #dns=['8.8.8.8']
        )
        return {"success": True, "output": output_bytes.decode('utf-8')}
    # ... (giữ nguyên phần except và finally)

    except docker.errors.ContainerError as e:
        stderr_text = e.stderr.decode('utf-8') if e.stderr else str(e)
        return {"success": False, "error": stderr_text}
    except Exception as e:
        return {"success": False, "error": f"Lỗi hệ thống Docker: {str(e)}"}
    finally:
        # 4. Dọn dẹp
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        if client:
            client.close()