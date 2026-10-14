# Mission 2 Phương án kỹ thuật và kế hoạch kiểm chứng

Trạng thái: AI-PROPOSAL, chờ người dùng duyệt trước khi lập trình. Người dùng xác nhận quen Python và đã có Gemini API key. Chưa xác nhận ngân sách, model cụ thể, nền tảng deploy hoặc stack cuối cùng. Chưa tạo mã ứng dụng, gọi API của MVP, chạy test hay deploy.

## 1 Tài liệu đã đối chiếu

- `Mission_1_Game_Market_Intelligence.pdf`: năm trang nội dung chính, đọc văn bản từ PDF.
- `evidence-log.md`: EL-001 đến EL-006, Decision Register và các unknowns; không khôi phục EL-000 hoặc timestamp đã được yêu cầu bỏ.
- `mabinogi-research-brief-claim-ledger.md`: hai decision tracks và 18 claim làm đầu vào nghiên cứu lịch sử.
- Yêu cầu Mission 2 do người dùng cung cấp trong cuộc trò chuyện.

Kết luận của Mission 1 là điểm xuất phát của thiết kế. Nội dung Claim Ledger cũ không được coi là bằng chứng mới đã được MVP truy xuất và xác minh. Các trang động và số liệu cũ cần được thu thập lại; nếu không có snapshot gốc, không được tuyên bố tái dựng chính xác dữ liệu trước cutoff.

## 2 Điều giữ lại và điều thay đổi

| Nội dung | Mission 1 | Đề xuất cho Mission 2 |
|---|---|---|
| Quyết định kinh doanh | Sàng lọc cơ hội cho Publishing/Strategy Lead | Giữ nguyên |
| Nguyên tắc | Evidence-centered hybrid, con người quyết định cuối | Giữ nguyên, có thao tác review và override |
| Case | MABINOGI MOBILE minh họa workflow | Engine nhận câu hỏi tự do và scope; kiểm thử thêm game và câu hỏi khác |
| Bằng chứng | Ledger do AI và người dùng nghiên cứu | App tự tìm nguồn, đọc tài liệu, lập claim có trích đoạn và metadata |
| Khuyến nghị | Hard gate, evidence gate, đánh giá có cấu trúc | Quy tắc đơn giản trong code; AI đề xuất đánh giá; reviewer xác nhận điểm trọng yếu |
| Dữ liệu thiếu | Hold có mục tiêu | Giữ nguyên; lỗi kỹ thuật được hiển thị riêng |
| Mức chứng minh | Thiết kế và nghiên cứu case | Có run thực, test report, artifact và giới hạn đã quan sát |
| Cutoff | Mốc lịch sử của Mission 1 | Nhập riêng cho từng run; case lịch sử và run hiện tại không trộn dữ liệu |

## 3 Giả thuyết cần chứng minh và phạm vi

Giả thuyết: với nhiều câu hỏi sàng lọc game khác nhau, cùng một pipeline có thể tạo nhận định mà người dùng lần ngược được tới đoạn bằng chứng, nhận ra giới hạn của nguồn và xác định việc cần kiểm chứng tiếp.

Hai chế độ đề xuất:

1. **Research**: xác minh tín hiệu thương mại, diễn giải phản hồi người chơi hoặc phân tích xu hướng trong một scope hữu hạn. Đầu ra trả lời câu hỏi, bằng chứng, mâu thuẫn, unknowns và việc nghiên cứu tiếp. Không bắt câu hỏi dữ kiện phải có quyết định Dừng cơ hội.
2. **Screening**: nghiên cứu nhằm phân bổ nguồn lực cho một cơ hội cụ thể. Bổ sung hai track market potential và business accessibility, cùng Tiếp tục/Tạm giữ/Dừng.

