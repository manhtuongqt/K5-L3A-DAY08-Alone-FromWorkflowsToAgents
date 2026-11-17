# Bài làm Day09 — Alone

Nguyễn Mạnh Tường — 2A202603646. Đây là phần bổ sung Day09 trong repo Day08 đúng hướng dẫn overlay; thư mục src/lab8/ và tài liệu gốc Day08 được giữ nguyên.

## Đọc theo thứ tự

1. [Taxonomy](failure_taxonomy.md): lỗi nào, bằng chứng đâu, dùng grader gì.
2. [Trace case](trace_case.md): C-002 sai lần đầu ở event 3, có đối chứng và regression test.
3. [Judge audit](judge_audit.md): tone được dùng, helpful bị loại; người học đã đối chiếu.
4. [Eval card](eval_card.md): số liệu v1/v2, CI, slice, reliability, giới hạn.
5. [PRD v1.1](PRD_v1.1.md): định nghĩa chạy đúng, gate owner và phạm vi pilot.
6. [Đối chiếu yêu cầu](DOI_CHIEU_YEU_CAU_DAY09.md): vị trí từng artifact.

## Chạy lại

Python ≥3.11, từ src/:
- python -m pip install -r requirements.txt -r requirements-lab9.txt
- python -m lab9.verify_submission --phase core
- python -m lab9.verify_submission --phase advanced
- python -m lab9.verify_submission --phase final
- python -m lab9.check_sources

Các lệnh verification chạy thí nghiệm thật, sinh JSON và lưu stdout/stderr/exit code tại docs/evidence/day09/. Không cần API key, Docker hoặc model thật. Lưu ý helpful và các candidate/trap lỗi cần exit 1; đó là kết quả mong đợi chứ không phải tất cả lệnh đều phải exit 0.

Report chỉ do script sinh. Những số tiền/secret/PII trong public fixture là dữ liệu giả lập của đề. Không đưa khóa thật vào repo.

## Kết quả chính

- V1: swarm 69/70; fixed 70/70; seeded_regression 50/70.
- V2: swarm 137/140; fixed và honest_refactor 140/140.
- Mutation 3/3, false alarm 0.
- Cả bốn trap public bị chặn; baseline tự so chính nó vẫn merge.
- Detection sau cải tiến grader 100%, false alarm 0%.
- Audit judge đã được Nguyễn Mạnh Tường đối chiếu; giữ nguyên CSV nguồn.

## Lỗi đã phát hiện và sửa

1. Chấm ledger không giải thích được proposal bị tự trừ trước ở C-013: thêm metric ProposalAmountCorrect; detection từ 75% lên 100%.
2. Test thêm variant làm ảnh hưởng registry của test Day08 khi chạy chung: fixture test mới khôi phục registry sau mỗi test, không sửa Lab08.
3. Hash eval-set khác Windows/Linux vì CRLF/LF: generator ghi LF và Git cố định LF cho eval-set JSONL. Sinh lại toàn bộ report bằng script, không đổi ngưỡng hoặc sửa số JSON.

Bộ CI gốc Day08 và workflow eval-gate của đề được giữ nguyên. Workflow bổ sung kiểm toàn bộ test, nguồn bất biến, ratchet với base-spec của PR và traps. Trạng thái cuối xem tab Checks trên PR starter/d09, không lấy một job bị skip làm bằng chứng hoàn thành Advanced.

## Phân công và AI hỗ trợ

Nhóm Alone có một người học: Nguyễn Mạnh Tường, phụ trách bài và quyết định nộp. Codex hỗ trợ triển khai code, chạy kiểm thử/thí nghiệm, phân tích và soạn báo cáo. Người học đã xác nhận audit judge ngày 17/11/2026. Việc xác nhận này không được mô tả thành tự viết độc lập mọi dòng code hoặc kiểm chứng model/người dùng thật.

## Nộp

Nộp link PR starter/d09 → main của repo nhóm theo SUBMISSION Day09; mô tả PR phải có output gate regression, mutation, A/A và bốn trap. Hạn nộp đối chiếu LMS/lịch lớp; không suy ra từ ngày clone repo. Tôi tự nộp LMS.
