# Đối chiếu toàn bộ yêu cầu Lab08

Rà soát ngày 16/11/2026, phạm vi bài chính. Đây là đối chiếu bằng chứng, không phải phiếu chấm điểm của giảng viên.

## 1. Nguồn yêu cầu

README, CHECKPOINTS, RUBRIC, RULES, SUBMISSION, TEAM; src/README, src/reports/README; docs/business_rules, contracts, metrics, architecture; các mẫu report/team. Bộ hidden và bonus được đọc để xác định phạm vi, không được tự công nhận kết quả chưa chạy.

## 2. Tám tiêu chí rubric

| Tiêu chí | Bằng chứng hiện có | Kết luận |
| --- | --- | --- |
| C1 Implementation, 20 điểm | Ba file shape triển khai; mỗi shape qua 62 student test; dùng finish và compute_compensation | Đủ bằng chứng public |
| C2 Hidden, 15 điểm | ADR chọn workflow; chưa có kết quả grader riêng | Chờ giảng viên; chưa xác nhận ≥0.75 trên 200 trial |
| C3 Durability, 20 điểm | crash.json 20/20; T11/T12; 6 test crash bổ sung trên ba shape | Đạt kiểm tra public |
| C4 Policy, 10 điểm | Matrix kiểm approval, policy, T13/T14; quote đầy đủ do host xử lý | Public đạt; approval_bypass_count hidden chưa có |
| C5 Handoff/trace, 10 điểm | make_handoff, investigator chỉ đọc; trace contract; test injection và output không lộ dữ liệu | Public đạt; secret_leak_count/pii_leak_count hidden chưa có |
| C6 Benchmark/quyết định, 10 điểm | 4 × 14 × 5 = 280 trial, ADR, research card và ablation 140 trial | Đủ bằng chứng; giữ giới hạn MockLLM |
| C7 Tái lập, 10 điểm | Commit kỹ thuật b1120c2; run ID; benchmark lần hai khớp toàn bộ; lệnh chạy trong hướng dẫn | Đạt trên Windows/Python 3.11.9; không nhận đã kiểm đa nền tảng |
| C8 Đóng góp, 5 điểm | Một thành viên trong TEAM; commit b1120c2 có ba shape và 15 test; báo cáo cá nhân riêng | Đủ hồ sơ kỹ thuật; người học cần đọc và hoàn thiện tự đánh giá |

Không cộng các dòng này thành điểm tự chấm. C2 và phần safety trên hidden chỉ có thể xác nhận bằng kết quả chính thức. Không phát hiện thiếu code hay bằng chứng public bắt buộc qua lần rà này.

## 3. Checkpoint và danh sách nộp

- CP1: môi trường, smoke, host và thông tin nhóm có đủ. Email liên hệ còn để chưa cung cấp; không ảnh hưởng check_submission.
- CP2: workflow/single/orchestrator không còn stub, 62 student test/shape, chữ ký run_claim giữ nguyên.
- CP3: idempotency, T12, handoff allowlist; đã chạy demo buggy_workflow và thấy 2 dòng unsafe, minh họa checkpoint không thay ledger.
- CP4: crash 20/20, quote dương bị từ chối có audit qua host; trace mới ở mọi nhánh return. Crash được truyền ra theo contract, không bị nuốt.
- CP5: có benchmark, ADR, research card, báo cáo nhóm và cá nhân; check_submission 0 FAIL, 0 WARN. Hidden selfcheck chỉ chạy khi được phát student_drop và không tự cho pass rate khi thiếu nhãn.

Thư mục/nội dung bắt buộc có đủ: TEAM.md; report/team/group_report.md, decision_adr.md, research_card.md, 2A202603646_NguyenManhTuong.md; src/lab8/shapes/{workflow,single,orchestrator}.py; test mới; src/reports/{benchmark,crash}.json. File mẫu MSSV_HoTen.md được giữ nguyên.

Tên repo đúng mẫu nhóm L3A và repo public. Commit trong ADR tồn tại, có test kỹ thuật trong lịch sử. Benchmark, crash và ablation do công cụ tạo, không sửa JSON. Kiểm tra 28 file host/core/config/data so với upstream không đổi; chỉ ba shape thay trong phần source chính thức. Không commit .env, .venv, trace, SQLite, student_drop hoặc pack hidden. Runtime không gọi API thật.

## 4. Những chỗ đã hoàn thiện trong lần rà này

1. Khôi phục phần hướng dẫn và hai cột đầu của research_card đúng mẫu gốc, chỉ điền cột Nhóm điền; giữ nguyên kết quả đã đo.
2. Bổ sung lệnh và output thực tế vào mục Khó khăn của báo cáo nhóm theo RULES, tham chiếu log máy tạo.
3. Đối chiếu file nộp, controls của ablation, hash bằng chứng, commit/test và liên kết báo cáo. Không sửa code hoặc chạy lại để thay kết quả bằng số đẹp hơn.

## 5. Việc còn lại

### Người học

- Điền email liên hệ nếu muốn hoàn chỉnh trường thông tin trong mẫu; có thể tự sửa file vì repo public. Đây không phải gate kỹ thuật.
- Đọc báo cáo cá nhân, sửa phần tự đánh giá theo trải nghiệm thực và chuẩn bị giải thích: vì sao chọn workflow; code/model quyết gì; vì sao quote đầy đủ; field nào không được ghi trace.
- Nếu nhận student_drop, đặt local trong src/ rồi chạy selfcheck theo src/README; không commit pack.
- Tự nộp link repo bằng tài khoản LMS đúng hạn coach thông báo. Hạn cụ thể phụ thuộc buổi học, không suy từ ngày chạy code.

### Giảng viên / môi trường ngoài

- Chấm hidden 40 claim × 5 seed: pass rate ≥0.75 và không approval bypass/secret leak, cùng yêu cầu crash 20/20. Không tự tạo hidden_grade.json.
- API GitHub kiểm tra thời điểm rà soát cho biết repo public và chưa có workflow run. CI đa nền tảng chưa có bằng chứng; CI không phải deliverable riêng bắt buộc và báo cáo không nhận đã chạy ở ba hệ điều hành.

Bonus tùy chọn chưa làm. Module trong src/bonus hiện phục vụ ablation bắt buộc và kiểm chứng kỹ thuật, không phải hồ sơ xin điểm cộng. Báo cáo nhóm được giữ ngắn ở Markdown; khi xuất bản in/PDF để trình bày cần giữ giới hạn 5 trang ngoài phụ lục.