Input gồm câu hỏi, game hoặc thể loại, thị trường, khoảng thời gian/cutoff và mục đích nghiên cứu. Chấp nhận câu hỏi tự do trong phạm vi game mobile; nếu quá rộng, giao diện yêu cầu thu hẹp và hiển thị giới hạn. MABINOGI MOBILE chỉ xuất hiện trong ví dụ và fixtures, không nằm trong logic điều kiện hoặc prompt cố định.

## 4 Core loop nhỏ nhất

**Câu hỏi và scope → tìm nguồn → đọc nội dung → trích claim → kiểm tra bằng chứng và đối chiếu → decision brief → người dùng kiểm tra và quyết định.**

Đề xuất giới hạn ban đầu: tối đa hai vòng tìm kiếm và sáu tài liệu được đọc cho một run. Giới hạn độ dài tài liệu, thời gian chờ và số lần retry. Số truy vấn tìm kiếm bên trong một lần gọi Gemini do model quyết định, cần ghi nhận nếu API cung cấp; không giả định một prompt tương ứng một truy vấn hoặc một mức phí cố định.

Quy trình thực hiện:

1. Gemini tìm nguồn theo câu hỏi và scope. Lưu URL và attribution từ API; câu trả lời tìm kiếm chỉ phục vụ phát hiện nguồn.
2. Ứng dụng đọc HTML hoặc PDF có text. Nguồn đọc thất bại, paywall, scan hay thiếu ngày được ghi rõ; không lấy search snippet thay cho full-text mà vẫn gắn verified.
3. Gemini trích JSON theo schema, gồm claim, loại dữ kiện, source ID, đoạn dẫn, thị trường và kỳ đo. Lưu bản nội dung đã đọc cùng hash trong artifact local; public repo chỉ đưa trích đoạn cần thiết và metadata phù hợp quyền sử dụng.
4. Code kiểm tra ID tồn tại, đoạn dẫn có trong nội dung, cutoff và scope. Trùng URL và bài đăng lại được đánh dấu; không tính là nhiều bằng chứng độc lập.
5. Gemini đề xuất quan hệ giữa các claim: cùng hỗ trợ, xung đột thực, khác scope/thời kỳ, hoặc chưa đủ cơ sở. Conflict Card giữ cả hai phía và bước phân xử.
6. Code kiểm tra brief chỉ dùng claim hợp lệ; inference phải chỉ ra claim đầu vào. Hiển thị recommendation, coverage, unknowns và lỗi thu thập riêng.
7. Reviewer mở claim trọng yếu, chấp nhận hoặc override đề xuất và nhập lý do; có nút tải run JSON/brief Markdown.

Đoạn dẫn có thật chỉ chứng minh khả năng truy vết. Việc claim diễn giải đúng đoạn dẫn vẫn cần đánh giá ngữ nghĩa và người dùng kiểm tra ở các claim ảnh hưởng quyết định. Trạng thái mặc định là AI-extracted hoặc mechanically-checked, không tự đổi thành human-verified.

## 5 Kiến trúc và stack đề xuất

Một ứng dụng Python duy nhất: Streamlit cho giao diện, các module xử lý riêng cho tìm nguồn, đọc tài liệu, claim, kiểm tra và recommendation. Không cần dịch vụ frontend/backend riêng.

| Thành phần | Lựa chọn đề xuất | Lý do và giới hạn |
|---|---|---|
| Giao diện | Streamlit | Ít việc thiết lập, hợp Python; hạn chế tùy biến và không xây dashboard production |
| Tìm nguồn | Gemini với Google Search grounding | Tận dụng key sẵn có; phụ thuộc attribution và quyền truy cập tool của tài khoản |
| Đọc tài liệu | httpx, trafilatura cho HTML; pypdf cho PDF có text | Có nội dung kiểm tra được; JS-only, paywall và scan là giới hạn thực tế |
| Trích xuất và tổng hợp | Gemini, Google GenAI SDK, JSON schema | Đầu ra có cấu trúc; model ID chọn sau smoke test trên tài khoản |
| Kiểm tra dữ liệu | Pydantic và quy tắc Python | Tách lỗi schema/citation khỏi suy luận mô hình |
| Lưu run | JSON và tải xuống; session state cho UI | Không thêm database; không hứa lưu bền trên cloud |
| Kiểm thử | pytest, fixture replay, live runs và audit thủ công | Tách regression lặp lại được khỏi chất lượng tìm kiếm hiện tại |
| Deploy | Ưu tiên Streamlit Community Cloud | Phụ thuộc tài khoản/GitHub và smoke test trên máy chủ; local fallback có hướng dẫn |

