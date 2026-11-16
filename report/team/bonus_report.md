# Bonus report: B4

Commit triển khai: `5e4d628c890e7781606e3d28d54016bf0d6e2111`, cùng commit code chốt trong ADR.

- Topic: baseline công bằng, ablation và thống kê; Rethinking the Evaluation of Efficiency Methods for Multi-Agent Systems, Zhang et al., EMNLP 2026, slide 44/59; [nguồn chính thức](https://aclanthology.org/2026.emnlp-main.798/).
- CLAIM: đánh giá hiệu quả có thể bị ảnh hưởng bởi prompt, topology xuất phát và setup; cần baseline đơn giản và điều kiện đo chung.
- BOUNDARY: nguồn nghiên cứu efficiency method trên benchmark của tác giả; lab này chỉ kiểm quy trình claim với MockLLM, không tái lập paper hoặc so model thật.
- HYPOTHESIS: bỏ draft workflow giữ kết quả nghiệp vụ và giảm cost; cắt peer/parse ngẫu nhiên của swarm có thể giữ kết quả với ít lời gọi hơn. Đây là mở rộng sau khi đã biết lỗi public, không đăng ký giả thuyết mù trước dữ liệu.
- Biến cố định: public world/corpus, MockLLM, as_of 2026-11-15, năm seed, bảng giá, tool và evaluator. Workflow ablation chỉ tắt draft. Swarm pruned bỏ riêng peer/parse độc lập với xác suất 0.5, RNG ổn định theo claim+seed; không chọn lại seed để làm đẹp kết quả.
- Lệnh tái lập trong src: `python -m bonus.run_b4`; kiểm test và chạy lại: `python -m bonus.verify_b4`.
- Report: src/reports/bonus_benchmark.json, bonus_ablation.json, bonus_verification.json. Run ID: R-rules_only-C-001-s11, R-swarm_pruned-C-002-s55; đầy đủ trong report.

## Kết quả

Benchmark chính thức qua extra-shape, 14 claim × 5 seed mỗi shape. Ba baseline workflow/single/swarm khớp kết quả bài chính. Rules-only dùng cùng workflow._run, chỉ tắt draft, không gọi model. Swarm pruned là bản dẫn xuất có ghi nguồn, không sửa swarm tham chiếu.

| Shape | Pass | Pass^5 | Variance | Cost/success mô phỏng VND | Bootstrap 95% CI pass rate |
| --- | --- | --- | --- | --- | --- |
| Workflow | 70/70 | 14/14 | 0 | 28.871429 | [1, 1] |
| Single | 70/70 | 14/14 | 0 | 39.154286 | [1, 1] |
| Swarm | 69/70 | 13/14 | 0.000816327 | 49.566957 | [0.957143, 1] |
| Rules-only, bỏ draft | 70/70 | 14/14 | 0 | 27.857143 | [1, 1] |
| Swarm pruned | 70/70 | 14/14 | 0 | 48.052286 | [1, 1] |

Bootstrap 5.000 lần, seed thống kê 20261116, resample theo claim và giữ nguyên năm seed trong từng cụm. CI [1,1] là bootstrap suy biến trên mẫu toàn pass, **không bảo đảm 100% trên claim mới**. Với workflow–swarm, rules-only–workflow và pruned–swarm: exact McNemar p=1.0; kiểm định sign theo cụm claim cũng p=1.0. Trial giữa các seed cùng claim có thể phụ thuộc nên không coi p trial là bằng chứng độc lập mạnh hơn p theo cụm.

Safety replay 350 trial mới, SQLite riêng: mỗi shape 70 trial, số runtime error, invalid trace, secret leak, PII leak, approval bypass, ledger lạ và effect/audit trùng đều 0. Scanner đọc result, trace và sibling, stdout/stderr; kiểm chuỗi nhạy cảm public và đối chiếu effect với host authorize. Đây là quan sát public, không thay grader hidden. Lần chạy lại bonus được so sánh toàn bộ byte JSON, không chỉ các số đã làm tròn.

## Kết luận

Bỏ draft giữ status/quote/effect và giảm 3.51% cost/success, nhưng không chứng minh chất lượng lời đáp khách được giữ vì grader không chấm lời đáp. Swarm pruned giảm số model call trung bình 3 → 2.014286 và đạt thêm đúng một trial public. Khi bỏ parse, đường override số ngày từ ticket cũng bị tắt: cải thiện không chứng minh pruning tăng năng lực suy luận. Chênh lệch nhỏ, p=1.0, chưa đủ bằng chứng có ý nghĩa thống kê; cũng không chứng minh hai hệ thống tương đương.

Giữ workflow làm shape chọn. Nếu workload mới cần hiểu ticket phi cấu trúc hoặc phản hồi có chất lượng, baseline rules-only có thể mất lợi thế và phải đo lại trên bộ mới.

## Giới hạn và gate

MockLLM, public nhỏ/đã quan sát, cost mô phỏng, latency `unavailable`; không suy sang model sản xuất. Các shape ghi trace khác độ chi tiết nên steps không phải latency. Ablation draft cô lập một thành phần; so bốn kiến trúc không cô lập hoàn toàn topology. Chỉ dùng stdlib và requirements gốc, không thêm API hay sửa host/config/data.

Đã chuẩn bị bằng chứng B4, **chưa tự nhận được cộng điểm**: giảng viên cần xác nhận workflow đạt hidden ≥0.80 trên 200 trial, không bypass/secret leak, crash 20/20 và host test xanh. Bonus tối đa +10, không mặc định được đủ điểm.
