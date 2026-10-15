# Deploy checklist — Streamlit Community Cloud

Repo public: `https://github.com/nghunganh110/gamota-game-market-intelligence`, nhánh `main`, entrypoint `app.py`, dependencies `requirements.txt`, Python 3.13. `.env` và `runs/` bị Git bỏ qua; `.env.example` không chứa credential. Bản demo có thể dùng Gemini live nếu chủ key cấu hình Cloud Secrets và mã truy cập riêng theo [hướng dẫn này](online-gemini-setup.md).

**Chưa deploy:** chưa có tài khoản Streamlit/GitHub được kết nối trong phiên này và không có browser surface khả dụng để thực hiện UI. Lần thử trước người dùng giữ demo local sau khi Streamlit yêu cầu quyền GitHub; không coi lựa chọn đó là quyền để tự cấp OAuth.

Theo [hướng dẫn Streamlit](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy), mở `share.streamlit.io` bằng tài khoản của chủ repo, tạo app từ repository có sẵn, chọn `nghunganh110/gamota-game-market-intelligence`, `main`, `app.py`, Python 3.13. Việc [kết nối GitHub](https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started/connect-your-github-account) yêu cầu người dùng xem và chấp nhận quyền OAuth tại GitHub. Nếu bật Gemini, nhập key vào **Cloud Secrets**, không vào repo hoặc UI; giữ mã truy cập riêng với chủ key.

Sau khi Streamlit báo deployed, xác minh URL `.streamlit.app` thực tế: mở app trong browser riêng, chọn từng case synthetic good, conflict, missing và semantic failure; kiểm tra câu trả lời sơ bộ và review claim sai O08 làm mất finding; kiểm tra JSON/Markdown export. Xác minh nút live bị khóa khi thiếu cấu hình/mã; nếu đã cấu hình thì chỉ người có mã mới mở được. Chỉ chạy test Gemini thật trong giới hạn mới được chủ key xác nhận. Chỉ sau smoke test mới điền URL demo vào README/bài nộp.

Không coi repo URL, screenshot local hoặc trạng thái deploy pending là bằng chứng app đã online. Nếu quyền OAuth không được người dùng cấp hoặc deploy thất bại, giữ local demo và ghi lý do quan sát được theo yêu cầu Mission 2.