Các phương án cần người dùng chọn:

| Quyết định | Phương án ưu tiên | Phương án thay thế và trade-off |
|---|---|---|
| UI | Python + Streamlit | FastAPI + frontend riêng: linh hoạt hơn, nhiều công triển khai và test hơn trong ba ngày |
| Search | Gemini grounding + đọc nguồn riêng | Tavily Search/Extract + Gemini: kiểm soát retrieval rõ hơn, cần thêm key và ngân sách |
| Quy trình | Pipeline cố định có giới hạn | Agent tự lặp tìm kiếm: linh hoạt nhưng khó giới hạn thời gian, chi phí và tái hiện lỗi |
| Lưu trữ | JSON export | SQLite hoặc database hosted: có lịch sử nhưng thêm vận hành; chỉ thêm nếu nhu cầu kiểm thử đòi hỏi |

Tách bước tìm kiếm khỏi bước trích JSON dù API/model có thể hỗ trợ kết hợp: thêm một bước xử lý nhưng dễ quan sát nguồn và debug. Nếu spike cho thấy URL của grounding không đọc được đủ tốt, báo kết quả cụ thể rồi xin người dùng chọn retrieval thay thế, không âm thầm bỏ yêu cầu bằng chứng.

M0 chưa chốt model ID hay chi phí. Trước live run, kiểm tra model có trong tài khoản, tool search, schema và quota; lưu phiên bản SDK/model đã dùng. API key cấu hình ở máy hoặc cloud secrets, không dán trong chat hay commit GitHub. Public demo cần giới hạn lượt chạy/chi phí và quyền truy cập live; replay được gắn nhãn rõ. Replay không thay thế yêu cầu live research.

## 6 Chất lượng nguồn khác độ phù hợp của nguồn

Không dùng một điểm tin cậy duy nhất. Mỗi nguồn có hai nhóm trường và lời giải thích:

- **Chất lượng:** ai phát hành, nguồn gốc hay đăng lại, phương pháp có rõ không, có xung đột lợi ích gì, nội dung có đọc được không.
- **Độ phù hợp:** đúng game/thể loại, thị trường, thời kỳ, chỉ số và câu hỏi hay không; trực tiếp, gián tiếp hoặc không phù hợp.

Ví dụ: báo cáo Nexon đáng dùng để xác minh Nexon công bố gì về Hàn Quốc nhưng không tự chứng minh nhu cầu tại Việt Nam. Review trực tiếp từ người chơi phù hợp để tìm loại vấn đề trải nghiệm, song một mẫu tự chọn không đại diện cho toàn bộ người chơi. Ước tính của bên thứ ba giữ nhãn estimate và coverage.

Thông tin nguồn do AI gán là đánh giá có lý do, cho phép reviewer sửa. Không đồng nhất domain uy tín, thứ hạng tìm kiếm hay số citation với độ đúng của claim.

## 7 Recommendation và bất định

Tách `run_status` như completed, partial, failed khỏi `recommendation` Tiếp tục/Tạm giữ/Dừng. Một lần gọi API thất bại không chứng minh opportunity kém.

Với screening, market potential, business accessibility và feasibility được đánh giá riêng theo evidence requirements mà người dùng nhìn thấy. Mỗi chiều có supported, concern hoặc unknown, kèm claim ID. Không đếm URL để quyết định đủ bằng chứng.

