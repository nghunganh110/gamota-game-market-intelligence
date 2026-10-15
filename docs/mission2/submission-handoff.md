# Bàn giao bài nộp Mission 2

Ngày cập nhật: 2026-10-15. Repo public: https://github.com/nghunganh110/gamota-game-market-intelligence. URL demo do chủ bài nộp cung cấp: https://gamota-game-market-intelligence.streamlit.app/. Kiểm tra HTTP không đăng nhập ngày 15/10/2026 trả `303` tới luồng login lặp lại, vì vậy **người chấm chưa chắc mở được demo** và phiên này chưa xác minh được giao diện sau deploy. Bản local và Streamlit AppTest đã chạy. Theo [hướng dẫn chia sẻ của Streamlit](https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app), chủ app có thể vào App settings → Sharing → “Who can view this app” → “This app is public and searchable”.

## Nội dung đã chuẩn bị

- MVP Streamlit cho nhiều câu hỏi; mặc định mở **hai ví dụ nguồn thật đã lưu** A01/A02. Chúng là bản biên tập rút gọn từ Gemini live, không tốn API, không có human review giả. Chế độ synthetic dùng để tái hiện good/conflict/missing/semantic failure. Chế độ Gemini nhận câu hỏi mới và URL nguồn nếu có mã truy cập.
- UI dẫn người xem từ nhận định sơ bộ, claim và đoạn trích, chất lượng/độ phù hợp của nguồn, gap, tới form review và export. `app.py` chứa routing/input; `gmi/ui_results.py` chứa trình bày và reviewer actions; pipeline/validation/models không phụ thuộc Streamlit.
- [Bộ kiểm thử](test-report.md) có trên năm tình huống theo format đề bài. A01 live: pipeline hoàn tất nhưng claim cần audit; A02 auto: discovery lỗi; A02 guided: nhận định nhóm thể loại, không có số riêng MMORPG. Không gán nhãn research PASS khi thiếu human acceptance.
- [Ba Forced Decisions](forced-decisions-draft.md) đã cập nhật theo kết quả A01/A02. [Video demo có phụ đề, 2:13](mission2-demo-captioned.mp4) được dựng từ ảnh chụp giao diện local, H.264 1920×1080, không có âm thanh hay API call khi quay. Video trình bày A01/A02 và lỗi synthetic; [kịch bản](video-script.md) dành cho bản thuyết minh bằng lời nếu chủ bài nộp muốn quay lại.

## Demo cho người chấm

1. Vào URL và mở **A01** bằng một nút; đọc nhận định rồi mở tab Claim và Nguồn. Nhấn mạnh nguồn khác nhau về phương pháp và độ phù hợp.
2. Mở **A02** để thấy câu hỏi thứ hai và phần dữ liệu riêng thể loại còn thiếu.
3. Mở synthetic **Giới hạn: diễn giải sai đoạn trích**, cho reviewer bác claim sai. Đây là tình huống thất bại được công khai, không phải kết quả nghiên cứu thị trường.
4. Mở report và Forced Decisions từ README. Nếu cần live, cấu hình Secrets theo [hướng dẫn](online-gemini-setup.md); demo bài nộp không cần tốn quota.

## Cần chủ bài nộp hoàn tất

- Trong tài khoản Streamlit Cloud, kiểm tra **App settings → Sharing** và bật **This app is public and searchable** nếu bài nộp cần link mở tự do; sau đó dùng cửa sổ ẩn danh mở URL, chọn A01/A02 và kiểm tra các tab. Nếu chủ ý giữ app riêng tư, mời đúng người chấm và ghi hướng dẫn đăng nhập trong bài nộp.
- Đọc/sửa ba câu Forced Decisions để chúng đúng quan điểm cá nhân; không nhận bản AI soạn là lời xác nhận sẵn.
- Xem lại [video có phụ đề 2:13](mission2-demo-captioned.mp4) và xác nhận nó thể hiện đúng điều bạn muốn nộp; tải file này lên nơi HR/Gamota yêu cầu và kiểm tra quyền xem. Có thể quay bản có lời theo [kịch bản](video-script.md) nếu cần. Sau đó nộp link repo, demo, video và report theo form HR/Gamota. Việc upload/nộp trong tài khoản của chủ bài nộp chưa được thực hiện bởi Codex.
- Nếu muốn tuyên bố kết quả nghiên cứu A01/A02 đã được xác nhận, cần mở trang gốc, review claim trọng yếu trong app, ghi lý do và xuất brief mới. Bài nộp hiện có thể mô tả trung thực chúng là kết quả live sơ bộ và đánh giá giới hạn của MVP.

## Rủi ro và dữ liệu

Không commit `.env`, Secrets hoặc `runs/`: các run local có thể chứa snapshot toàn văn nguồn. Fixture `fixtures/real_cases/` chỉ giữ đoạn trích ngắn và link gốc. Public app live dùng key server và mã truy cập; giới hạn per-session không là giới hạn chi phí toàn tài khoản. Tính đúng ngữ nghĩa vẫn cần người kiểm chứng; `mechanically_checked` và `completed` chỉ nói về gate/phần mềm.
