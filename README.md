# Game Market Intelligence — MVP Mission 2

[Ứng dụng trực tuyến](https://gamota-game-market-intelligence.streamlit.app/) · [Video demo có phụ đề, 2 phút 13 giây](docs/mission2/mission2-demo-captioned.mp4) · [Kết quả kiểm thử](docs/mission2/test-report.md) · [Ba câu trả lời bắt buộc](docs/mission2/forced-decisions-draft.md)

## Sản phẩm giải quyết việc gì?

Khi hỏi AI về một game hoặc một thể loại, người dùng cần biết câu trả lời dựa vào nguồn nào, nguồn đó có phù hợp không, và còn thiếu thông tin gì. MVP này làm rõ đường đi của kết luận:

**Câu hỏi → tìm và đọc nguồn → rút ra từng ý có dẫn chứng → câu trả lời sơ bộ → người phụ trách đối chiếu nguồn và kết luận.**

Mỗi ý được đánh số C1, C2… để người xem mở đoạn trích và trang gốc. Việc tìm thấy đoạn trích **chưa chứng minh AI hiểu đúng đoạn đó**. Vì vậy ứng dụng phân biệt kiểm tra tự động với xác nhận của người phụ trách.

## Xem thử trong hai phút

1. Mở ứng dụng, chọn **Ví dụ từ nguồn thật**, rồi bấm **Mở ví dụ** cho A01. Đọc câu trả lời sơ bộ về MABINOGI MOBILE tại Hàn Quốc. Mở tab **Ý rút ra & đoạn trích** để đối chiếu một ý với nguồn; tab **Nguồn & độ tin cậy** cho biết cách đánh giá từng nguồn.
2. Chọn A02 để xem một câu hỏi khác: thể loại MMORPG tại Việt Nam. Nguồn nói về **nhóm nhiều thể loại**, chưa cho doanh thu riêng MMORPG. Ứng dụng nêu rõ thông tin còn thiếu thay vì tự suy ra con số.
3. Chọn **Tình huống mô phỏng** → **Giới hạn: diễn giải sai đoạn trích**. Đoạn nguồn nói *không có nhu cầu mạnh* nhưng AI lại viết *có nhu cầu mạnh*. Đây là lỗi mà kiểm tra tự động chưa bắt được; người phụ trách có thể bác ý sai. Tình huống này là dữ liệu giả định, không phải sự thật thị trường.

Hai ví dụ A01/A02 được biên tập rút gọn từ các lần nghiên cứu bằng Gemini đã lưu. Mở chúng không tốn lượt gọi Gemini. Chúng là **kết quả sơ bộ, chưa được người phụ trách xác nhận**. Mục **Nghiên cứu bằng Gemini** dành cho câu hỏi mới, cần cấu hình của chủ ứng dụng và có thể tốn hạn mức API.

## Kết quả thực tế và giới hạn

[Báo cáo kiểm thử](docs/mission2/test-report.md) ghi hơn năm tình huống theo mẫu **kỳ vọng → thực tế → đạt/chưa đạt → bài học**. A01 đã đọc được hai nguồn và tạo câu trả lời sơ bộ, nhưng một số cách diễn đạt cần đối chiếu lại. A02 cho thấy cả lỗi tìm nguồn và giới hạn của dữ liệu theo thể loại. Có tình huống kiểm thử mà AI hiểu ngược đoạn trích. Vì vậy chúng tôi **chưa coi chất lượng nghiên cứu đã được chứng minh hoàn toàn**, dù phần mềm đã chạy được.

Nguồn web không đọc được, ngày công bố không rõ, dữ liệu sai thị trường hoặc thiếu số liệu đều được báo ra. Người phụ trách có thể sửa đánh giá nguồn, bác hoặc viết lại một ý, và ghi kết luận cuối kèm lý do. Ứng dụng chưa tự kiểm tra được mọi lỗi diễn giải, chưa đọc được mọi trang động hoặc nội dung trả phí, và chưa thay thế quyết định của con người.

Mission 1 chọn MABINOGI MOBILE để xem cơ hội tại Việt Nam. Ví dụ A01 của MVP chỉ kiểm tra tín hiệu ra mắt tại Hàn Quốc, nơi có nguồn công khai đọc được; **chưa có kết luận về cơ hội tại Việt Nam**. Đây là thay đổi phạm vi để chứng minh quy trình, được giải thích trong [ba câu trả lời bắt buộc](docs/mission2/forced-decisions-draft.md).

## Chạy trên máy cá nhân

Yêu cầu Python 3.13. Hai chế độ xem ví dụ và mô phỏng không cần khóa API.

```sh
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m streamlit run app.py --browser.gatherUsageStats false
```

Chạy kiểm thử:

```sh
python -m pytest -q
```

Để dùng Gemini, điền khóa API, tên mô hình và mã truy cập vào `.env` trên máy hoặc mục Secrets của Streamlit Cloud theo [hướng dẫn](docs/mission2/online-gemini-setup.md). Không đưa khóa vào GitHub hoặc giao diện. Tệp JSON tải từ ứng dụng có thể chứa nội dung nguồn đầy đủ, nên chỉ chia sẻ sau khi kiểm tra.

## Bàn giao

- `app.py`: chọn chế độ xem, nhập câu hỏi và mở kết quả.
- `gmi/ui_results.py`: hiển thị câu trả lời, nguồn, các ý được rút ra và biểu mẫu kiểm chứng.
- `gmi/pipeline.py`, `gmi/reader.py`, `gmi/gemini.py`: điều phối nghiên cứu, đọc nguồn, gọi Gemini.
- `gmi/validation.py`, `gmi/models.py`, `gmi/export.py`: kiểm tra dữ liệu, lưu đánh giá và xuất báo cáo.
- `fixtures/real_cases/`: hai ví dụ rút gọn; `tests/`: kiểm thử phần mềm.

Xem [hướng dẫn bàn giao](docs/mission2/submission-handoff.md) và [lời thuyết trình ngắn, dễ dùng](docs/mission2/presentation-notes.md). Các tài liệu cũ trong `docs/mission2/` lưu lịch sử phát triển; báo cáo kiểm thử liên kết phía trên là trạng thái hiện tại.
