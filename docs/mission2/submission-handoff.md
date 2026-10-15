# Bàn giao bài nộp Mission 2

Cập nhật: 15/10/2026. [Mã nguồn công khai](https://github.com/nghunganh110/gamota-game-market-intelligence) · [Ứng dụng trực tuyến](https://gamota-game-market-intelligence.streamlit.app/) · [Video demo có phụ đề, 2:13](mission2-demo-captioned.mp4).

Ứng dụng đã được kiểm thử trên máy cá nhân. Tuy nhiên, khi mở đường dẫn trực tuyến mà chưa đăng nhập, trình duyệt bị chuyển đến màn hình đăng nhập Streamlit. **Chủ ứng dụng cần kiểm tra quyền xem trước khi gửi link cho người chấm.** Theo [hướng dẫn chính thức của Streamlit](https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app), vào App settings → Sharing → “Who can view this app” và chọn “This app is public and searchable” nếu muốn ai có link cũng xem được. Sau đó thử lại bằng cửa sổ ẩn danh.

## Đã chuẩn bị

- Ứng dụng nhận nhiều câu hỏi; hai ví dụ từ nguồn thật A01/A02 mở bằng một nút mà không tốn lượt gọi Gemini. Tình huống mô phỏng cho thấy sản phẩm xử lý đủ dữ liệu, mâu thuẫn, thiếu dữ liệu và một lỗi hiểu ngược đoạn trích.
- Giao diện dẫn từ câu trả lời sơ bộ tới từng ý, đoạn trích, trang nguồn, điều chưa biết và chỗ người phụ trách ghi kết luận. Các thuật ngữ kỹ thuật được giữ trong mã và tệp dữ liệu, còn màn hình chính dùng lời nói thông thường.
- [Báo cáo kiểm thử](test-report.md) có hơn năm tình huống theo mẫu đề bài. [Ba câu trả lời bắt buộc](forced-decisions-draft.md) đã viết theo kết quả thật và cần chủ bài nộp rà soát.
- [Video có phụ đề 2:13](mission2-demo-captioned.mp4) dùng ảnh chụp giao diện local, định dạng H.264 1920×1080, không có âm thanh và không lộ khóa API. [Kịch bản có lời](video-script.md) và [lời giải thích 60 giây](presentation-notes.md) có sẵn nếu muốn tự quay lại.

## Cách demo

1. Mở **A01**. Đọc câu trả lời sơ bộ, mở một ý để xem đoạn trích và trang gốc. Chỉ cách ứng dụng đánh giá mức phù hợp của nguồn.
   Nói rõ A01 dùng số liệu Hàn Quốc để chứng minh quy trình, **chưa trả lời câu hỏi cơ hội MABINOGI tại Việt Nam** của Mission 1.
2. Mở **A02**. Nói rằng nguồn nêu **nhóm** thể loại, chưa có doanh thu riêng MMORPG. Chỉ phần thông tin còn thiếu.
3. Mở tình huống mô phỏng **Giới hạn: diễn giải sai đoạn trích**. Chỉ rõ chữ “không” trong nguồn và cho thấy người phụ trách có thể bác ý AI viết sai.
4. Mở [báo cáo kiểm thử](test-report.md) và [ba câu trả lời](forced-decisions-draft.md). Nói rõ ví dụ thật là kết quả sơ bộ, chưa được người phụ trách chấp nhận là kết luận thị trường cuối.

## Chủ bài nộp cần làm

1. Chỉnh quyền xem ứng dụng trong Streamlit Cloud, thử A01/A02 trong cửa sổ ẩn danh sau khi bản mới cập nhật.
2. Đọc và sửa ba câu trả lời bắt buộc cho đúng quan điểm cá nhân.
3. Xem video, tải lên nơi nhận bài và kiểm tra quyền xem; dùng bản có phụ đề hoặc quay bản có lời theo kịch bản.
4. Nộp link mã nguồn, ứng dụng, video và báo cáo theo hướng dẫn của HR/Gamota. Codex chưa thực hiện thao tác nộp trong tài khoản của bạn.

Tệp `.env` và dữ liệu nghiên cứu đầy đủ trong `runs/` không được đưa lên GitHub. Hai ví dụ công khai chỉ giữ đoạn trích ngắn và link nguồn. Ứng dụng vẫn cần con người đối chiếu những ý ảnh hưởng quyết định; trạng thái “Đã xử lý” không phải chứng nhận câu trả lời đúng.
