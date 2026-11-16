# Báo cáo nhóm — Lab08 LogiX-VN

## 1. Thông tin nhóm

- Nhóm NguyenManhTuong, một thành viên: Nguyễn Mạnh Tường — 2A202603646 — L3A.
- Commit kỹ thuật chốt: b1120c2aeb12e2e0a185693d4abd6b766a10d4f5, trùng ADR. Commit tài liệu sau đó chỉ bổ sung hồ sơ nộp.
- Phạm vi: bài chính, không xin điểm bonus. Hidden chính thức chưa có kết quả.

## 2. Mục tiêu và cách tiếp cận

Tôi so sánh bốn kiến trúc cho cùng quy trình claim để chọn mức tự chủ thấp nhất vẫn đáp ứng công việc. Ba shape tự triển khai là workflow, single và orchestrator; swarm giữ nguyên làm đối chứng. Codex hỗ trợ code, test và tổng hợp bằng chứng. Không dùng model API thật; mọi lời gọi mô hình dùng MockLLM theo seed như đề quy định.

Thứ tự triển khai: đọc contract, nối tool đọc và host, kiểm student matrix, thêm test cho các ranh giới, chạy crash/benchmark, ablation và đối chiếu báo cáo. Chỉ sửa ba file shape, thêm test và module thí nghiệm trong bonus; giữ nguyên host, policy, evaluator, config và dữ liệu.

## 3. Giải pháp

| Shape | Điều phối | Ranh giới code / model |
| --- | --- | --- |
| Workflow | Các bước cố định: claim → order → quote → host → draft | Code tính tiền và quyết định; MockLLM chỉ tạo draft cuối |
| Single | run_react tối đa 8 bước, nhận observation và gọi tool đọc | Controller bằng code ánh xạ trạng thái sang action; MockLLM ghi nhận plan/draft, không tự sinh action JSON |
| Orchestrator | Lập task → handoff allowlist → investigator chỉ đọc → host | Dữ kiện đi qua make_handoff; chỉ orchestrator gọi host ghi tiền |
| Swarm | Bản tham chiếu có sẵn | Giữ nguyên điểm yếu tin số ngày trong ticket ở seed chia hết cho 5 |

Quote do compute_compensation tính từ order/policy có cấu trúc. Ticket không quyết số ngày trễ, không bổ sung order_id bị thiếu và không có quyền đổi policy. Quote bằng 0 thì denied không ghi; quote dương được truyền **đầy đủ** cho issue_refund. Host kiểm approval đúng claim, thời hạn và trần theo đơn trong transaction; tự trừ tiền claim cũ. T14 vì vậy giữ proposal 150.000 nhưng effect 120.000, không trừ hai lần.

Mọi nhánh kết thúc dùng finish, lấy effect/audit từ ledger thật và ghi trace mới. Thiếu order_id trả needs_info; không nhìn thấy đơn trả escalated; unknown claim trả failed. Khi crash, InjectedCrash được truyền ra, connection đóng trong finally. Retry dựa ledger/idempotency, không chỉ dựa checkpoint.

Handoff chỉ có field allowlist và tool đọc; không truyền parent context. Trace không ghi nguyên claim/order, ticket, secret, header, phone, địa chỉ, tên hàng hay internal note; không debug stdout. Single chỉ trace kết quả tool đọc đã allowlist. Trace ở src/traces không commit và được sinh lại bằng lệnh demo.

## 4. Kết quả

Số liệu từ `src/reports/benchmark.json`: 14 claim × seed 11,22,33,44,55; tổng 280 trial, mỗi trial SQLite mới, cùng as_of 2026-11-15 và bảng giá chính thức.

| Shape | Pass rate | Pass^5 | Seed min–max | Variance | Cost/success VND mô phỏng | Mean / p95 steps |
| --- | --- | --- | --- | --- | --- | --- |
| Workflow | 70/70, 100% | 14/14, 100% | 1–1 | 0 | 28.871429 | 5.428571 / 6 |
| Single | 70/70, 100% | 14/14, 100% | 1–1 | 0 | 39.154286 | 11.642857 / 13 |
| Orchestrator | 70/70, 100% | 14/14, 100% | 1–1 | 0 | 48.724286 | 8.214286 / 9 |
| Swarm | 69/70, 98.57% | 13/14, 92.86% | 0.928571–1 | 0.000816327 | 49.566957 | 2.8 / 3 |

