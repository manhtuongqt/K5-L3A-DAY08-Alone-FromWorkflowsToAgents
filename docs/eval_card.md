# Eval card — Day09 Core

Nhóm Alone — Nguyễn Mạnh Tường — 2A202603646.

## Phiên bản và nguồn

- Nền Day08: cf413f3fff56015b2f16833989e5f1e9726fba26, src/lab8/ giữ nguyên.
- Overlay Day09: d1b9471540727d693c9eb392667b9f0d8a998bf5.
- Eval v1: SHA e0d63d30c41e; 14 item × 5 seed 11/22/33/44/55; labels_v1.json tách riêng.
- metric_spec_version=1.0; grader trong lab9/graders.py, thống kê trong lab9/stats.py.
- Môi trường chạy local: Python 3.11.9, pydantic-evals 2.68.0, MockLLM; judge replay, không gọi model API.
- Code/grader commit và kết quả CI cuối được ghi trong bảng đối chiếu Day09 sau khi chốt PR.

## Kết quả v1

| Metric | Baseline swarm | fixed | seeded_regression | Quy định |
|---|---:|---:|---:|---|
| approval_bypass | 0 | 0 | 0 | Blocking max 0 |
| secret_leak | 0 | 0 | 0 | Blocking max 0 |
| refund_amount_correct | 0.9857 | 1.0000 | 0.8571 | Blocking min 0.95 + no significant drop |
| pass_rate | 0.9857 | 1.0000 | 0.7143 | Blocking min 0.85 + no significant drop |
| reply_ledger_consistent | 1.0000 | 1.0000 | 0.7857 | Blocking min 1 |
| db_fact_kept | 0.9857 | 1.0000 | 0.9286 | Theo dõi min 0.95 |
| proposal_amount_correct | 0.9857 | 1.0000 | 0.7857 | Chẩn đoán min 0.95, không blocking |
| pass_5 | 0.9286 | 1.0000 | 0.7143 | Theo dõi min 0.80 |
| cost_per_success | 49.5670 | 48.7157 | 81.2020 | Chi phí mô phỏng, theo dõi tăng tối đa 10% |

Nguồn máy sinh: [baseline](../src/reports/baseline_v1.json), [fixed](../src/reports/eval_fixed.json), [regression](../src/reports/eval_seeded_regression.json). Run ID lần lượt E-swarm-20261117-e0d6, E-fixed-20261117-e0d6, E-seeded_regression-20261117-e0d6.

Delta pass_rate regression − baseline = −0.271; paired percentile CI 95% [−0.500, −0.057]. Cặp bootstrap là trung bình mỗi item qua năm seed, không phải 70 quan sát độc lập. Cấu hình 1000 resample, rng=2027. fixed và swarm PR merge; regression block vì refund_amount_correct, pass_rate, reply_ledger_consistent. [Log gate](evidence/day09/m4_gate_seeded_regression.txt).

## Judge, trace và phạm vi

Tone đạt κ=.757, P=.857, R=.8 trên replay; helpful bị loại κ=.375, R=.3 dù P=1. [Audit đã được người học đối chiếu](judge_audit.md). Tiền/phê duyệt không giao judge.

[Trace case](trace_case.md) chỉ rõ C-002 event 3 là bước sai đầu tiên, có test đối chứng. Chủ trì gate: Nguyễn Mạnh Tường. Exit 1 là không merge; cần tìm nguyên nhân, sửa lớp eval đúng phạm vi và chạy lại. Không hạ ngưỡng để lấy build xanh.

Pilot ở đây là đánh giá offline bài toán claim một đơn, approvals và mức tiền theo fixture. Chưa cho phép tác động tiền thật; chưa đo người dùng thật.

## Giới hạn

MockLLM deterministic không đại diện model thật. V1 chỉ 14 item, CI rộng; dữ liệu replay đã public không phải held-out mới. Metric reply_ledger_consistent kiểm tính nhất quán của số tiền quan sát được: swarm gốc không có reply event nên 1.0 không chứng minh toàn bộ trả lời đúng/đủ. Tiền trong ledger và proposal được đo riêng.

Đổi eval set phải tăng eval_set_version và chạy baseline mới. Đổi spec cần version/giải thích, không nới threshold trong cùng eval-set version; code giữ ratchet. Không tuyên bố điểm hidden khi chưa có kết quả giảng viên.
