# Actual offline test report

Toàn bộ O01–O08 là synthetic hoặc fault injection; không có Gemini live call. Không dùng claim thị trường cũ như output MVP.

## Kiểm thử tự động

Lần đầu: 30 passed, 3 failed. Hai UI tests sai đường dẫn; một HTML test giả định library chọn title tag trong khi chọn heading. Đã sửa assumptions của test. Kết quả trước sửa giữ ở pytest-initial.xml.

Lần sau: 33 passed; sau khi thêm kiểm tra sửa đánh giá nguồn, blocker định nghĩa trước, PDF reader và pipeline mock đầy đủ: **37 passed**. Bao gồm kiểm tra UI/review, API disabled, mock SDK/schema/attribution, scope/cutoff/citation, lỗi thu thập và reader. `test_known_semantic_failure...` PASS vì tái hiện được giới hạn sản phẩm; không phải semantic support PASS.

## Các tình huống có kết quả thực tế

### O01 — Tình huống tốt

**Loại:** synthetic / offline

**Kỳ vọng:** Các chiều đủ synthetic evidence → Tiếp tục; xuất ledger truy vết được

**Kết quả thực tế:** `{"status": "completed", "recommendation": "Tiếp tục", "claim_statuses": ["mechanically_checked", "mechanically_checked", "mechanically_checked"], "findings": ["Fictional signals justify reviewing the opportunity."], "errors": []}`

**Đạt/Chưa đạt:** Đạt

**Điều học được:** Workflow hoạt động trên đầu vào synthetic; chưa chứng minh chất lượng Gemini.

**Artifact:** [Run JSON](test-artifacts/O01.json)

### O02 — Game/thị trường/câu hỏi khác

**Loại:** synthetic / offline

**Kỳ vọng:** Xử lý Game Beta ở China; Research không ép recommendation

**Kết quả thực tế:** `{"status": "completed", "recommendation": null, "claim_statuses": ["mechanically_checked", "mechanically_checked", "mechanically_checked"], "findings": ["Signals are scoped to fictional China data; no transfer to Vietnam assumed."], "errors": []}`

**Đạt/Chưa đạt:** Đạt

**Điều học được:** Logic không hard-code MABINOGI; chưa thay thế ba live runs.

**Artifact:** [Run JSON](test-artifacts/O02.json)

### O03 — Khó: hai nguồn mâu thuẫn

**Loại:** synthetic / offline

**Kỳ vọng:** Giữ C1 và C4, Tạm giữ, có bước phân xử

**Kết quả thực tế:** `{"status": "completed", "recommendation": "Tạm giữ", "claim_statuses": ["mechanically_checked", "mechanically_checked", "mechanically_checked", "mechanically_checked"], "findings": ["Fictional signals justify reviewing the opportunity."], "errors": []}`

**Đạt/Chưa đạt:** Đạt

**Điều học được:** Không lấy trung bình hoặc bỏ một phía.

**Artifact:** [Run JSON](test-artifacts/O03.json)

### O04 — Thiếu D30 retention

**Loại:** synthetic / offline

**Kỳ vọng:** Không thay bằng doanh thu; partial và gap cụ thể

**Kết quả thực tế:** `{"status": "partial", "recommendation": null, "claim_statuses": [], "findings": [], "errors": []}`

**Đạt/Chưa đạt:** Đạt

**Điều học được:** Câu hỏi chưa được đáp ứng; xử lý thiếu dữ liệu đúng. Case synthetic, không phải T09 live.

**Artifact:** [Run JSON](test-artifacts/O04.json)

### O05 — Citation giả

**Loại:** synthetic / offline

**Kỳ vọng:** Loại claim và findings phụ thuộc; Tạm giữ

**Kết quả thực tế:** `{"status": "partial", "recommendation": "Tạm giữ", "claim_statuses": ["rejected", "mechanically_checked", "mechanically_checked"], "findings": [], "errors": ["Finding excluded: invalid claim references"]}`

**Đạt/Chưa đạt:** Đạt

**Điều học được:** Chặn trích đoạn giả bằng nội dung đã đọc.

**Artifact:** [Run JSON](test-artifacts/O05.json)

### O06 — Nguồn sai thị trường

**Loại:** synthetic / offline

**Kỳ vọng:** Không dùng Korea evidence vượt gate Vietnam

**Kết quả thực tế:** `{"status": "partial", "recommendation": "Tạm giữ", "claim_statuses": ["rejected", "mechanically_checked", "mechanically_checked"], "findings": [], "errors": ["Finding excluded: invalid claim references"]}`

**Đạt/Chưa đạt:** Đạt

**Điều học được:** Uy tín nguồn không thay thế độ phù hợp.

**Artifact:** [Run JSON](test-artifacts/O06.json)

### O07 — Lỗi kỹ thuật

**Loại:** synthetic / offline

**Kỳ vọng:** failed; không tạo claim, không Dừng opportunity

**Kết quả thực tế:** `{"status": "failed", "recommendation": "Tạm giữ", "claim_statuses": [], "findings": [], "errors": ["Pipeline interrupted (TimeoutError); no fabricated fallback"]}`

**Đạt/Chưa đạt:** Đạt

**Điều học được:** Fault injection PASS kỹ thuật; không tự tính thành case thị trường thất bại.

**Artifact:** [Run JSON](test-artifacts/O07.json)

### O08 — Thất bại sản phẩm: ngữ nghĩa

**Loại:** synthetic / offline

**Kỳ vọng:** Nhận ra claim nói mạnh trong khi quote nói không mạnh

**Kết quả thực tế:** `{"status": "completed", "recommendation": null, "claim_statuses": ["mechanically_checked"], "findings": ["Strong Vietnam demand."], "errors": []}`

**Đạt/Chưa đạt:** Chưa đạt

**Điều học được:** Actual: claim và finding sai vẫn qua quote matching. Cần semantic audit người dùng; ưu tiên thêm entailment assessment và audit set khi chạy live.

**Artifact:** [Run JSON](test-artifacts/O08.json)

## Còn thiếu trước bài nộp

T01–T03 và T06/T09 live chưa chạy; chưa có audit của người tham gia/Lead thực; chưa đo chất lượng nghiên cứu, latency live, chi phí hay tiết kiệm thời gian. O08 là thất bại synthetic đã quan sát; chưa đáp ứng yêu cầu case sản phẩm thất bại từ live research.