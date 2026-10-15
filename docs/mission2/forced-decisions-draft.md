# Ba Forced Decisions — bản thảo để người dùng rà soát

**AI-PROPOSAL lịch sử, chưa sẵn sàng nộp.** T01–T03 và lượt online Liên Quân đã chạy live nhưng đều partial; chưa có brief được người dùng audit và chấp nhận. Nội dung bên dưới được viết trước các lượt live, cần viết lại theo [kiểm toán Mission 2](acceptance-gap-audit.md). Không tự coi lời văn này là quyết định mới của người dùng.

## 1. Phần quan trọng nhất được hiện thực hóa

Tôi chọn đường dẫn từ nhận định về claim, đoạn trích và phạm vi nguồn, kết hợp với review của con người. Người phụ trách cần thấy tại sao có đề xuất, nguồn đang đo gì và dữ liệu nào còn thiếu để quyết định có nghiên cứu sâu hơn. MVP hiện đã chạy được vòng này trên dữ liệu synthetic, với câu hỏi/game/thị trường khác nhau, source quality và relevance riêng, conflict, gap và override có lý do. Nếu cùng vòng này vượt kiểm tra trên live evidence và audit claim thì hướng giải quyết có cơ sở khả thi. Các test offline hiện tại chưa đủ để kết luận điều đó.

## 2. Thay đổi so với Mission 1 và bằng chứng khiến thay đổi

Phạm vi Mission 1 tập trung một game để kiểm chứng thiết kế. Mission 2 đã được tôi yêu cầu mở thành engine nhận câu hỏi tự do, có Research và Screening, giữ MABINOGI MOBILE là case chính nhưng không hard-code. Implementation tách trạng thái xử lý khỏi recommendation: lỗi timeout không biến thành kết luận game kém. Khi kiểm thử, tôi thấy quote matching chưa chứng minh claim diễn giải đúng, nên UI giữ nhãn mechanically checked và lưu review riêng. Đây là cụ thể hóa nguyên tắc evidence-centered đã chọn, chưa phải sự thay thế bằng semantic validation tự động. Offline replay được làm trước vì key có quyền dùng nhưng giới hạn sử dụng và cấu hình live còn thiếu; replay luôn có nhãn synthetic.

## 3. Tình huống xử lý chưa tốt và ưu tiên tiếp theo

Tình huống O08 cho thấy đoạn trích nói không có nhu cầu mạnh nhưng claim nói nhu cầu mạnh vẫn vượt validator. Nguyên nhân là code kiểm tra trích dẫn tồn tại và scope, chưa kiểm tra entailment. Thêm một model chấm claim không tự loại bỏ lỗi này. Tôi ưu tiên chạy các case live đã thiết kế, audit toàn bộ decision-driving claims, thu thập lỗi và xây bộ đánh giá ngữ nghĩa có cả phủ định, qualifiers, scope và số liệu. Nếu kết quả cho thấy Gemini attribution không dẫn tới tài liệu đọc được, tôi sẽ xem xét thay retrieval bằng quyết định kỹ thuật riêng. Chưa có cơ sở tuyên bố chất lượng nghiên cứu hoặc tiết kiệm thời gian.
