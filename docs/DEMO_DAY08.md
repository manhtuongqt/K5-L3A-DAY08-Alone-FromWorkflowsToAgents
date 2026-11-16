# Demo Day08 khoảng 4 phút

Chạy trong src, dùng .venv/Scripts/python.exe trên Windows. Các lệnh dưới tạo DB riêng; chạy lại cùng DB là retry thật, không phải lần chạy mới. Trace ở src/traces không commit.

## 1. Workflow trả tiền đúng

```powershell
.venv/Scripts/python.exe -m lab8.run --shape workflow --claim-id C-001 --seed 11 --db data/demo_ok.sqlite
Get-Content traces/R-workflow-C-001-s11.json -Encoding UTF8
```

Giải thích order có cấu trúc → quote 35.000 → host → một effect. Không để model tính tiền.

## 2. Ticket không phải sự thật

```powershell
.venv/Scripts/python.exe -m lab8.run --shape workflow --claim-id C-002 --seed 55 --db data/demo_ticket.sqlite
.venv/Scripts/python.exe -m lab8.run --shape swarm --claim-id C-002 --seed 55 --db data/demo_swarm.sqlite
```

Workflow denied vì order trễ 2 ngày; swarm reference tin 5 ngày trong ticket. Mở benchmark.json trial C-002/s55 để thấy lỗi được giữ lại.

## 3. Handoff chỉ đọc

```powershell
.venv/Scripts/python.exe -m lab8.run --shape orchestrator --claim-id C-001 --seed 11 --db data/demo_handoff.sqlite
Get-Content traces/R-orchestrator-C-001-s11.json -Encoding UTF8
```

Chỉ field allowlist, không parent_secret/header/ticket; investigator không có issue_refund.

## 4. Crash rồi resume

```powershell
.venv/Scripts/python.exe -m lab8.run --shape workflow --claim-id C-012 --seed 11 --db data/demo_crash.sqlite --crash-at after_effect_before_checkpoint
.venv/Scripts/python.exe -m lab8.run --shape workflow --claim-id C-012 --seed 11 --db data/demo_crash.sqlite
```

Lệnh đầu cố ý crash, lệnh sau dùng đúng DB cũ: effect và committed audit vẫn một. Dùng tên DB chưa tồn tại để trình bày crash lần đầu; nếu đã demo trước, đổi tên DB cho cả hai lệnh, không xóa bằng chứng cũ.

## Kết luận

Workflow/single/orchestrator public đều 70/70 nhưng workflow rẻ nhất; swarm 69/70. Cost mô phỏng, latency unavailable; chưa kết luận hidden hay production. Ablation bỏ draft chỉ kiểm quyết định nghiệp vụ, không chấm chất lượng lời đáp.