- Tiếp tục khi các chiều bắt buộc có bằng chứng phù hợp hỗ trợ luận điểm cơ hội và không có blocker hoặc mâu thuẫn trọng yếu chưa xử lý.
- Tạm giữ khi có evidence gap hoặc mâu thuẫn có thể đảo chiều. Mỗi gap phải có tác động, cách tìm, người review và điểm đánh giá lại.
- Dừng khi blocker đủ bằng chứng và được reviewer xác nhận. Nhánh tín hiệu tiêu cực hội tụ trong Mission 1 được giữ ở dạng đề nghị người phụ trách review trước khi Dừng, để MVP tránh tự kết luận loại bỏ trên rubric chưa được hiệu chỉnh.

Nếu không có nguồn đọc được, app báo nghiên cứu chưa đủ cơ sở hoặc lỗi thu thập; không sinh narrative có vẻ hoàn chỉnh. Thiếu ngày công bố là unknown; trong run cutoff nghiêm ngặt, nguồn đó không được dùng để quyết định nếu chưa có bằng chứng khác về thời điểm. Trang động không có snapshot lịch sử không được coi là nội dung chắc chắn tồn tại trước cutoff.

## 8 Bộ kiểm thử thiết kế trước

Tất cả kết quả thực tế hiện tại: **CHƯA CHẠY**. Đây là expected behavior, không phải test đã pass. Bộ tối thiểu gồm ít nhất ba live runs với hai game khác nhau và một câu hỏi ngoài case MABINOGI, cộng fixture tests cho các tình huống khó tái hiện.

| ID | Câu hỏi hoặc tình huống | Loại | Kỳ vọng |
|---|---|---|---|
| T01 | MABINOGI MOBILE có bằng chứng gì về launch strength tại Hàn Quốc, trong kỳ được chọn? | Live, ứng viên case tốt | Claim quan trọng có nội dung nguồn; phân biệt estimate và company-reported; không suy ra Vietnam fit |
| T02 | Dungeon&Fighter Mobile có tín hiệu thương mại nào tại Trung Quốc, và các tín hiệu đó có giới hạn gì khi áp dụng sang Việt Nam? | Live, game khác | Pipeline tìm nguồn theo input; tách country/time/metric; ghi unknown về transferability |
| T03 | Bằng chứng công khai nào hỗ trợ nhận định MMORPG mobile có cơ hội ở Việt Nam trong kỳ được chọn? | Live, thể loại | Dùng dữ liệu đúng thị trường; tách spending/download; không dự báo tăng trưởng chắc chắn khi thiếu dữ liệu |
| T04 | Doanh thu launch mạnh và rating thấp có thực sự mâu thuẫn? | Replay từ nguồn đã thu thập | Tách outcome, platform, time và population; không quy toàn bộ rating thấp cho gameplay |
| T05 | Hai tài liệu nói khác nhau về cùng metric, market và period | Fixture gắn nhãn synthetic nếu tự tạo | Conflict Card giữ hai phía; chưa phân xử thì không đưa kết luận dứt khoát |
| T06 | Có thể khẳng định Gamota có quyền phát hành MABINOGI MOBILE tại Việt Nam không? | Live, dữ liệu có thể thiếu | Không tìm thấy xác nhận không đồng nghĩa bị từ chối; unknown/targeted validation |
| T07 | Nguồn uy tín sai thị trường; bài đăng lại; nguồn thiếu ngày hoặc sau cutoff | Fixture | Tách quality/relevance, tránh đếm độc lập giả và loại khỏi evidence gate khi không hợp cutoff |
| T08 | API 429, timeout hoặc toàn bộ tài liệu không đọc được | Fault injection | Báo failed/partial và giới hạn thực; không tạo claim hay recommendation giả |
| T09 | Yêu cầu D30 retention theo quốc gia để so hiệu quả dài hạn, nhưng dữ liệu không công khai | Live challenge, ứng viên chưa đáp ứng | Ghi rõ không hoàn thành câu hỏi do thiếu dữ liệu; không thay bằng doanh thu hoặc rating |
| T10 | Nội dung nguồn chứa chỉ dẫn bỏ qua quy tắc; claim trích sai đoạn hoặc sinh source ID mới | Fixture | Nguồn chỉ là dữ liệu; validator chặn ID/quote giả; ghi thất bại nếu bị vượt qua |

