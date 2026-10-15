# Kịch bản quay video Mission 2 — khoảng 4 phút 30 giây

Đây là **kịch bản**, chưa phải file video. Quay màn hình app đang chạy trong phiên của chủ bài nộp. Không dùng API Gemini khi quay; hai ví dụ rút gọn đã lưu giúp demo lặp lại được. Khi nói về A01/A02, dùng đúng nhãn “lượt live đã lưu và biên tập, chưa có human acceptance”.

| Thời gian | Màn hình / lời nói chính |
|---|---|
| 0:00–0:35 | Bài toán: thông tin game nhiều, độ tin cậy khác nhau; mục tiêu là nhận định truy được tới chứng cứ và phần còn thiếu, để người phụ trách quyết định. |
| 0:35–1:00 | Mở app. Giải thích phần MVP chọn chứng minh: câu hỏi → nguồn → claim và quote → nhận định sơ bộ → review. Chỉ vào bốn tab kết quả. |
| 1:00–2:05 | Chọn **Ví dụ đã lưu — nguồn thật → A01 → Mở case**. Đọc nhận định sơ bộ, mở một claim và trang gốc. Chỉ ra thông tin chất lượng/độ phù hợp của nguồn và giới hạn số liệu. Nói rõ A01 pipeline hoàn tất nhưng claim chưa được người review duyệt. |
| 2:05–2:55 | Chọn **A02 → Mở case**. Đây là câu hỏi khác về Mobile MMORPG Việt Nam. Chỉ nguồn Gamota chỉ nói nhóm MMORPG/4X/Team Battle, không cho doanh thu riêng MMORPG. Chỉ mục “Điều chưa biết”; vì vậy nhận định phải hẹp. |
| 2:55–3:40 | Chuyển **Demo offline — synthetic → Giới hạn: diễn giải sai đoạn trích**. Mở claim sai dấu phủ định; chỉ rằng gate cơ học vẫn có thể cho qua. Demo form reviewer bác claim và finding biến mất. Nhắc case này là dữ liệu giả lập để kiểm thử lỗi. |
| 3:40–4:15 | Mở tab review của một case để chỉ cách người phụ trách viết nhận định cuối, gắn claim đã kiểm tra và lưu lý do. Xem report: case tốt kỹ thuật, case khó và failure được ghi theo kỳ vọng/thực tế/bài học. |
| 4:15–4:30 | Kết: ưu tiên tiếp theo là kiểm chứng ngữ nghĩa claim và cải thiện nguồn; nêu repo public, demo link và tài liệu ba Forced Decisions. |

Trước khi quay: kiểm tra app mở được khi đã đăng nhập, thử A01/A02 một lần, phóng to chữ đủ đọc và ẩn mọi Secrets/API key. Sau khi quay: kiểm tra thời lượng **dưới 5 phút**, âm thanh/chữ đọc được và link video có quyền xem cho người chấm. Không nói `completed` đồng nghĩa nhận định đã đúng; không gọi replay là lượt Gemini mới.
