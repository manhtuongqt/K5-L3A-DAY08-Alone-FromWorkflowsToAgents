# Báo cáo cá nhân — Nguyễn Mạnh Tường

## 1. Thông tin thành viên

- Họ tên: Nguyễn Mạnh Tường. MSSV: 2A202603646. Lớp: L3A.
- Email: chưa cung cấp. GitHub: [manhtuongqt](https://github.com/manhtuongqt).
- Nhóm: NguyenManhTuong, một thành viên.

## 2. Phần việc phụ trách

Phạm vi bài của tôi gồm workflow, single ReAct, orchestrator, test an toàn và báo cáo so sánh với swarm có sẵn. Tôi dùng Codex hỗ trợ viết code, chạy lệnh và soạn báo cáo từ kết quả thực thi. Không khai báo người cộng tác giả hoặc người review độc lập.

## 3. Đóng góp cụ thể

- Workflow lấy dữ kiện có cấu trúc, tính quote bằng code rồi gọi host với quote đầy đủ.
- Single đi qua run_react, chỉ dùng tool đọc, tối đa 8 bước; orchestrator chuyển handoff allowlist.
- Tiền, approval, giới hạn theo đơn và idempotency vẫn thuộc code/host; không sửa thước đo.
- Thêm 15 test trong `src/tests/test_team_safety.py`, gồm cửa sổ crash bổ sung, injection, unknown claim, handoff và loop.
- Ablation bỏ riêng draft cuối; cùng dữ liệu, seed, tool, giá và evaluator.

## 4. Bằng chứng

- Commit kỹ thuật: b1120c2aeb12e2e0a185693d4abd6b766a10d4f5; cũng được tham chiếu trong ADR.
- Benchmark: workflow/single/orchestrator mỗi shape 70/70, swarm 69/70.
- Crash suite 20/20; student 248 passed; host và test bổ sung 69 passed.
- Run minh họa: `R-workflow-C-001-s11`, `R-swarm-C-002-s55`.
- `src/reports/verification.json` lưu lệnh kiểm chứng thực thi; không phải grader hidden.

## 5. Công cụ AI đã dùng

Codex hỗ trợ giải thích contract, triển khai shape/test, chạy benchmark/ablation và dự thảo tài liệu. Số liệu được kiểm bằng evaluator chính thức và lần chạy lại benchmark; không sửa JSON. Kiểm chứng kỹ thuật tự động không thay trách nhiệm của tôi khi đọc và giải thích code với giảng viên.

Tôi cần giải thích được vì sao phải truyền quote đầy đủ, approval thuộc host và ticket không có quyền sửa dữ kiện order. Runtime Lab08 dùng MockLLM, không dùng API model thật.

## 6. Tự đánh giá

Kết quả public ủng hộ workflow cho quy trình luật rõ ràng. Single và orchestrator tăng lời gọi nhưng chưa tăng độ đúng. Không suy thành mọi multi-agent đều kém hơn workflow. Hidden chưa được chấm; không lấy public làm điểm hidden.

Báo cáo cá nhân này là dự thảo có AI hỗ trợ để tôi đọc, hoàn thiện phần tự đánh giá và chuẩn bị trình bày trước khi nộp LMS.
