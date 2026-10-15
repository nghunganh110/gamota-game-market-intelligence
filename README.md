# Gamota Game Market Intelligence — Mission 2 MVP

**Demo:** https://gamota-game-market-intelligence.streamlit.app/

**Bộ kiểm thử và kết quả thật:** [docs/mission2/test-report.md](docs/mission2/test-report.md)

**Ba câu trả lời bắt buộc:** [docs/mission2/forced-decisions-draft.md](docs/mission2/forced-decisions-draft.md)

**Video demo có phụ đề (2:13):** [docs/mission2/mission2-demo-captioned.mp4](docs/mission2/mission2-demo-captioned.mp4) · [Kịch bản bản có lời](docs/mission2/video-script.md)

MVP thử một giả thuyết hẹp: một câu hỏi nghiên cứu game có thể được chuyển thành nhận định truy ngược được tới claim, đoạn trích và nguồn; phần thiếu và độ tin cậy được hiện rõ để người phụ trách quyết định. Luồng là **câu hỏi → thu nguồn → trích claim → kiểm tra cơ học → nhận định sơ bộ → người review đối chiếu và viết kết luận cuối**. Ứng dụng không tự gán nhãn “đúng” cho một claim chỉ vì câu trích xuất hiện trên trang.

## Xem demo trong hai phút

1. Mở link demo, giữ chế độ **Ví dụ đã lưu — nguồn thật**, chọn **A01** và bấm **Mở case**. Đây là bản rút gọn, đã biên tập từ lượt Gemini thật; không gọi API, không phải bản đã được người review chấp nhận.
2. Đọc nhận định sơ bộ và mục **Điều chưa biết**. Mở tab **Claim & đoạn trích** để xem claim và trang gốc; sang **Nguồn & độ tin cậy** để xem chất lượng, độ phù hợp và ngày công bố.
3. Chọn **A02** và mở case thứ hai: câu hỏi về thể loại MMORPG ở Việt Nam cho thấy nguồn chỉ hỗ trợ nhận định nhóm thể loại, không có số riêng MMORPG. Tab **Người review quyết định** minh họa chỗ người phụ trách kiểm chứng và ghi nhận định cuối.
4. Để xem trường hợp sai có chủ đích, chuyển **Demo offline — synthetic** → **Giới hạn: diễn giải sai đoạn trích**. Đoạn trích phủ định nhưng claim khẳng định vẫn qua gate cơ học; reviewer có thể bác claim. Dữ liệu synthetic không phải dữ kiện thị trường.

**Nghiên cứu Gemini** cho phép đặt câu hỏi mới, để Gemini tìm nguồn hoặc nhập URL nguồn công khai đã chọn. Chế độ này dùng key server và mã truy cập riêng, tiêu thụ quota; không cần chạy live để xem demo. App có thể xuất brief Markdown và run JSON; JSON có thể chứa snapshot toàn văn nguồn, nên không tự động công khai.

## Kết quả kiểm thử và giới hạn

[Report hiện tại](docs/mission2/test-report.md) ghi từng case theo **kỳ vọng → thực tế → đạt/chưa đạt → bài học**, gồm nhiều câu hỏi, tình huống tốt, khó và thất bại. A01 live đọc được 2 nguồn và tạo 6 claim qua gate cơ học, nhưng có câu chữ cần thu hẹp trước khi chấp nhận. A02 Gemini tự tìm nguồn gặp `ServerError`; A02 với URL được chọn chỉ hỗ trợ một nhận định định tính hẹp. Chưa có nhận định live cuối được người review xác nhận. `completed` chỉ là trạng thái pipeline, không phải chứng nhận độ đúng của nghiên cứu.

MVP có thể trả về `partial` hoặc không đủ căn cứ khi nguồn không đọc được, sai chủ thể/thị trường/kỳ đo, thiếu chỉ số, hoặc mâu thuẫn. Chất lượng nhà xuất bản/phương pháp và độ phù hợp với câu hỏi được đánh giá riêng; reviewer có thể sửa đánh giá nguồn và claim, giữ lịch sử. Giới hạn lớn nhất hiện tại là kiểm tra chuỗi trích dẫn chưa hiểu ngữ nghĩa (ví dụ phủ định); nguồn web động/paywall và snapshot lịch sử cũng chưa được xử lý đầy đủ. Không dùng MVP để quyết định đầu tư nếu chưa kiểm chứng claim trọng yếu.

## Chạy local và cấu hình

Đã kiểm thử với Python 3.13; dependencies khóa trong `requirements.txt`.

```sh
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m streamlit run app.py --browser.gatherUsageStats false
```

Demo ví dụ đã lưu và synthetic chạy không cần key. Để bật Gemini, sao chép `.env.example` thành `.env` trên máy của bạn rồi điền key, model, mã truy cập, giới hạn sử dụng; xem [hướng dẫn cấu hình](docs/mission2/online-gemini-setup.md). `.env`, `runs/` và Cloud Secrets không được commit. Không đưa API key vào giao diện hoặc chat. Session cap chỉ giới hạn trình duyệt, không thay thế quota phía nhà cung cấp.

```sh
python -m pytest -q
python -m scripts.offline_report
```

## Cấu trúc bàn giao

| Thành phần | Vai trò |
|---|---|
| `app.py` | Trang vào, chọn demo/live/upload và cấu hình phiên Streamlit |
| `gmi/ui_results.py` | Trình bày nhận định, claim, nguồn, gap và form review |
| `gmi/pipeline.py`, `gmi/gemini.py`, `gmi/reader.py` | Điều phối, gọi model, đọc nguồn HTML/PDF |
| `gmi/validation.py`, `gmi/models.py` | Gate, cấu trúc dữ liệu và hành động review |
| `gmi/export.py`, `gmi/replay.py` | Brief/JSON và fixture offline |
| `fixtures/real_cases/` | Hai ví dụ nguồn thật đã rút gọn cho demo một nút |
| `tests/`, `docs/mission2/` | Kiểm thử, evidence và tài liệu nộp |

[Hướng dẫn bàn giao và checklist](docs/mission2/submission-handoff.md) nêu bước demo, trạng thái deploy và những việc chỉ chủ bài nộp có thể hoàn tất. Tài liệu Mission 1 nằm trong `docs/mission1/`; các kế hoạch/lần thử cũ trong `docs/mission2/` là lịch sử, không thay cho report hiện tại.
