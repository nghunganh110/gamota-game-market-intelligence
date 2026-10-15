# Lời giải thích ngắn khi demo

Bạn có thể nói gần như nguyên văn đoạn này trong khoảng 45–60 giây:

> “Gamota cần nghiên cứu thị trường game, nhưng câu trả lời của AI chỉ hữu ích khi người phụ trách kiểm tra được nó dựa vào đâu. Tôi làm một ứng dụng nhận câu hỏi, tìm và đọc nguồn, rồi tách câu trả lời thành từng ý. Mỗi ý có đoạn trích và đường dẫn để mở trang gốc. Ứng dụng cũng nói rõ thông tin nào còn thiếu và nguồn nào không phù hợp. Phần mềm kiểm tra tự động được một số lỗi đơn giản, nhưng chưa hiểu hết ý nghĩa của câu chữ. Vì vậy người phụ trách có bước xác nhận hoặc bác từng ý trước khi đưa ra kết luận cuối.”

Khi mở A01, hãy nói: “Đây là ví dụ về một game ở Hàn Quốc. Ứng dụng đọc được hai nguồn và nêu tín hiệu ra mắt, nhưng kết luận vẫn là sơ bộ.” Khi mở A02: “Nguồn nói về một nhóm thể loại; không thể lấy số của cả nhóm rồi gán riêng cho MMORPG.” Khi mở tình huống mô phỏng: “Ở đây AI hiểu ngược chữ *không*. Tôi giữ lỗi này trong bộ kiểm thử để thấy rõ giới hạn và vị trí con người cần kiểm tra.”

Nếu giám khảo hỏi về những chữ còn xuất hiện trong tệp dữ liệu kỹ thuật:

| Trong mã/tệp kỹ thuật | Cách giải thích bằng lời |
|---|---|
| `claim`, mã C1/C2 | Một ý cụ thể AI rút ra từ nguồn; mã giúp lần tới đúng đoạn trích. |
| `quote` | Đoạn chữ lấy từ trang nguồn để đối chiếu. |
| `gate` | Bước kiểm tra tự động, ví dụ đúng game, đúng kỳ đo, tìm thấy đoạn trích. |
| `review` | Người phụ trách đọc nguồn và xác nhận, sửa hoặc bác một ý. |
| `completed` | Ứng dụng đã xử lý xong lượt đó; chưa nói câu trả lời đã đúng. |

Bạn không cần dùng các từ tiếng Anh trong phần trình bày. Nói “ý được rút ra”, “đoạn trích”, “kiểm tra tự động” và “người phụ trách xác nhận” là đủ.
