# Kết quả kiểm thử MVP — Mission 2

Cập nhật: 15/10/2026. Ứng dụng xử lý được nhiều câu hỏi và cho người xem lần theo từng ý về nguồn. **Chất lượng câu trả lời từ nguồn thật chưa được người phụ trách xác nhận cuối.** Bộ kiểm thử phần mềm có **81 bài đạt** (`python -m pytest -q`); con số này nói phần mềm chạy đúng các tình huống đã viết, không chứng minh mọi nhận định thị trường đều đúng.

## Kỳ vọng → kết quả thực tế → đánh giá → bài học

| Tình huống | Kỳ vọng | Kết quả thực tế | Đánh giá | Bài học |
|---|---|---|---|---|
| **A01 — MABINOGI MOBILE, Hàn Quốc, nguồn thật** | Đọc nguồn về lượt tải, doanh thu và người dùng; đưa câu trả lời hẹp, có thể kiểm tra. | Đọc được 2 nguồn, tạo 6 ý qua kiểm tra tự động. Một số cách diễn đạt về chỉ số và nguyên nhân–kết quả vẫn cần xem lại với nguồn gốc. | **Đạt phần xử lý; chưa xác nhận chất lượng kết luận.** | Chạy xong không có nghĩa mọi câu chữ AI viết đã đúng. [Chi tiết](mvp-live-results-2026-10-15.md). |
| **A02 — Mobile MMORPG Việt Nam, Gemini tự tìm nguồn** | Tìm được nguồn và nêu tín hiệu theo thể loại. | Gemini trả lỗi máy chủ ở bước tìm nguồn; không có nguồn hoặc ý nào. | **Chưa đạt.** | Phải báo lỗi thu thập rõ ràng, không tự bịa câu trả lời. |
| **A02 — Mobile MMORPG Việt Nam, dùng đường dẫn có sẵn** | Nêu điều bài viết thực sự nói và phần số liệu còn thiếu. | Đọc được bài Gamota; một ý về **nhóm MMORPG, 4X và Team Battle** qua kiểm tra tự động. Bài không có doanh thu riêng MMORPG. | **Đạt một phần.** | Không lấy số chung của nhiều thể loại để kết luận riêng một thể loại. [Chi tiết](mvp-live-results-2026-10-15.md). |
| **O01 — tình huống mô phỏng đủ dữ liệu** | Các nguồn và ý phù hợp tạo được gợi ý sàng lọc. | 3 ý qua kiểm tra tự động, ứng dụng gợi ý “Tiếp tục”. | **Đạt luồng phần mềm**, không phải bằng chứng thị trường. | Cần tách mô phỏng khỏi dữ kiện thật. |
| **O02 — tình huống mô phỏng với game/thị trường khác** | Cùng ứng dụng xử lý câu hỏi khác, không gắn cứng MABINOGI. | Xử lý Game Beta tại Trung Quốc mà không ép gợi ý sàng lọc. | **Đạt luồng phần mềm.** | Cấu trúc nhập câu hỏi dùng lại được. |
| **O03/O04 — tình huống mô phỏng mâu thuẫn hoặc thiếu số liệu** | Hiện hai nguồn mâu thuẫn; không thay số liệu còn thiếu bằng chỉ số khác. | Mâu thuẫn và phần thiếu đều được nêu; ứng dụng không đưa kết luận chắc chắn. | **Đạt cách xử lý thận trọng.** | Thông tin thiếu cũng là một kết quả nghiên cứu cần cho người xem biết. |
| **O08 — tình huống mô phỏng AI hiểu ngược đoạn trích** | Đoạn nói “không có nhu cầu mạnh” phải ngăn ý “có nhu cầu mạnh”. | Kiểm tra tự động vẫn cho ý sai đi qua. Người phụ trách có thể mở nguồn và bác ý đó. | **Chưa đạt tự động.** | Cần kiểm tra ý nghĩa câu chữ, nhất là phủ định; hiện phải có con người đối chiếu. |
| **Liên Quân Mobile — lượt online người dùng báo** | Câu hỏi, game, kỳ đo và tiêu chí “thành công” nhất quán. | Trước bản sửa, game trong câu hỏi và đối tượng nhập không khớp; 3 nguồn đọc lỗi, không có ý nào hợp lệ. | **Chưa đạt ở lượt đó.** | Bản mới kiểm tra phạm vi trước khi gọi Gemini, nhưng chưa có lượt online kiểm tra lại. |

O01–O08 là **dữ liệu mô phỏng** để kiểm thử hành vi phần mềm. A01/A02 và Liên Quân là **lượt với nguồn thật**; các ví dụ A01/A02 trên giao diện đã được rút gọn, biên tập lại để người chấm mở bằng một nút, nên trạng thái ví dụ có thể khác lượt nghiên cứu gốc. Không tính việc biên tập đó là một lần gọi Gemini mới hay là người phụ trách đã duyệt kết luận.

## Giới hạn cần trình bày

- Kiểm tra tự động xem đoạn trích có xuất hiện trong nguồn, đúng game, thị trường và thời gian hay không. Nó **chưa xác nhận AI hiểu đúng ý nghĩa**; O08 chứng minh điều này.
- Trang web có thể chặn đọc, lỗi máy chủ hoặc thiếu chỉ số cần tìm. Khi đó ứng dụng báo điều chưa biết thay vì tự điền số.
- Chưa có kết luận thị trường cuối của A01/A02 được người phụ trách kiểm chứng và chấp nhận. [Ba câu trả lời bắt buộc](forced-decisions-draft.md) và [video demo](mission2-demo-captioned.mp4) giữ rõ giới hạn này.

Kết quả chi tiết cũ của T01–T03 và các lần thử khác được lưu trong [báo cáo lịch sử](test-report-history.md) và [báo cáo A01/A02](mvp-live-results-2026-10-15.md). Chúng không thay thế đánh giá hiện tại ở trên.