Expected behavior sẽ được đóng băng trước run. Với T01–T03, không ấn định một kết luận kinh doanh hoặc ép status trước khi thấy dữ liệu. T04/T05 chỉ gắn nhãn conflict theo nội dung đã duyệt; không dựng mâu thuẫn giữa các nguồn thật nếu không có.

Mỗi test report có: Kỳ vọng → Kết quả thực tế → Đạt/Chưa đạt → Điều học được, cùng run ID, evidence artifact và chế độ live/replay/synthetic. Nếu sửa lỗi, giữ kết quả trước và sau sửa.

Một fault-injection test xử lý lỗi đúng có thể PASS về kỹ thuật, nhưng không tự đáp ứng yêu cầu case sản phẩm thất bại. T09 có thể là thất bại về mức đáp ứng câu hỏi nhưng đúng về an toàn bằng chứng; báo cả hai chiều. Case chưa xử lý tốt cho bài nộp chỉ được chốt sau khi quan sát run thật. Nếu chưa quan sát được case phù hợp, ghi yêu cầu này chưa hoàn tất, không tạo kết quả giả.

## 9 Tiêu chí đánh giá

| Tiêu chí | Cách đo và điều kiện chấp nhận đề xuất |
|---|---|
| Nhiều câu hỏi | Ít nhất ba live runs theo T01–T03, bao gồm hai game và một câu hỏi thể loại; input không được hard-code |
| Truy vết | Mọi factual claim ảnh hưởng kết luận trỏ về source đã đọc và đoạn dẫn tồn tại; inference có claim đầu vào |
| Claim được nguồn hỗ trợ | Người dùng audit toàn bộ decision-driving claims trong brief; chỉ đúng URL chưa đủ. Lỗi làm đổi kết luận phải sửa trước khi gọi brief đạt |
| Quality và relevance | T07 phải tách hai trục và giải thích; nguồn uy tín sai thị trường không vượt evidence gate |
| Bất định và conflict | T04–T09 nêu đúng giới hạn; unknown không bị biến thành blocker, API error không bị biến thành Stop |
| Tái hiện | Cùng structured evidence và gate tạo cùng status bằng code; rerun toàn bộ LLM không được hứa deterministic |
| Hữu ích | Người dùng xác định được kết luận, claim hỗ trợ, điểm chưa biết và next action trong một buổi review thực; ghi rõ reviewer là người tham gia nếu không có Lead thực tế |
| Hiệu năng và chi phí | Ghi latency, số lần gọi, token/search usage có sẵn; ghi unavailable khi thiếu metadata. Chốt trần chi phí trước live run; không tuyên bố tiết kiệm thời gian khi chưa có baseline tương đương |
| Bài nộp | Repo public, fresh local run theo README, link demo nếu deploy thực thành công, ≥5 test có actual result, video ≤5 phút, ba Forced Decisions dựa trên quá trình thật |

## 10 Các tính năng chủ động không làm

- Dự báo doanh thu hoặc xác suất game thành công, xếp hạng nhiều game bằng trọng số chưa hiệu chỉnh.
- Agent nhiều tầng, tự lặp vô hạn, vector database, RAG corpus lớn hoặc fine-tuning.
- Dashboard toàn thị trường Đông Nam Á, giám sát liên tục hoặc crawling hàng loạt.
- OCR/PDF scan, truy cập paywall, mạng xã hội cần đăng nhập, scraping review quy mô lớn.
- Kết nối dữ liệu nội bộ hoặc thực hiện đàm phán quyền phát hành.
- Multi-user accounts, history service hay hệ thống phân quyền production.
- Xuất DOCX/PDF trong app trước khi core loop và test đạt; ưu tiên JSON/Markdown có thể kiểm tra.

