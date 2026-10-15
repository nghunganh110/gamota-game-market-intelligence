# Ba Forced Decisions — bản thảo cuối để chủ bài nộp rà soát

Các câu dưới đây được Codex soạn từ implementation và kết quả kiểm thử hiện có. **Chủ bài nộp cần đọc, sửa theo nhận định của mình rồi mới dùng ở ngôi “tôi”.** Chưa có xác nhận của người dùng cho câu chữ này, và chưa có human acceptance đối với nhận định thị trường live.

## 1. Tôi chọn phần nào để hiện thực hóa, và vì sao?

Tôi chọn vòng chứng cứ có thể kiểm tra: từ một câu hỏi, thu và đọc nguồn, trích claim gắn đoạn nguyên văn, ghi chất lượng và độ phù hợp của nguồn, tạo nhận định có claim hỗ trợ, nêu phần còn thiếu, rồi để người phụ trách kiểm tra ngữ nghĩa và quyết định. Nếu vòng này hoạt động với nhiều câu hỏi thật, kết quả nghiên cứu có thể được dùng để quyết định **có nên nghiên cứu sâu hơn** mà không cần tin mù vào câu trả lời AI. MVP đã chạy được với câu hỏi về một game tại Hàn Quốc và một thể loại tại Việt Nam, bên cạnh các case synthetic; nhưng các lượt live hiện mới chứng minh một phần luồng kỹ thuật. Chưa có nhận định live cuối được người review chấp nhận, nên tôi chưa tuyên bố giả thuyết chất lượng nghiên cứu đã được chứng minh trọn vẹn.

## 2. Tôi đã đổi gì so với Mission 1, và vì sao?

Mission 1 mô tả khung nghiên cứu và quyết định cho một case trọng tâm. Khi hiện thực hóa, tôi giữ schema chung để nhập game hoặc thể loại, thị trường, kỳ đo và tiêu chí, thay vì hard-code một bài mẫu. Tôi tách **trạng thái pipeline** khỏi **khuyến nghị**: lỗi đọc nguồn hoặc model không thể bị hiểu là game kém tiềm năng. Qua lượt Liên Quân và T01–T03, tôi thêm kiểm tra chủ thể/tiêu chí/kỳ đo trước khi gọi model, cho phép URL nguồn do người dùng chọn và hiển thị lý do claim bị loại. Qua A01/A02, tôi nhận ra quote matching chỉ chứng minh truy vết chứ không chứng minh ý nghĩa; vì vậy reviewer có thể thu hẹp hoặc bác claim, còn bản AI ban đầu vẫn được giữ. Tôi cũng đưa hai case live đã rút gọn lên giao diện một nút để demo không phụ thuộc key/quota. Đây là thay đổi do lỗi quan sát được, không phải bằng chứng hệ thống đã tự chữa mọi lỗi diễn giải.

## 3. MVP xử lý kém nhất ở đâu, nguyên nhân và ưu tiên tiếp?

Tình huống nguy hiểm nhất là claim **diễn giải ngược hoặc mạnh hơn đoạn trích** mà vẫn qua gate cơ học. O08 synthetic tái hiện phủ định bị đảo nghĩa; A01 live có các nhãn “gross revenue”, “active users” và quan hệ nhân quả chưa được quote xác nhận đủ. A02 cho thấy một failure khác: discovery gặp `ServerError`, còn nguồn về nhóm thể loại không có số riêng MMORPG. Nguyên nhân là kiểm tra hiện tại dựa vào chuỗi, scope và metadata; retrieval web có thể lỗi và dữ liệu công khai không luôn đúng đơn vị phân tích. Nếu có thêm thời gian, tôi ưu tiên audit claim ảnh hưởng kết luận trên nhiều run thật, lập tập lỗi phủ định/chỉ số/phạm vi, rồi cải thiện kiểm tra semantic support và chiến lược nguồn trước khi thêm tính năng hoặc tự động đưa quyết định. Trong thời gian đó, sản phẩm phải giữ kết luận sơ bộ, gap và review của con người tách biệt.
