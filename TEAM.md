# Team

## Thông tin nhóm

- Tên nhóm: NguyenManhTuong (nhóm một thành viên)
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY08-NguyenManhTuong-FromWorkflowsToAgents`
- URL repo, nhánh nộp, commit chốt: https://github.com/manhtuongqt/K5-L3A-DAY08-NguyenManhTuong-FromWorkflowsToAgents ; main; commit kỹ thuật xem ADR.

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
| 1 | Nguyễn Mạnh Tường | 2A202603646 | Chưa cung cấp | manhtuongqt | Phụ trách bài nhóm một người; dùng Codex hỗ trợ triển khai và kiểm chứng kỹ thuật |

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Nguyễn Mạnh Tường | Tích hợp shape, test, benchmark và báo cáo; Codex hỗ trợ code/thực thi | b1120c2aeb12e2e0a185693d4abd6b766a10d4f5 | src/tests/test_team_safety.py: 15 test bổ sung cho crash, injection, handoff, loop và ablation |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## 2A202603646_NguyenManhTuong

### Phần việc phụ trách

- Ba shape, test an toàn, đo so sánh và báo cáo.

### Đóng góp cụ thể

- Phạm vi và công cụ AI được ghi trong [báo cáo cá nhân](report/team/2A202603646_NguyenManhTuong.md); không khai báo thành viên giả.

### Bằng chứng

- `src/reports/benchmark.json`, `crash.json`, `research_ablation.json`, `verification.json` và commit kỹ thuật trong ADR.
