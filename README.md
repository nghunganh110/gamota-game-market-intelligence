# Gamota Game Market Intelligence

MVP Mission 2 cho Publishing/Strategy Lead: câu hỏi → Gemini tìm nguồn → đọc HTML/PDF riêng → Claim Ledger → kiểm tra evidence → brief → người phụ trách review và quyết định.

**MVP hiện tại:** nghiên cứu bằng Gemini tự tìm nguồn hoặc bằng URL nguồn người dùng chọn; câu hỏi đánh giá phải có tiêu chí; reviewer kiểm tra từng claim, viết nhận định cuối với claim đã duyệt, rồi xuất hoặc mở lại run JSON. [Báo cáo kiểm thử hiện tại](docs/mission2/test-report.md) ghi rõ phần đã chạy và phần còn cần kiểm chứng. Chưa có hai lượt live sau bản sửa được người dùng chấp nhận, nên chưa thể tuyên bố đã chứng minh giả thuyết Mission 2.

Trên giao diện: chọn **Nghiên cứu Gemini** → nhập câu hỏi, tiêu chí nếu hỏi “thành công”, tên game/thể loại, thị trường và kỳ → chọn **Gemini tìm nguồn** hoặc **Tôi cung cấp URL nguồn**. Chế độ URL nhận 1–6 đường dẫn bài viết/báo cáo công khai; nếu không đọc được nguồn nào, app không gọi Gemini để trích xuất. Sau khi có kết quả, xem *Nguồn đã thu*, mở từng claim và trang gốc, lưu đánh giá Supported/Unsupported/Unclear, rồi viết *Nhận định cuối* trong phần review. Tải run JSON để mở lại bằng **Mở run đã lưu**; tải brief Markdown để chia sẻ bản nhận định. Các thao tác review không gọi Gemini.

**Trạng thái đã xác nhận:** app chạy local; bộ test hiện tại **72 đạt**; 8 acceptance cases synthetic/fault injection và [T01–T03 với model thật](docs/mission2/live-test-progress.md) đã chạy. Các research runs còn partial và lỗi ngữ nghĩa; chưa có human acceptance end-to-end. Người dùng đã chạy một lượt Gemini trên URL Streamlit online và báo kết quả partial; môi trường kiểm tra không đăng nhập vẫn chuyển tới login nên chưa tự smoke test được app. Chưa có kết quả chi phí tiền tệ. Replay sau sửa không thay thế bằng chứng fresh retrieval.

**Cập nhật UI:** Sau phản hồi người dùng rằng brief T01 thiếu kết luận, màn hình kết quả nay đưa câu trả lời sơ bộ, claim hỗ trợ và bước kiểm chứng lên đầu. Mỗi claim có review supported/unsupported/unclear với tên và lý do; claim bị đánh dấu unsupported hoặc unclear không còn hỗ trợ finding. Export giữ review. Kết luận vẫn là đề xuất AI cho đến khi người dùng review nội dung; lỗi diễn giải ngữ nghĩa chưa được tự động chữa.

**Lượt online Liên Quân Mobile:** người dùng báo subject `MOBA` cho câu hỏi về tên game, kỳ `Q1 2025`, các ô ngày đang hiện 01/10–31/12/2025 (chỉ có hiệu lực nếu chọn nhập ngày thủ công), cutoff 31/12/2025 và strict. Kết quả 2 API calls, 5 claim rejected, 4 findings excluded, 3 nguồn đọc lỗi. UI nay kiểm tra các mâu thuẫn phạm vi trước khi gọi Gemini, tự suy ra ngày đầu/cuối quý từ `Q1–Q4 YYYY` và tóm tắt lý do claim bị loại. [Chi tiết quan sát](docs/mission2/mission2-evidence-log.md).

[Extraction mới trên snapshots](docs/mission2/live-T01-extraction-review.md) đã chạy với 1 API call: 5/6 claim vượt cơ học, xác nhận bản sửa kỳ đo trên output model thật; partial vì một quote ghép không khớp. AI audit vẫn phát hiện kết luận vượt bằng chứng. Đây là replay có model call mới, không phải một lượt tìm nguồn live mới.

[T02 game thứ hai](docs/mission2/live-T02-review.md) đã chạy live: 6/10 claim qua cơ học, partial vì scope và còn lỗi ngữ nghĩa. Xem [tiến độ kiểm chứng](docs/mission2/live-test-progress.md); T03 cũng đã chạy, human acceptance vẫn còn thiếu.