Swarm fail C-002 seed 55: ticket nói trễ 5 ngày, order là 2 ngày; reference override dẫn tới refund thay vì denied. Đây là lỗi đã được giữ nguyên trong report, không sửa fixture hoặc swarm để tăng điểm.

Crash suite chính thức đạt 20/20 trong `src/reports/crash.json`. Suite này kiểm host/swarm; ba shape tự viết còn qua T11/T12 và 6 test bổ sung trước effect/sau checkpoint. Host và test mới: 69 passed, student: 248 passed. Benchmark chạy lại được so sánh toàn bộ controlled_variables, 280 trial và summary; bằng chứng ở `src/reports/verification.json` và `benchmark_reproduced.json`.

Tôi chọn workflow theo [ADR](decision_adr.md): cùng độ đúng public với single/orchestrator nhưng ít tự chủ và chi phí thấp hơn. [Research card](research_card.md) chọn R4, ablation bỏ riêng draft cuối: vẫn 70/70 và 14/14 pass^5, cost 28.871429 → 27.857143, model call 1 → 0, tool call không đổi. Không suy ra chất lượng lời đáp giữ nguyên vì grader không chấm câu chữ.

Hidden chính thức cần ≥0.75 trên 40 claim × 5 seed; hiện chưa có pack/nhãn/grader giảng viên. Không báo pass rate hidden từ public. Chưa có student_drop nên không tạo hidden_selfcheck giả.

## 5. Khó khăn và cách xử lý

- Máy không có Python launcher `py`; dùng `python` 3.11.9 tạo src/.venv và gọi trực tiếp .venv/Scripts/python.exe, không phụ thuộc activate.
- MockLLM không sinh tool JSON: dùng controller trạng thái theo contract runtime, ghi rõ đây là mô phỏng thay vì khẳng định model tự suy luận tiền.
- T13/T14 dễ nhầm quote với effect: giữ quote đầy đủ cho host, kiểm ledger và audit thực qua evaluator.
- Số host test thực tế của phiên bản clone là 54, khác ví dụ tài liệu ghi 52; sau 15 test bổ sung là 69. Không sửa test để khớp số hướng dẫn.

Bằng chứng trên Windows: `py -0p` trả lỗi không nhận diện lệnh `py`. Cách chạy thay thế là `python -m venv src/.venv` ở gốc repo, rồi `.venv/Scripts/python.exe -m pytest -q` trong src. Output kiểm chứng: `69 passed, 248 deselected`; lệnh `.venv/Scripts/python.exe -m pytest -q -m student -o addopts=` cho `248 passed, 69 deselected`. Output đầy đủ của hai lệnh test được lưu trong `src/reports/verification.json`.

## 6. Tổng hợp đóng góp

Nhóm một người; bảng đóng góp trong TEAM.md và [báo cáo cá nhân](2A202603646_NguyenManhTuong.md) ghi phạm vi, test, commit và mức hỗ trợ của Codex. Không có phỏng vấn/review độc lập hoặc thành viên thứ hai được khai báo.

## 7. Hạn chế và hướng cải thiện

MockLLM không phải model sản xuất. Chi phí là mô phỏng VND, latency `unavailable`. Steps là số event, không là thời gian thực; swarm trace ít chi tiết hơn nên không so trực tiếp thành tốc độ nhanh hơn. Corpus public nhỏ và đã thấy; benchmark 100% không bảo đảm hidden hoặc production. Bốn shape khác cả prompt/tool-call/instrumentation nên không cô lập nhân quả topology; chỉ ablation draft giữ các yếu tố khác cố định. Nếu có điều tra song song hoặc workload mới làm workflow không đạt, cần thí nghiệm độc lập trước khi đổi kiến trúc.

## 8. Tài liệu tham khảo

- Repo đề VinUni-AI20k/K5-Day8-From-Workflows-to-Agents; README, RULES, contracts, business_rules, metrics và swarm_reference.
- Zhang et al. (EMNLP 2026), [Rethinking the Evaluation of Efficiency Methods for Multi-Agent Systems](https://aclanthology.org/2026.emnlp-main.798/). Chỉ dùng claim về đánh giá có kiểm soát, không coi kết quả lab là tái lập paper.
- Bằng chứng và lệnh tái lập: [hướng dẫn bài làm](../../docs/BAI_LAM_DAY08.md).
