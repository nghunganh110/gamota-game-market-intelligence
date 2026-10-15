# Actual offline test report

## Latest live evidence and regression update

[T03 đã chạy](live-T03-review.md) bằng .env private: một ConnectError trong sandbox được giữ; sau cấp quyền chạy ngoài sandbox, 2 attempts, 5 claims, 1 mechanically checked, partial. Bốn nguồn đọc thất bại; nhận định còn lại chỉ là qualitative genre signal. T01/T02/T03 đã thực thi nhưng chưa có human acceptance. Không chạy suite mới trong phiên chỉ execute/audit; 53 passed là kết quả lần thêm .env loader.

[T02 live](live-T02-review.md) đã chạy game thứ hai: 2 calls, 10 claims, 6 mechanically checked, 4 rejected vì period ngoài scope; partial. AI audit vẫn có lỗi trộn phạm vi claim, gross/net và attribution; chưa human-accepted. [Bảng tiến độ các lần gọi thật](live-test-progress.md) tách fresh discovery, snapshot extraction và offline derivatives.

T01 extraction từ snapshots: **1 model call thật**, 6 claims, 5 mechanically checked, 1 rejected do ghép quote bằng `...`; partial. Không còn period mismatch, Research dimensions rỗng. AI audit vẫn thấy causal inference PC không có đủ evidence, nên chất lượng tổng thể chưa đạt. [Báo cáo extraction](live-T01-extraction-review.md). Đây là replay có extraction mới, không phải fresh discovery hoặc human audit.

T01 lần 2: partial, 2 API attempts, 0 claims, discovery chỉ trả navigation shell. Extraction trả gaps thay vì bịa evidence; chưa kiểm chứng được bản sửa kỳ đo. [Báo cáo lần 2](live-T01-rerun-review.md) ghi root cause và phép thử extraction một-call với snapshots cũ. Suite hiện tại **50 passed**, chưa chạy Gemini thêm trong phiên chẩn đoán.

The first T01 live run has now executed: two API attempts, five extracted claims, partial status. It exposed a period-string validation failure and semantic overclaims. See [T01 actual result and AI audit](live-T01-review.md). This is not an accepted research brief; human audit remains pending. The earlier offline results below are historical and unchanged. After the measurement-window fix, the current suite is **47 passed**; the earlier clean-environment verification covered 37 tests.

Toàn bộ O01–O08 là synthetic hoặc fault injection; không có Gemini live call. Không dùng claim thị trường cũ như output MVP.

## Kiểm thử tự động

Lần đầu: 30 passed, 3 failed. Hai UI tests sai đường dẫn; một HTML test giả định library chọn title tag trong khi chọn heading. Đã sửa assumptions của test. Kết quả trước sửa giữ ở pytest-initial.xml.

Lần sau: 33 passed; sau khi thêm kiểm tra sửa đánh giá nguồn, blocker định nghĩa trước, PDF reader và pipeline mock đầy đủ: **37 passed**. Bao gồm kiểm tra UI/review, API disabled, mock SDK/schema/attribution, scope/cutoff/citation, lỗi thu thập và reader. `test_known_semantic_failure...` PASS vì tái hiện được giới hạn sản phẩm; không phải semantic support PASS.

## Kiểm tra môi trường sạch

Source từ Git archive + venv Python mới + requirements.txt (cài từ cache offline): **37 passed**. Artifact: test-artifacts/pytest-clean.xml. Browser cold start và các tình huống good/conflict/missing/semantic failure đã mở được. Khi hot-reload sau thay đổi module, server giữ import cũ và báo thiếu SourceReview; restart server giải quyết, cold start không tái hiện lỗi này.

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

T01 đã chạy live và chưa đạt chất lượng end-to-end; latency và usage có trong báo cáo mới. T02–T03 và T06/T09 live chưa chạy; chưa có audit của người tham gia/Lead thực, chi phí tiền tệ hay đo tiết kiệm thời gian. O08 là thất bại synthetic; T01 bổ sung thất bại sản phẩm quan sát từ live research.
