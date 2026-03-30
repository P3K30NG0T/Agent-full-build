import pandas as pd
from rich.console import Console
from rich.table import Table

# 1. Tạo dữ liệu giả lập
data = {
    'Month': ['Tháng 1', 'Tháng 2', 'Tháng 3'],
    'Store A': [500, 600, 750],
    'Store B': [400, 450, 400],
    'Store C': [800, 850, 900]
}
df = pd.DataFrame(data)

# 2. Tính tổng doanh thu từng cửa hàng
# Chỉ lấy các cột Store để tính tổng
totals = df[['Store A', 'Store B', 'Store C']].sum()

# 3. Hiển thị báo cáo bằng Rich
console = Console()

console.print("\n========== BÁO CÁO PHÂN TÍCH DOANH THU ==========")

table = Table(title="Tổng Kết Doanh Thu Quý 1", show_header=True, header_style="bold magenta")
table.add_column("Tên Cửa Hàng", style="cyan", width=15)
table.add_column("Tổng Doanh Thu (USD)", justify="right", style="green")

for store, total in totals.items():
    table.add_row(store, f"{total:,}")

console.print(table)
console.print("=================================================\n")
console.print("Hệ thống TOM S-AOS: Hoàn tất xử lý dữ liệu.")