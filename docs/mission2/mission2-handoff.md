# Bàn giao Mission 2 sang phiên Codex mới

## Yêu cầu hiện tại của người dùng

> bây giờ bạn hãy giúp tôi khởi tạo 1 repo mới và làm với phiên codex mới trên đó, tôi không muốn làm trên work nữa

Người dùng muốn một phiên **Codex local mới**, repo Git riêng cho Mission 2 và tiếp tục implementation ở đó. Không tạo một phiên ChatGPT Work cloud mới. Không lập trình tiếp trong workspace cũ.

## Các quyết định đã xác nhận

- Đã vượt Mission 1 theo thông tin người dùng cung cấp; đang làm Mission 2 MVP ba ngày.
- Problem: sàng lọc cơ hội game có căn cứ cho Publishing/Strategy Lead.
- Evidence-centered hybrid: AI tìm nguồn, đọc/trích claim và tạo brief; con người quyết định cuối, có thể override với lý do.
- Recommendation Tiếp tục/Tạm giữ/Dừng; thiếu dữ liệu không mặc định là Dừng.
- MABINOGI MOBILE là case chính, không được hard-code; phải xử lý nhiều câu hỏi và game/thể loại khác.
- Người dùng quen Python và có Gemini API key.
- Người dùng đã duyệt phương án bằng câu: `tôi xác nhận phương án nhé`.
- Stack được duyệt: Python + Streamlit + Gemini, tìm nguồn qua Gemini rồi đọc nội dung riêng; Pydantic và quy tắc Python; export JSON/Markdown. Chi tiết trong kế hoạch.

## Key và chi phí

Nguyên văn người dùng: `Tôi đang có API Key của nguời khác cho cũng không biết hạn mức như thế nào ?`

Chưa có ngân sách hoặc quota được xác nhận, chưa có key trong workspace/env được kiểm tra. Không yêu cầu dán key trong chat hoặc commit key. Chưa được phép suy ra dùng API không giới hạn; chưa gọi API Gemini của người dùng. Tiếp tục implementation, test offline và đọc nguồn công khai khi có quyền truy cập; live Gemini mặc định tắt cho đến khi chủ key/người dùng xác nhận quyền và giới hạn sử dụng. Không tự bật billing.

## Tài liệu nguồn cần sao chép vào repo mới

Workspace cũ: `/home/hunganh/Documents/Codex/2026-10-09/t-i-ang-tham-gia-ch`

Các file đã có:

- `outputs/mission2-technical-plan.md`: scope, kiến trúc, trade-off, 10 test cases, tiêu chí và M0–M5. Lưu ý dòng đầu vẫn phản ánh thời điểm trước duyệt; xác nhận trong handoff này và log có ưu tiên mới hơn.
- `outputs/mission2-evidence-log.md`: prompt Mission 2 nguyên văn và quyết định, cần thêm xác nhận duyệt và thông tin key.
- `outputs/evidence-log.md`: log Mission 1 EL-001 đến EL-006, không timestamp, đã bỏ EL-000.
- `outputs/mabinogi-research-brief-claim-ledger.md`: research lịch sử; không coi là kết quả mới đã chạy bằng MVP.
- `outputs/Mission_1_Game_Market_Intelligence.pdf`: bản chính 5 trang.
- `outputs/Mission_1_Game_Market_Intelligence.docx`: bản Word tương ứng.
- `outputs/Mission_1_Game_Market_Intelligence_Complete.pdf`: bản ghép 13 trang gồm 5 trang báo cáo + 8 trang Evidence Log.
- `outputs/mission2-handoff.md`: file này.

Copy có chọn lọc; không copy `.venv`, toàn bộ cache, metadata riêng của app hoặc bất cứ secret nào. Giữ nguyên các bản gốc trong workspace cũ. Nếu public repo, chỉ đưa tài liệu thích hợp sau khi kiểm tra thông tin; không công bố dữ liệu nhạy cảm.

## Trạng thái đã thực hiện

- Đã đọc tài liệu Mission 1 và tài liệu kỹ thuật chính thức, soạn phương án và test plan.
- Chưa có mã ứng dụng, test pass, live API run, GitHub repo hoặc deploy.
- Thử cài dependencies đã thất bại; không được ghi là môi trường đã sẵn sàng.
- `mission2-mvp/` trong workspace cũ hiện chỉ chứa `.venv`; không có source code cần chuyển.
- Root workspace cũ không phải Git repo; `.git` là một directory bảo vệ chỉ đọc. Không cố ghi/xóa nó. Trong phiên mới, nếu root cũng bị bảo vệ tương tự, tạo repo trong subdirectory riêng và dùng thư mục đó cho mọi thao tác coding.

## Quan sát môi trường từ phiên cũ

- Python hệ thống: `/home/hunganh/miniconda3/bin/python3`, phiên bản 3.13.12; `uv` có sẵn; Git 2.48.1.
- Có sẵn pydantic/httpx/pytest trên Python hệ thống; thiếu streamlit/trafilatura/google-genai/pypdf tại lần kiểm tra đó.
- Runtime bundled Python 3.12 có pypdf nhưng thiếu streamlit/google-genai/httpx/pytest.
- Network permission request ở phiên cũ không trả grant. Không khẳng định network ở phiên mới giống hệt; kiểm tra theo quyền của phiên mới.
- Cache uv gốc chỉ đọc. Lần `uv venv` đầu lỗi lock cache; không phải lỗi ứng dụng.
- Đã tạo một venv trong workspace cũ khi đổi cache dir, nhưng `uv pip install --offline` lỗi không resolve được streamlit trong cache. Không copy nguyên cache 16 GB hoặc cố ghi cache gốc.
- Không có GEMINI_API_KEY/GOOGLE_API_KEY/GEMINI_MODEL trong env được kiểm tra; chỉ kiểm tra có/không, không in giá trị secret.

## Ưu tiên tiếp theo trong Codex

1. Khởi tạo repo Git mới và báo đường dẫn thực tế; chỉ git add các file chủ động tạo/copy và đã kiểm tra, không add toàn bộ thư mục cũ.
2. Copy tài liệu, tạo README và cập nhật Evidence Log. Tiếp tục không thêm timestamp cuộc trò chuyện theo yêu cầu; metadata ngày công bố/cutoff của evidence vẫn cần giữ.
3. Thiết lập môi trường khả dụng; bắt đầu code MVP theo kế hoạch đã duyệt, không hỏi lại phê duyệt stack.
4. Hoàn thiện pipeline, UI, rule validators và tests offline. Phân biệt fixture/synthetic/replay với live research.
5. Chỉ làm live Gemini sau khi có quyền dùng key và trần chi phí phù hợp; báo thực trạng nếu còn thiếu.
6. Mission 2 cần GitHub Public + README + demo nếu khả thi + ≥5 actual test cases (tốt/khó/chưa xử lý tốt) + video ≤5 phút + ba Forced Decisions. Không tuyên bố bất kỳ phần nào hoàn thành khi chưa có kết quả thật.

Deadline Mission 2 chính xác chưa được cung cấp; ba ngày tính từ lúc mission mở, không tự suy ra từ ngày hiện tại.
