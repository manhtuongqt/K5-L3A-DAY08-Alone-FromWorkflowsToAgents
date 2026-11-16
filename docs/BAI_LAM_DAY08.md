# Bài làm Day08 — Nguyễn Mạnh Tường

Nhóm Alone, MSSV 2A202603646. Repo nhánh main; code bài chính xem ADR. Đã làm bài chính và mở rộng bonus B4; được cộng điểm hay không còn phụ thuộc gate hidden của giảng viên. Ablation research card ban đầu vẫn giữ riêng để đối chiếu.

## Cài và chạy

Từ gốc repo, Windows PowerShell:

```powershell
python -m venv src/.venv
src/.venv/Scripts/python.exe -m pip install -r src/requirements.txt
cd src
.venv/Scripts/python.exe -m lab8.smoke
.venv/Scripts/python.exe -m pytest -q
.venv/Scripts/python.exe -m pytest -q -m student -o addopts=
.venv/Scripts/python.exe -m lab8.crash_test --count 20 --out reports/crash.json
.venv/Scripts/python.exe -m lab8.benchmark --shapes workflow,single,orchestrator,swarm --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/benchmark.json
.venv/Scripts/python.exe -m lab8.benchmark --shapes workflow,workflow_no_draft --extra-shape workflow_no_draft=bonus.workflow_no_draft:run_claim --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/research_ablation.json
.venv/Scripts/python.exe -m bonus.verify_public
.venv/Scripts/python.exe -m bonus.run_b4
.venv/Scripts/python.exe -m bonus.verify_b4
.venv/Scripts/python.exe -m lab8.check_submission
```

macOS/Linux dùng python3 tạo venv, sau đó gọi .venv/bin/python thay .venv/Scripts/python.exe. Không có API key, Docker, model tải về hoặc dịch vụ ngoài trong runtime. Kiểm chứng hiện tại trên Windows/Python 3.11.9; không nhận đã tự chạy macOS/Linux.

## Đối chiếu checkpoint

| CP | Bằng chứng | Trạng thái |
| --- | --- | --- |
| CP1 | Smoke pass, host xanh, TEAM một người | Hoàn thành kỹ thuật |
| CP2 | 62 student test mỗi shape, 248 toàn ma trận | Đạt public |
| CP3 | T11/T12 và crash bổ sung; handoff chỉ tool đọc | Đạt public |
| CP4 | crash.json 20/20, public evaluator và test injection/approval | Đạt public; chưa xác nhận safety count hidden |
| CP5 | benchmark bốn shape, ablation, báo cáo, ADR, đóng góp, check_submission | Đủ hồ sơ kỹ thuật; gate hidden chờ giảng viên |

`check_submission` chỉ kiểm format và một số case public, không cấp điểm hidden. Gate ≥75% trên 200 hidden trial chưa xác nhận. Nếu được phát student_drop, đặt ở src/student_drop và chạy lệnh tự kiểm trong src/README.md; không commit thư mục đó. Người học tự đọc báo cáo cá nhân, chuẩn bị giải thích code và nộp link GitHub lên LMS.

## Bằng chứng

- [Đối chiếu toàn bộ yêu cầu và các phần còn chờ](DOI_CHIEU_YEU_CAU_DAY08.md): đủ tám tiêu chí rubric và checklist nộp.

- reports/benchmark.json và research_ablation.json: công cụ benchmark chính thức tạo.
- reports/crash.json: crash_test chính thức tạo, không sửa tay.
- reports/verification.json: smoke, test, replay benchmark và hash file host/config/data giữ nguyên.
- reports/benchmark_reproduced.json: benchmark lần hai độc lập, đối chiếu toàn bộ report.
- [Bonus B4](../report/team/bonus_report.md): reports/bonus_benchmark.json, bonus_ablation.json, bonus_verification.json; 9 test trong tests/test_bonus_b4.py.
- [Báo cáo nhóm](../report/team/group_report.md), [ADR](../report/team/decision_adr.md), [research card](../report/team/research_card.md), [cá nhân](../report/team/2A202603646_NguyenManhTuong.md).

JSON không sửa tay; trace/SQLite là đầu ra local bị ignore. Raw ticket và parent secret không có trong trace. Mọi con số cost là mô phỏng, không phải tiền API thực.
