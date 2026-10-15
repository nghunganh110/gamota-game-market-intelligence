# Deploy checklist — Streamlit Community Cloud

Repo public đã cập nhật: `https://github.com/nghunganh110/gamota-game-market-intelligence`, nhánh `main`, entrypoint `app.py`, dependencies `requirements.txt`, Python 3.13. Local suite: 56 passed. `.env` và `runs/` bị Git bỏ qua; `.env.example` không chứa credential. Bản demo public dự kiến chỉ hiển thị synthetic replay và quy trình reviewer, không chạy Gemini live.

**Chưa deploy:** chưa có tài khoản Streamlit/GitHub được kết nối trong phiên này và không có browser surface khả dụng để thực hiện UI. Lần thử trước người dùng giữ demo local sau khi Streamlit yêu cầu quyền GitHub; không coi lựa chọn đó là quyền để tự cấp OAuth.

Theo [hướng dẫn Streamlit](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy), mở `share.streamlit.io` bằng tài khoản của chủ repo, tạo app từ repository có sẵn, chọn `nghunganh110/gamota-game-market-intelligence`, `main`, `app.py`, Python 3.13. Việc [kết nối GitHub](https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started/connect-your-github-account) yêu cầu người dùng xem và chấp nhận quyền OAuth tại GitHub. Không nhập API key vào Streamlit secrets cho public demo.

Sau khi Streamlit báo deployed, xác minh URL `.streamlit.app` thực tế: mở app trong browser riêng, chọn từng case synthetic good, conflict, missing và semantic failure; kiểm tra câu trả lời sơ bộ và review claim sai O08 làm mất finding; kiểm tra JSON/Markdown export. Xác minh không có nút live chạy được khi server không cấu hình key/flags. Chỉ sau smoke test mới điền URL demo vào README/bài nộp.

Không coi repo URL, screenshot local hoặc trạng thái deploy pending là bằng chứng app đã online. Nếu quyền OAuth không được người dùng cấp hoặc deploy thất bại, giữ local demo và ghi lý do quan sát được theo yêu cầu Mission 2.
