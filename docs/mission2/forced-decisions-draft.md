# Ba câu trả lời bắt buộc — bản thảo để chủ bài nộp rà soát

Phần này được soạn từ sản phẩm và kết quả kiểm thử hiện có. **Bạn cần đọc và sửa theo quan điểm của mình trước khi nộp ở ngôi “tôi”.** Chưa có người phụ trách xác nhận kết luận thị trường cuối của các ví dụ thật.

## 1. Tôi chọn làm phần nào? Vì sao phần đó quan trọng?

Tôi chọn làm rõ **vì sao AI đưa ra một câu trả lời**. Ứng dụng bắt đầu từ câu hỏi, tìm và đọc nguồn, rút ra từng ý có dẫn chứng, cho người xem mở đoạn trích và trang gốc, rồi chỉ rõ thông tin còn thiếu. Người phụ trách là người đối chiếu và viết kết luận cuối. Nếu cách này hoạt động với nhiều câu hỏi, AI có thể giúp nghiên cứu nhanh hơn mà người dùng vẫn kiểm tra được trước khi quyết định có nghiên cứu sâu hơn hay không. MVP đã chạy với câu hỏi về một game tại Hàn Quốc và một thể loại tại Việt Nam. Tuy nhiên, tôi chưa khẳng định câu trả lời từ nguồn thật đã chính xác hoàn toàn: những ý quan trọng vẫn cần người phụ trách kiểm chứng.

## 2. Tôi thay đổi gì so với Mission 1? Điều gì khiến tôi thay đổi?

Mission 1 tập trung vào cách nghiên cứu và ra quyết định cho một ví dụ chính. Khi làm sản phẩm, tôi mở rộng phần nhập liệu để hỏi về nhiều game hoặc thể loại, thị trường và kỳ đo khác nhau. Tôi cũng tách **việc ứng dụng chạy xong** khỏi **việc câu trả lời đáng tin**: nguồn không đọc được hoặc AI gặp lỗi không thể bị hiểu là game thiếu tiềm năng. Các lần thử về Liên Quân và những câu hỏi khác cho thấy cần kiểm tra game, tiêu chí và kỳ đo trước khi gọi Gemini; đồng thời cho người dùng chọn sẵn nguồn khi cần. Với A01/A02, tôi thấy việc tìm được đoạn trích trên trang vẫn chưa đủ để tin rằng AI diễn giải đúng. Vì vậy người phụ trách có thể bác hoặc viết lại một ý, còn bản AI viết ban đầu vẫn được lưu để đối chiếu. Hai ví dụ đã lưu giúp trình bày sản phẩm mà không phụ thuộc khóa API trong lúc demo.

## 3. Sản phẩm còn yếu nhất ở đâu? Tôi sẽ ưu tiên cải thiện gì?

Rủi ro lớn nhất là AI **hiểu sai hoặc nói mạnh hơn nguồn**. Trong một tình huống mô phỏng, đoạn nguồn nói “không có nhu cầu mạnh” nhưng AI lại viết “có nhu cầu mạnh”; kiểm tra tự động chưa phát hiện. Ở A01, một số cách gọi chỉ số và quan hệ nguyên nhân–kết quả cũng cần đối chiếu lại. A02 cho thấy trường hợp khác: Gemini gặp lỗi khi tìm nguồn; khi dùng một bài viết có sẵn, bài đó chỉ nói về nhóm nhiều thể loại, không có số riêng MMORPG. Nếu có thêm thời gian, tôi sẽ kiểm tra nhiều câu trả lời thật cùng người phụ trách, tập hợp các lỗi diễn giải về phủ định, chỉ số và phạm vi, rồi cải thiện cách kiểm tra ý nghĩa và chọn nguồn. Trước khi làm được điều đó, sản phẩm phải tiếp tục ghi rõ đâu là câu trả lời sơ bộ và đâu là kết luận đã được con người xác nhận.