## Chạy local

Môi trường đã kiểm thử: Python 3.13.12, Streamlit 1.65.0, google-genai 1.75.0. Dependencies được khóa trong `requirements.txt`. Đã tạo source checkout sạch và venv mới, cài dependency từ cache rồi chạy **37/37 tests đạt**. Khi sửa các module Python trong lúc phát triển, khởi động lại server nếu Streamlit giữ import cũ.

```sh
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m streamlit run app.py --browser.gatherUsageStats false
```

Mở địa chỉ local mà Streamlit hiển thị. Chọn **Demo offline — synthetic**, chọn tình huống và bấm **Chạy tình huống**. Demo không cần key và không gọi Gemini. Game Alpha/Beta và tất cả số liệu fixture là hư cấu.

```sh
python -m pytest -q
python -m scripts.offline_report
```

Kết quả và kỳ vọng được ghi trong [test report](docs/mission2/test-report.md). Test ngữ nghĩa PASS chỉ chứng minh tái hiện được lỗi sản phẩm, không chứng minh claim đúng.

## Luồng và ranh giới kiểm chứng

- **Research:** câu hỏi dữ kiện/diễn giải, không ép một quyết định cơ hội.
- **Screening:** tách market potential, business accessibility, feasibility; chiều thiếu evidence hoặc conflict trọng yếu → Tạm giữ.
- Mỗi claim giữ source ID, đoạn trích, game, market, period, metric, loại reported/estimate/qualitative/observed và giới hạn.
- Kiểm tra cơ học source/quote/scope/cutoff. `mechanically_checked` không phải `human_verified`; người review kiểm tra ngữ nghĩa và chọn claim đã xác nhận.
- Source quality và relevance là hai trường riêng. Gemini chỉ đề xuất đánh giá; nguồn không có đánh giá đủ vẫn được xử lý bảo thủ.
- Reviewer có thể sửa quality/relevance nguồn, lưu lý do và tính gate lại; review quyết định cũ được giữ trong history. Hard blocker phải được định nghĩa trước trong scope.
- Reviewer có thể override và phải ghi lý do. Dừng cần claim blocker hợp lệ và người review xác nhận. Khuyến nghị AI và quyết định người phụ trách được lưu riêng.
- JSON export gồm snapshot nội dung/hash và metadata; chỉ dùng local/reviewer. Không tự public nội dung nguồn đầy đủ. Markdown export gồm ledger, conflict, unknowns, actions và review.

## Gemini live — mặc định tắt

CLI/app hỗ trợ đọc `.env` riêng trong root project; điền key/model trực tiếp trên máy, không gửi key trong chat. `.env` bị Git bỏ qua; `.env.example` chỉ là mẫu không có credential. Env đã export có ưu tiên hơn file. Xem [hướng dẫn cấu hình](docs/mission2/live-run-guide.md). Bộ test loader literal/không lộ secret nằm trong suite hiện tại.

[T03 thể loại tại Vietnam](docs/mission2/live-T03-review.md) đã chạy bằng .env: partial, 1/5 claim qua cơ học, chỉ đọc được 2/6 nguồn. T01/T02/T03 đã thực thi; vẫn chưa human-accepted. Không có API calls bổ sung ngoài lượt đã được phép. Giới hạn T03 trong .env không phải allowance cho các lần chạy tiếp.

[Hướng dẫn live T01](docs/mission2/live-run-guide.md) có scope, lệnh preflight không gọi API và lệnh chạy một lần để lưu run/brief/mẫu audit. Lần live đầu đã có [báo cáo và AI audit](docs/mission2/live-T01-review.md); lần gọi tiếp theo cần nằm trong giới hạn sử dụng được xác nhận.

Quyền dùng key đã được người dùng xác nhận. Key/model đã được người dùng cấu hình trong `.env` local cho T03; file này không nằm trên GitHub. Giới hạn hai calls cho T03 đã được sử dụng. Không nhập key vào chat, source code hoặc GitHub. Nếu chạy live thêm, xác định giới hạn sử dụng mới và cấu hình riêng trên máy:

