# Decision record

- Shape chọn: workflow
- Commit hash: b1120c2aeb12e2e0a185693d4abd6b766a10d4f5
- Run id dẫn chứng: R-workflow-C-001-s11; R-swarm-C-002-s55; toàn bộ tại src/reports/benchmark.json
- Pass rate / pass^5 / seed min-max / variance: public 70/70 = 1.0; 14/14 = 1.0; 1.0–1.0; 0.0. Hidden chưa được chấm.
- Cost per success (mô phỏng, VND): 28.8714285714, từ src/reports/benchmark.json, không phải hóa đơn API.
- Crash safety: 20/20 (src/reports/crash.json); workflow còn qua T12 và test before_effect/after_checkpoint.
- Secret leak / approval bypass: không phát hiện trên public, 70/70 qua evaluator; count hidden chính thức chưa có.

## Vì sao shape này

Workflow, single và orchestrator cùng đạt 70/70 trên 14 claim × năm seed. Workflow có cost/success thấp nhất trong bốn shape chính: 28.87 so với 39.15, 48.72 và 49.57 VND mô phỏng. Quy trình phụ thuộc tuần tự vào order, policy, quote và approval nên tôi chọn mức tự chủ thấp nhất đáp ứng bộ public. Đây là shape chọn để giảng viên chấm hidden, chưa phải kết luận đã đạt gate hidden.

## Có đáng đổi lấy multi-agent không

Chưa có lợi ích độ đúng trên public để bù chi phí tăng. Tôi sẽ cân nhắc đổi nếu tác vụ cần điều tra độc lập, ranh giới triển khai hoặc workflow bỏ lỡ nhóm case hợp lệ mà agent xử lý tốt trên bộ mới. Kết luận không áp dụng cho mọi bài toán multi-agent.

## Trace và bằng chứng

Workflow ghi trạng thái claim tối thiểu, khả năng truy cập order, quote, kết quả host, model draft và quyết định. Single thêm observation tool đọc và điều kiện dừng. Orchestrator ghi handoff đã sanitize và dữ kiện investigator allowlist. Không ghi nguyên claim/order, ticket, parent_secret, header, phone, địa chỉ, internal note hoặc tên hàng. Trace sinh trong src/traces, không commit; lệnh tái tạo ở docs/DEMO_DAY08.md. Không ghi debug ra stdout hay file ngoài scanner.

## Giới hạn

MockLLM không phải model sản xuất; latency là `unavailable`. MockLLM trả text xác định, không sinh action JSON; controller single chọn bước từ observation bằng code. Steps phụ thuộc mức chi tiết instrumentation khác nhau giữa shape. Ablation bỏ draft giữ 70/70 và giảm cost xuống 27.86 nhưng evaluator không chấm lời đáp khách nên chưa chứng minh trải nghiệm tốt hơn. Không sửa JSON để đạt ngưỡng 0.75.
