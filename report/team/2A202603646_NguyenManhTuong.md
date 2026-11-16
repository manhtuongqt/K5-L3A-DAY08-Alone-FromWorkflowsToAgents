# Báo cáo cá nhân — Nguyễn Mạnh Tường

## 1. Thông tin thành viên

- Họ tên: Nguyễn Mạnh Tường. MSSV: 2A202603646. Lớp: L3A.
- Email: chưa cung cấp. GitHub: [manhtuongqt](https://github.com/manhtuongqt).
- Nhóm: Alone, một thành viên.

## 2. Phần việc phụ trách

Tôi là thành viên duy nhất của nhóm Alone và phụ trách toàn bộ bài chính, bonus B4, kiểm thử, benchmark và báo cáo. Toàn bộ phần việc của nhóm được ghi dưới tên tôi; không có thành viên khác cùng thực hiện.

Phạm vi bài của tôi gồm workflow, single ReAct, orchestrator, test an toàn và báo cáo so sánh với swarm có sẵn. Tôi dùng Codex hỗ trợ viết code, chạy lệnh và soạn báo cáo từ kết quả thực thi. Không khai báo người cộng tác giả hoặc người review độc lập.

## 3. Đóng góp cụ thể

- Workflow lấy dữ kiện có cấu trúc, tính quote bằng code rồi gọi host với quote đầy đủ.
- Single đi qua run_react, chỉ dùng tool đọc, tối đa 8 bước; orchestrator chuyển handoff allowlist.
- Tiền, approval, giới hạn theo đơn và idempotency vẫn thuộc code/host; không sửa thước đo.
- Thêm 15 test trong `src/tests/test_team_safety.py`, gồm cửa sổ crash bổ sung, injection, unknown claim, handoff và loop.
- Ablation bỏ riêng draft cuối; cùng dữ liệu, seed, tool, giá và evaluator.
- Bonus B4: thêm rules-only, swarm pruned theo seed và thống kê bootstrap theo claim, kiểm định cặp; không sửa swarm tham chiếu hoặc evaluator chính thức.

## 4. Bằng chứng

- Commit kỹ thuật: 5e4d628c890e7781606e3d28d54016bf0d6e2111; cũng được tham chiếu trong ADR.
- Benchmark: workflow/single/orchestrator mỗi shape 70/70, swarm 69/70.
- Crash suite 20/20; student 248 passed; host và test bổ sung 78 passed, gồm 9 test bonus mới.
- Run minh họa: `R-workflow-C-001-s11`, `R-swarm-C-002-s55`.
- `src/reports/verification.json` lưu lệnh kiểm chứng thực thi; không phải grader hidden.
- B4 có 350 trial benchmark và safety replay riêng; `src/reports/bonus_ablation.json` và `bonus_verification.json` lưu CI, p-value, safety và kết quả tái lập. Commit mở rộng B4 được ghi tại phần bổ sung trong TEAM.md.

## 5. Công cụ AI đã dùng

Codex hỗ trợ giải thích contract, triển khai shape/test, chạy benchmark/ablation và dự thảo tài liệu. Số liệu được kiểm bằng evaluator chính thức và lần chạy lại benchmark; không sửa JSON. Kiểm chứng kỹ thuật tự động không thay trách nhiệm của tôi khi đọc và giải thích code với giảng viên.

Tôi cần giải thích được vì sao phải truyền quote đầy đủ, approval thuộc host và ticket không có quyền sửa dữ kiện order. Runtime Lab08 dùng MockLLM, không dùng API model thật.

## 6. Tự đánh giá

Tôi chọn workflow vì đạt cùng kết quả public với single và orchestrator nhưng ít lời gọi và chi phí mô phỏng thấp hơn. Điểm cần giữ trong thiết kế là số tiền và approval phải do code kiểm soát; model không có quyền bỏ qua ledger hoặc thay dữ kiện order bằng lời khách viết trong ticket.

Thí nghiệm B4 cho thấy bỏ draft không làm đổi quyết định nghiệp vụ trong bộ này. Tôi không coi đó là bằng chứng bỏ model luôn tốt vì evaluator chưa chấm câu chữ trả lời khách. Swarm pruned tránh được một lỗi public khi bỏ parse nhưng exact McNemar và sign test đều p=1.0; tôi chưa có cơ sở khẳng định khác biệt có ý nghĩa thống kê hoặc hai hệ thống tương đương.

Giới hạn quan trọng là MockLLM, 14 claim public và việc đã biết lỗi của swarm trước khi làm bonus. Tôi giữ nguyên kết quả không hoàn hảo và ghi nguồn code tham chiếu. Hidden chưa được chấm: bài chính cần ≥0.75, điều kiện nhận bonus cần ≥0.80 cùng các must-pass. Tôi không lấy public làm điểm hidden và không ghi đã nộp LMS khi chưa nộp.

## 7. Nội dung chuẩn bị trình bày

1. Quote đầy đủ giúp host tự trừ refund cũ đúng một lần, T14 proposal 150.000 nhưng effect 120.000.
2. Approval thuộc đúng claim và kiểm trong host, không dùng chỉ dẫn trong ticket để cấp quyền ghi.
3. Retry dùng khóa refund:claim_id và transaction effect/audit; checkpoint đơn lẻ không bảo đảm một lần hoàn tiền.
4. Handoff/trace chỉ chứa dữ kiện được phép; không ghi raw ticket, parent secret, header hoặc PII.
5. Không dùng số bước trace làm latency; các giá VND trong báo cáo là mô phỏng.

Báo cáo được Codex hỗ trợ soạn từ code và kết quả chạy thực tế. Tôi chịu trách nhiệm đọc, giải thích bài làm và tự nộp link repo qua tài khoản LMS của mình.