## 11 Milestone trong ba ngày

Ngày 1–3 là tương đối từ lúc bắt đầu implementation sau duyệt; thời điểm Mission 2 mở và deadline chính xác chưa được cung cấp.

| Mốc | Thời điểm | Artifact và cách xác nhận | Nếu chưa đạt |
|---|---|---|---|
| M0 | Trước lập trình | Người dùng duyệt scope, stack, retrieval và budget; ghi USER-DECISION | Chỉ hoàn thiện design, chưa gọi API hay triển khai |
| M1 | Hai giờ đầu Day 1 | Spike Gemini search, đọc URL/PDF, schema; hai câu hỏi khác nhau có evidence artifact | Chỉ rõ khâu hỏng; quyết định thu hẹp loại nguồn hoặc đổi retrieval với người dùng |
| M2 | Cuối Day 1 | Một live question đi hết từ input đến brief và citation mở được; lưu run JSON | Sửa core trước khi thêm conflict/replay/deploy |
| M3 | Cuối Day 2 | Claim validation, quality/relevance, conflict, unknowns, gates và override hoạt động; có T01–T03 thực | Cắt UI/export phụ; bảo vệ bằng chứng và đa câu hỏi |
| M4 | Đầu Day 3 | Tối thiểu năm actual test results, có tốt/khó/chưa đáp ứng; giữ failure artifacts | Báo gap, sửa lỗi ảnh hưởng kết luận; không che log |
| M5 | Cuối Day 3 | Repo public đã kiểm tra secrets; README chạy từ môi trường sạch; smoke test demo/local; video và Forced Decisions | Nếu deploy không khả thi, ghi nguyên nhân đã quan sát và hướng dẫn local |

Gói bài nộp dự kiến: mã nguồn, README, test-report, nguồn/fixtures phù hợp quyền sử dụng, decision-log, hướng dẫn demo, ba Forced Decisions và video. Không khởi tạo hay public repository trước khi người dùng duyệt phương án.

Video gợi ý 4 phút 50 giây: 30 giây bài toán; 40 giây phần chọn hiện thực hóa; 120 giây live demo hai câu hỏi và citation; 70 giây case khó/thất bại; 30 giây hạn chế và ưu tiên tiếp theo. Ba Forced Decisions chỉ được hoàn thiện sau khi có thay đổi thực và hạn chế quan sát được.

## 12 Nguồn kỹ thuật đã đọc

Các tài liệu dưới đây xác nhận khả năng API/framework, không xác nhận app đã hoạt động trên tài khoản người dùng.

- Gemini Google Search grounding: https://ai.google.dev/gemini-api/docs/google-search — có công cụ search và attribution/citations, thông tin mô hình hỗ trợ và cách tính search usage.
- Gemini structured output: https://ai.google.dev/gemini-api/docs/structured-output — hỗ trợ schema; giá trị vẫn cần ứng dụng kiểm tra.
- Gemini pricing: https://ai.google.dev/gemini-api/docs/pricing — phải kiểm tra đúng model/tier; không cam kết free hoặc suy ra quota từ việc có key.
- Gemini rate limits: https://ai.google.dev/gemini-api/docs/rate-limits — quota tài khoản cần xác nhận khi spike.
- Gemini URL context: https://ai.google.dev/gemini-api/docs/url-context — phương án đọc URL bổ sung, chưa chọn làm mặc định thay snapshot có thể kiểm tra.
- Streamlit deploy: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app — hướng dẫn triển khai, chưa có link app.
- Streamlit secrets: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management — lưu secrets ngoài repository.
- Tavily Search: https://docs.tavily.com/documentation/api-reference/endpoint/search và Extract: https://docs.tavily.com/documentation/api-reference/endpoint/extract — phương án retrieval thay thế chưa được chọn.
