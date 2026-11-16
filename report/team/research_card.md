# Research card

File này nằm cố định ở `report/team/research_card.md`; `python -m lab8.check_submission` đọc cột "Nhóm điền" bằng máy.

Phần này nối tiếp phần mini research ở buổi lý thuyết (slide 62–63). Chọn **một** câu R1–R4, điền 6 dòng, rồi biến nó thành **một ablation** chạy được trong lab: giữ nguyên model (MockLLM), tool, seed, corpus và giá, chỉ thay đổi một biến.

| Câu | Nguồn (thư viện tham khảo, slide 68–69) | Câu hỏi gợi ý cho lab |
| --- | --- | --- |
| R1 · Scaling | Google Research 2026, *Towards a Science of Scaling Agent Systems* | Task claims chủ yếu tuần tự hay song song được? Dự đoán thêm investigator sẽ làm pass rate và cost/success thay đổi thế nào. |
| R2 · Failure taxonomy | MAST, NeurIPS 2025, *Why Do Multi-Agent LLM Systems Fail?* | Các trial fail của swarm (seed 55) thuộc nhóm nào: lỗi giao việc, lệch mục tiêu, hay lỗi kiểm chứng? |
| R3 · Architecture choices | AgentArch, AACL 2026 | Nếu đổi topology mà giữ nguyên mọi thứ khác, biến nào phải cố định để kết luận còn đúng? |
| R4 · Evaluation confounders | EMNLP 2026, *Rethinking Evaluation of MAS Efficiency* | Làm sao chứng minh chênh lệch giữa A/B/C/D là do topology, không phải do prompt, tool hay seed? |

## Phiếu của nhóm

Điền vào cột cuối. Không xóa hai cột đầu.

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R4 — Evaluation confounders |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng (benchmark, production report, blog kinh nghiệm) | Zhang et al., EMNLP 2026, Rethinking the Evaluation of Efficiency Methods for Multi-Agent Systems; https://aclanthology.org/2026.emnlp-main.798/ ; nghiên cứu benchmark có kiểm soát, đối chiếu abstract chính thức. |
| CLAIM | Một kết luận gốc của nguồn. Không viết rộng hơn phạm vi paper | Hiệu quả báo cáo có thể phụ thuộc prompt/topology/setup; đánh giá cần giữ backbone, registry và runtime chung. Không diễn giải thành multi-agent luôn thừa. |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | Nguồn nghiên cứu efficiency method trong benchmark của tác giả; lab dùng MockLLM và task claim nhỏ, không tái lập toàn bộ paper. |
| HYPOTHESIS | Nếu đổi shape A→B (hoặc bật/tắt một thành phần), metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | Bỏ riêng draft cuối workflow giữ pass rate 1.0, giảm một model call/trial và cost/success. Đây là dự đoán giải thích cấu trúc, không đăng ký trước khi đã quan sát public. |
| METHOD | Biến giữ cố định: model, tools, seed, corpus, giá, evaluator. Biến duy nhất được thay đổi: … | Giữ model, tool, world/corpus, policy as_of, năm seed, giá và evaluator. Chỉ tắt draft cuối, dùng cùng workflow._run với draft=False và run name riêng. |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo nó: pass rate, pass^5, variance, cost/success, leak, bypass | Nếu đổi status, proposal hoặc ledger thì giả thuyết không đạt. Đo pass, pass^5, variance, cost/success, model/tool calls và steps; test đối chiếu effect trực tiếp. |

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

Code biến thể ở `src/bonus/` để không sửa host; đây là ablation bắt buộc của research card. Phần B4 mở rộng, thống kê và baseline bổ sung được báo cáo riêng ở [bonus_report.md](bonus_report.md), không dùng ablation này để tự nhận điểm. Giữ workflow có draft làm shape chính. Giới hạn: MockLLM, latency `unavailable`, public nhỏ và evaluator không chấm lời đáp khách. Thí nghiệm chỉ cô lập draft; không cô lập topology của bốn shape vì prompt, số tool call và instrumentation khác nhau.