| Biến | Ý nghĩa |
|---|---|
| `GEMINI_API_KEY` hoặc `GOOGLE_API_KEY` | Key bí mật; không in/log giá trị |
| `GEMINI_MODEL` | Model do người dùng chọn sau khi kiểm tra khả năng tài khoản |
| `GMI_LIVE_ENABLED=1` | Mở live sau khi quyền và giới hạn được xác nhận |
| `GMI_KEY_AUTHORIZED=1` | Quyền sử dụng key cho MVP |
| `GMI_BUDGET_NOTE` | Giới hạn đã xác nhận, không chứa key |
| `GMI_MAX_CALLS` | Tổng API attempts trong một browser session, 1–3; mặc định 2 |
| `GMI_LIVE_ACCESS_CODE` | Mã riêng ít nhất 12 ký tự để mở Gemini trên UI; không phải API key |

Một run tối đa một search call, sáu nguồn, một extraction call. Không retry API tự động. Search queries bên trong call do model quyết định, không đồng nghĩa với số API attempts. Đọc tối đa 4 MB/30 giây/30k ký tự mỗi nguồn, PDF ≤50 trang. Lưu usage có sẵn; **chưa tính phí tiền tệ**. Session cap không phải quota account hay trần tiền tệ; session mới hoặc process mới có thể reset. UI nay yêu cầu mã truy cập riêng trước khi bật nút live. Để dùng trên Cloud, cấu hình Secrets và hạn mức ở phía nhà cung cấp theo [hướng dẫn Gemini online](docs/mission2/online-gemini-setup.md). Mã truy cập chỉ giới hạn người dùng; nó không tự đặt trần chi phí toàn tài khoản.

SDK integration theo [Google GenAI Python SDK](https://github.com/googleapis/python-genai), [Google Search grounding](https://ai.google.dev/gemini-api/docs/google-search), [structured outputs](https://ai.google.dev/gemini-api/docs/structured-output). Lần T01 đã nhận search grounding và structured extraction bằng cấu hình của người dùng; model ID lưu trong run là cấu hình client, chưa xác minh độc lập danh tính model phía server.

## Hạn chế đã quan sát

- Đảo ngược ý nghĩa claim vẫn có thể vượt quote matching: O08 minh họa. Semantic audit của người dùng vẫn bắt buộc với claim ảnh hưởng quyết định.
- Không có D30 retention: trả gap, không đổi câu hỏi sang doanh thu/rating.
- Run lịch sử strict cần publication date **và snapshot lịch sử**. Reader hiện tại không tự lấy archive, nên tài liệu hiện tại không chứng minh nội dung tồn tại trước cutoff cũ. PDF publication date mặc định unknown, không dùng creation metadata thay thế.
- Không OCR, JS rendering, paywall bypass, dữ liệu nội bộ hay quyền phát hành thực. HTML date extraction là metadata tự động, cần kiểm tra lại.
- Exact duplicate URL/content được đánh dấu; paraphrased repost cần reviewer nhận diện, không hứa tự phát hiện mọi phụ thuộc nguồn.
- URL reader chặn private/reserved addresses trước request/redirect. MVP chưa phải crawler production và chưa có transport chống DNS rebinding; public live retrieval chưa được mở.

## Demo và bài nộp

Repo public: https://github.com/nghunganh110/gamota-game-market-intelligence. Người dùng đã cung cấp URL [Streamlit online](https://gamota-game-market-intelligence.streamlit.app/); kiểm tra không đăng nhập nhận chuyển hướng tới login (`HTTP 303`), nên chưa xác minh được UI hoặc Gemini trên Cloud. Cloud Secrets có thể cấp key/model cho chế độ Gemini sau khi chủ key xác nhận phạm vi sử dụng; UI yêu cầu mã truy cập riêng. Lần chạy online do người dùng báo có hai nguồn đọc lỗi và extraction `ValidationError`; bản sửa giữ record hợp lệ và hiển thị chẩn đoán an toàn đã được push, nhưng cần một lượt smoke test mới để xác nhận trên Cloud. [Checklist deploy](docs/mission2/deploy-checklist.md).

[Technical plan](docs/mission2/mission2-technical-plan.md) giữ nguyên lịch sử đề xuất; [Evidence Log](docs/mission2/mission2-evidence-log.md) ghi xác nhận mới. Báo cáo Mission 1 trong `docs/mission1` chỉ là tài liệu nền. [Ba Forced Decisions](docs/mission2/forced-decisions-draft.md) và [kịch bản video](docs/mission2/video-script.md) là AI-PROPOSAL để người dùng rà soát. Không tự nộp thay người dùng.
