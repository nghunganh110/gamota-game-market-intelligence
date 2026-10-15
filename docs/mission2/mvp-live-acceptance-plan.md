# Kế hoạch kiểm thử live cho bản MVP mới

Chốt trước khi gọi Gemini. Hai câu hỏi khác nhau dùng cùng pipeline, cùng UI review và export. Chưa có kết quả của bản mới tại thời điểm viết; không thay scope sau khi thấy output để gọi PASS.

| Case | Câu hỏi / cách thu nguồn | Kỳ vọng có thể kiểm tra | Calls tối đa |
|---|---|---|---:|
| A01 | [MABINOGI MOBILE, South Korea, March–May 2025](mvp-A01-scope.json); [hai URL đã kiểm tra reader](mvp-A01-urls.txt) | Ít nhất một nhận định hẹp có quote đúng về ước tính doanh thu/tải hoặc người chơi tháng 4; phân biệt nguồn và phép đo; không suy Vietnam. Nếu không, ghi failure/gap. | 1 |
| A02 | [Mobile MMORPG, Vietnam 2025](mvp-A02-scope.json); Gemini tự tìm URL | Có nhận định đúng phạm vi thể loại hoặc gap rõ; không dùng số toàn thị trường thay genre; báo chất lượng và độ phù hợp nguồn. Nếu discovery hỏng, ghi failure. | 2 |
| A02 guided diagnostic | Giữ nguyên scope A02 và dùng [URL Gamota đã kiểm tra reader](mvp-A02-urls.txt) | Xác định lỗi nằm ở discovery/reader hay extraction, không tính là một câu hỏi thứ ba. | 1, chỉ khi cần |

Reader không gọi Gemini đã đọc được cả ba URL trực tiếp ngày 2026-10-15: Sensor Tower 2.584 ký tự, ngày 2025-05-20; Mobile Index 1.193 ký tự, ngày 2025-05-12; Gamota 2.686 ký tự, ngày 2026-06-04. Chỉ xác nhận khả năng đọc và metadata tự động, chưa xác nhận ngữ nghĩa claim hay độ tin cậy nội dung.

Giới hạn mới cần chủ key xác nhận: tối đa **4 API attempts** tổng cho ba phép chạy trên. Không tự retry. Sau mỗi run: lưu JSON/brief, kiểm tra các claim ảnh hưởng câu trả lời với nguyên văn trang gốc, ghi expected → actual → pass/fail → lesson. Người dùng xác nhận hoặc sửa nhận định cuối trong UI; AI audit không tự gán `human_verified`. Tiền tệ/search usage chưa đo được nếu SDK không trả metadata.

Lệnh sau khi có giới hạn mới:

```sh
.venv/bin/python -m scripts.live_research --scope docs/mission2/mvp-A01-scope.json --url-file docs/mission2/mvp-A01-urls.txt --run
.venv/bin/python -m scripts.live_research --scope docs/mission2/mvp-A02-scope.json --run
# Chỉ khi A02 auto discovery thất bại và còn allowance:
.venv/bin/python -m scripts.live_research --scope docs/mission2/mvp-A02-scope.json --url-file docs/mission2/mvp-A02-urls.txt --run
```
