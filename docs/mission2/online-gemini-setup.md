# Gemini trên Streamlit Community Cloud

Repo public chứa code, không chứa `.env` hoặc key. Streamlit Cloud nhận cấu hình riêng qua **Secrets**; các giá trị TOML ở cấp gốc được cung cấp cho app như biến môi trường ([Streamlit Secrets](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management), [Streamlit secrets API](https://docs.streamlit.io/develop/concepts/connections/secrets-management)).

1. Tại `share.streamlit.io`, tạo app từ `nghunganh110/gamota-game-market-intelligence`, nhánh `main`, file `app.py`. Trong Advanced settings chọn Python 3.13.
2. Trong **Secrets** dán mẫu TOML dưới đây, điền bốn giá trị đang để trống bằng key, model, mã truy cập và giới hạn sử dụng mới của bạn. Nếu app đã deploy: **Settings → Secrets → Save**. Không dán các giá trị thật vào chat, GitHub issue, README hoặc `.env.example`.
3. Dùng mã truy cập Gemini riêng, ngẫu nhiên và dài; giữ mã này với những người được phép dùng key. Trên app public, phần demo offline vẫn mở cho mọi người, còn nút Gemini chỉ bật sau khi nhập mã.
4. Mở tab ẩn danh để thử: chọn **Nghiên cứu Gemini**, xác nhận nút **Nghiên cứu** bị khóa khi chưa nhập mã; nhập mã để mở. Chạy một câu hỏi thật chỉ sau khi đã xác định giới hạn sử dụng mới. Mỗi run dự kiến tối đa hai API attempts (một discovery và một extraction), không retry tự động.

```toml
GEMINI_API_KEY = ""
GEMINI_MODEL = ""
GMI_LIVE_ACCESS_CODE = ""
GMI_LIVE_ENABLED = "1"
GMI_KEY_AUTHORIZED = "1"
GMI_MAX_CALLS = "2"
GMI_BUDGET_NOTE = ""
```

Mẫu là **TOML**, nên chuỗi cần dấu ngoặc kép. `.env` local vẫn dùng dạng `KEY=value` và không được đẩy lên GitHub. Không tái sử dụng ghi chú giới hạn T03 đã tiêu hết. `GMI_MAX_CALLS` chỉ đếm attempts trong **một phiên trình duyệt**; mở phiên khác có thể tiếp tục gọi. Mã truy cập cũng không phải trần chi phí. Nếu tài khoản có billing, cân nhắc đặt project spend cap trong [Google AI Studio](https://ai.google.dev/gemini-api/docs/billing/) trước khi bật live; cap có thể có độ trễ và phát sinh vượt mức.

Repo public khiến app public theo mặc định. Nếu chỉ nhóm nhỏ cần dùng live, đổi **Settings → Sharing → Only specific people can view this app** theo [Streamlit sharing](https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app), rồi mời đúng người cần xem. Streamlit hiện cho phép một private app mỗi tài khoản Community Cloud. Khi chưa có key hoặc mã truy cập, chế độ Gemini vẫn bị khóa và demo synthetic hoạt động.
