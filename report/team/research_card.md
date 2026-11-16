# Research card

## Phiếu của nhóm

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R4 — Evaluation confounders |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng | Zhang et al., EMNLP 2026, Rethinking the Evaluation of Efficiency Methods for Multi-Agent Systems; https://aclanthology.org/2026.emnlp-main.798/ ; nghiên cứu benchmark có kiểm soát, đối chiếu abstract chính thức. |
| CLAIM | Kết luận gốc của nguồn | Hiệu quả báo cáo có thể phụ thuộc prompt/topology/setup; đánh giá cần giữ backbone, registry và runtime chung. Không diễn giải thành multi-agent luôn thừa. |
| BOUNDARY | Giới hạn kết luận | Nguồn nghiên cứu efficiency method trong benchmark của tác giả; lab dùng MockLLM và task claim nhỏ, không tái lập toàn bộ paper. |
| HYPOTHESIS | Dự đoán khi thay một thành phần | Bỏ riêng draft cuối workflow giữ pass rate 1.0, giảm một model call/trial và cost/success. Đây là dự đoán giải thích cấu trúc, không đăng ký trước khi đã quan sát public. |
| METHOD | Biến cố định / thay đổi | Giữ model, tool, world/corpus, policy as_of, năm seed, giá và evaluator. Chỉ tắt draft cuối, dùng cùng workflow._run với draft=False và run name riêng. |
| FAILURE / METRIC | Lỗi và cách đo | Nếu đổi status, proposal hoặc ledger thì giả thuyết không đạt. Đo pass, pass^5, variance, cost/success, model/tool calls và steps; test đối chiếu effect trực tiếp. |

## Kết quả ablation

Chạy trong `src/`:

```powershell
python -m lab8.benchmark --shapes workflow,workflow_no_draft --extra-shape workflow_no_draft=bonus.workflow_no_draft:run_claim --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/research_ablation.json
```

- Report: `src/reports/research_ablation.json`, do benchmark chính thức sinh.
- Run id: `R-workflow-C-001-s11`, `R-workflow_no_draft-C-001-s11`; 70 cặp claim/seed mỗi biến thể.

| Biến thể | Pass | Pass^5 | Variance | Cost/success VND mô phỏng | Model call trung bình | Tool call trung bình | Mean/p95 steps |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Workflow có draft | 70/70 | 14/14 | 0 | 28.871429 | 1 | 2.785714 | 5.428571 / 6 |
| Bỏ draft | 70/70 | 14/14 | 0 | 27.857143 | 0 | 2.785714 | 4.428571 / 5 |

Kết quả phù hợp giả thuyết trên public: giảm 1.014286 VND mô phỏng/success, khoảng 3.51%, không đổi quyết định nghiệp vụ. Steps giảm một do bỏ một event, không phải phép đo latency nhanh hơn. Không phát hiện leak/bypass trên các trial qua evaluator; không suy ra safety count hidden.

Code biến thể ở `src/bonus/` để không sửa host; đây là ablation bắt buộc của research card, **không xin điểm bonus**. Giữ workflow có draft làm shape chính. Giới hạn: MockLLM, latency `unavailable`, public nhỏ và evaluator không chấm lời đáp khách. Thí nghiệm chỉ cô lập draft; không cô lập topology của bốn shape vì prompt, số tool call và instrumentation khác nhau.
