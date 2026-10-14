# Gamota Game Market Intelligence

MVP Mission 2 cho Publishing/Strategy Lead: câu hỏi → Gemini tìm nguồn → đọc HTML/PDF riêng → Claim Ledger → kiểm tra evidence → brief → người phụ trách review và quyết định.

**Trạng thái đã xác nhận:** app chạy local; 37 kiểm thử offline đạt; 8 actual acceptance cases synthetic/fault injection đã chạy, gồm một giới hạn ngữ nghĩa chưa đạt. **Chưa có Gemini live research, audit của Lead, deploy online hoặc kết quả chi phí.** Replay không thay thế bằng chứng live.

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

Quyền dùng key đã được người dùng xác nhận; **giới hạn chi phí/lượt gọi, model và key local vẫn chưa được cấu hình**. Không nhập key vào chat, source code hoặc GitHub. Đặt các biến môi trường riêng trên máy sau khi có giới hạn được xác nhận:

| Biến | Ý nghĩa |
|---|---|
| `GEMINI_API_KEY` hoặc `GOOGLE_API_KEY` | Key bí mật; không in/log giá trị |
| `GEMINI_MODEL` | Model do người dùng chọn sau khi kiểm tra khả năng tài khoản |
| `GMI_LIVE_ENABLED=1` | Mở live sau khi quyền và giới hạn được xác nhận |
| `GMI_KEY_AUTHORIZED=1` | Quyền sử dụng key cho MVP |
| `GMI_BUDGET_NOTE` | Giới hạn đã xác nhận, không chứa key |
| `GMI_MAX_CALLS` | Tổng API attempts trong một browser session, 1–3; mặc định 2 |

Một run tối đa một search call, sáu nguồn, một extraction call. Không retry API tự động. Search queries bên trong call do model quyết định, không đồng nghĩa với số API attempts. Đọc tối đa 4 MB/30 giây/30k ký tự mỗi nguồn, PDF ≤50 trang. Lưu usage có sẵn; **chưa tính phí tiền tệ**. Session cap không phải quota account hay trần tiền tệ; session mới hoặc process mới có thể reset. Public demo phải giữ live tắt đến khi có cơ chế hạn mức toàn hệ thống được duyệt.

SDK integration theo [Google GenAI Python SDK](https://github.com/googleapis/python-genai), [Google Search grounding](https://ai.google.dev/gemini-api/docs/google-search), [structured outputs](https://ai.google.dev/gemini-api/docs/structured-output). Hiện kiểm tra SDK bằng mocked response, chưa xác minh server/model/schema bằng key thật.

## Hạn chế đã quan sát

- Đảo ngược ý nghĩa claim vẫn có thể vượt quote matching: O08 minh họa. Semantic audit của người dùng vẫn bắt buộc với claim ảnh hưởng quyết định.
- Không có D30 retention: trả gap, không đổi câu hỏi sang doanh thu/rating.
- Run lịch sử strict cần publication date **và snapshot lịch sử**. Reader hiện tại không tự lấy archive, nên tài liệu hiện tại không chứng minh nội dung tồn tại trước cutoff cũ. PDF publication date mặc định unknown, không dùng creation metadata thay thế.
- Không OCR, JS rendering, paywall bypass, dữ liệu nội bộ hay quyền phát hành thực. HTML date extraction là metadata tự động, cần kiểm tra lại.
- Exact duplicate URL/content được đánh dấu; paraphrased repost cần reviewer nhận diện, không hứa tự phát hiện mọi phụ thuộc nguồn.
- URL reader chặn private/reserved addresses trước request/redirect. MVP chưa phải crawler production và chưa có transport chống DNS rebinding; public live retrieval chưa được mở.

## Demo và bài nộp

Repo public: https://github.com/nghunganh110/gamota-game-market-intelligence. Demo local đã chạy; người dùng chọn **giữ demo local trước** khi Streamlit yêu cầu cấp quyền GitHub. Chưa cấp quyền/deploy online. Khi người dùng muốn tiếp tục, deploy cần đăng nhập nền tảng và smoke test. Trên Streamlit Community Cloud, chọn `app.py`, Python 3.13 và `requirements.txt`; demo public ban đầu chỉ replay, không đặt live key. Chưa có URL deployment được xác minh.

[Technical plan](docs/mission2/mission2-technical-plan.md) giữ nguyên lịch sử đề xuất; [Evidence Log](docs/mission2/mission2-evidence-log.md) ghi xác nhận mới. Báo cáo Mission 1 trong `docs/mission1` chỉ là tài liệu nền. [Ba Forced Decisions](docs/mission2/forced-decisions-draft.md) và [kịch bản video](docs/mission2/video-script.md) là AI-PROPOSAL để người dùng rà soát. Không tự nộp thay người dùng.
