# Evidence Log Mission 2

Tiếp nối Mission 1 trong `evidence-log.md`. Giữ yêu cầu không có trường timestamp, không khôi phục EL-000. Mỗi quyết định kỹ thuật do AI đề xuất chỉ chuyển thành USER-DECISION khi người dùng xác nhận. Log kỹ thuật của ứng dụng sau này vẫn cần ngày công bố/ngày truy cập/cutoff để kiểm tra bằng chứng; đây là metadata nghiên cứu, khác timestamp của cuộc trò chuyện.

## M2-EL-001 Yêu cầu khởi động Mission 2

**Công cụ/model:** Codex assistant; shell đọc file và trích văn bản PDF; công cụ duyệt web tìm tài liệu kỹ thuật chính thức. Không gọi Gemini bằng API key của người dùng.

**Nguyên văn prompt:**

> Tôi đã vượt qua Mission 1 — Game Market Intelligence của Gamota và đang bắt đầu Mission 2: Hiện thực hóa MVP trong 3 ngày.
>
> Hãy tiếp tục dựa trên các tài liệu Mission 1 và Evidence Log của tôi. Trước tiên, tìm và đọc các tài liệu đó trong workspace hiện tại.
>
> Các quyết định Mission 1 gồm:
>
> - Problem: Sàng lọc cơ hội game bằng nhận định có căn cứ.
> - Người dùng: Publishing/Strategy Lead.
> - Hướng giải quyết: Evidence-centered hybrid.
> - AI tìm nguồn, trích xuất claim và tạo decision brief; con người giữ quyền quyết định cuối.
> - Recommendation: Tiếp tục / Tạm giữ / Dừng.
> - Case nghiên cứu chính: MABINOGI MOBILE.
> - Thiết kế ưu tiên truy xuất bằng chứng, nhận diện bất định và xử lý nguồn mâu thuẫn.
>
> Mission 2 yêu cầu:
>
> 1. MVP hoạt động thực tế.
> 2. Xử lý nhiều hơn một câu hỏi nghiên cứu.
> 3. Kết luận quan trọng có nguồn kiểm chứng.
> 4. Phân biệt chất lượng và độ phù hợp của nguồn.
> 5. Không che giấu sự thiếu dữ liệu hoặc bất định.
> 6. Có tối thiểu 5 test cases với kết quả thực tế, trong đó có tình huống tốt, khó và thất bại.
> 7. Repository GitHub Public, README, demo online nếu khả thi, video tối đa 5 phút và ba Forced Decisions.
>
> Tôi muốn giữ vai trò đưa ra quyết định kỹ thuật, không giao toàn bộ dự án cho AI.
>
> Hãy bắt đầu bằng việc:
>
> - Đối chiếu Mission 1 với yêu cầu Mission 2.
> - Xác định core loop nhỏ nhất cần triển khai.
> - Đề xuất kiến trúc và stack khả thi trong 3 ngày.
> - Thiết kế trước bộ test và tiêu chí đánh giá.
> - Nêu rõ những tính năng sẽ chủ động không làm.
> - Tạo kế hoạch implementation có từng milestone kiểm chứng được.
>
> Tôi không muốn hệ thống chỉ hard-code MABINOGI MOBILE. MVP phải xử lý được nhiều câu hỏi thuộc phạm vi Game Market Intelligence.
>
> Không tự tuyên bố code đã chạy, test đã pass hay sản phẩm đã deploy nếu chưa có kết quả thực tế.
>
>
> Trước khi bắt đầu lập trình, hãy trình bày phương án kỹ thuật và những trade-off quan trọng để tôi xem xét. Sau khi tôi duyệt, tiến hành hiện thực hóa, kiểm thử và hoàn thiện bài nộp., đây là nội dung cụ thể mission 2 nếu bạn cần: đây là nội dung mission 2: Mission 2: Hiện thực hóa BỐI CẢNH BÀI TEST A — NGHIÊN CỨU THỊ TRƯỜNG GAME MÔ TẢ ĐỀ Gamota cần một sản phẩm sử dụng AI để hỗ trợ nghiên cứu thị trường game nhanh hơn, có hệ thống hơn và tạo ra những nhận định có thể sử dụng cho việc ra quyết định.  Thông tin trên Internet rất nhiều nhưng phân tán, khác nhau về độ tin cậy, có thể đã cũ hoặc mâu thuẫn. Thách thức không nằm ở việc tìm thật nhiều thông tin, mà ở khả năng biến thông tin thành nhận định có căn cứ và có thể kiểm chứng.  Ví dụ: “Thể loại game mobile nào có tiềm năng tại Đông Nam Á trong 12 tháng tới?” Đây chỉ là ví dụ, không phải câu hỏi duy nhất sản phẩm cần xử lý.  CÂU HỎI CỐT LÕI Làm thế nào để kết quả nghiên cứu vừa đáng tin cậy, vừa thực sự giúp người dùng đưa ra quyết định?  MISSION 2 — HIỆN THỰC HÓA Xây Prototype/MVP để chứng minh phần quan trọng nhất của giải pháp thực sự hoạt động. Xây dựng Prototype/MVP để chứng minh phần quan trọng nhất trong giải pháp của bạn thực sự hoạt động.  Bạn đã phân tích và thiết kế giải pháp ở Mission 1. Bây giờ hãy lựa chọn phần quan trọng nhất và chứng minh nó bằng một sản phẩm chạy được.  Mission 2 không yêu cầu một sản phẩm hoàn chỉnh. Một MVP nhỏ nhưng chứng minh đúng giả thuyết quan trọng sẽ được đánh giá cao hơn một sản phẩm nhiều tính năng nhưng không giải quyết rõ bài toán.  THỜI GIAN 03 ngày kể từ khi Mission 2 được mở.  KHÔNG CẦN Làm toàn bộ những gì đã nghĩ ở Mission 1. Xây sản phẩm production-ready. Làm giao diện thật đẹp. Cố che giấu lỗi hoặc hạn chế của MVP. CẦN CHỨNG MINH Bạn biết chọn đúng thứ cần làm → biến nó thành sản phẩm → kiểm thử → biết sản phẩm đang tốt và chưa tốt ở đâu.  CORE LOOP MISSION 2 Câu hỏi nghiên cứu → tìm hiểu → sử dụng nguồn thông tin → tạo nhận định có căn cứ → người dùng kiểm chứng được kết quả.  MVP cần chứng minh:  Xử lý được nhiều hơn một câu hỏi mẫu. Kết luận quan trọng có căn cứ. Không coi mọi nguồn có độ tin cậy ngang nhau. Biết thể hiện khi dữ liệu thiếu hoặc không chắc chắn. Có cách kiểm thử chất lượng. BỘ KIỂM THỬ MISSION 2 Tối thiểu 05 tình huống kiểm thử.  Bắt buộc có:  Ít nhất 01 tình huống sản phẩm làm tốt. Ít nhất 01 tình huống khó hoặc dữ liệu không rõ ràng. Ít nhất 01 tình huống sản phẩm chưa xử lý tốt/thất bại. Format:  Kỳ vọng → Kết quả thực tế → Đạt/Chưa đạt → Điều học được  3 CÂU HỎI BẮT BUỘC Phần quan trọng nhất bạn chọn để hiện thực hóa trong MVP là gì? Vì sao nếu phần này hoạt động, bạn tin rằng hướng giải quyết của mình là khả thi? So với kế hoạch ở Mission 1, bạn đã thay đổi quyết định hoặc thiết kế nào? Điều gì trong quá trình làm khiến bạn thay đổi? MVP hiện xử lý chưa tốt nhất ở tình huống nào? Theo bạn nguyên nhân nằm ở đâu và nếu có thêm thời gian bạn sẽ ưu tiên cải thiện điều gì? BÀI NỘP MISSION 2 GitHub Repository Public. Có README. Không chứa API key, mật khẩu hoặc dữ liệu nhạy cảm. Bản chạy thử Ưu tiên link online.  Nếu không thể deploy, phải ghi rõ lý do và hướng dẫn chạy local trong README.  Video trình bày Tối đa 5 phút.  Tập trung vào:  Bài toán → phần chọn để chứng minh → demo → tình huống khó → hạn chế.  Bộ kiểm thử Tối thiểu 05 test cases.  GHI CHÚ Được phép và được khuyến khích sử dụng AI: điều cần đánh giá là khả năng hiểu đúng vấn đề, lựa chọn cách giải quyết hợp lý, biến ý tưởng thành sản phẩm và tiếp tục hoàn thiện khi thực tế thay đổi. Tự do chọn ngôn ngữ, framework, model và nhà cung cấp LLM (OpenAI, Gemini, Claude, model open-source...); khuyến khích dùng free tier, chi phí API tự lo. Nộp bài theo hướng dẫn của HR/Gamota.

**Mục tiêu:** Đối chiếu tài liệu, đề xuất core loop, kiến trúc, trade-off, bộ test và milestone; chờ người dùng duyệt trước implementation.

**Kết quả AI:** Đã soạn `mission2-technical-plan.md`, gồm hai chế độ Research/Screening, pipeline có giới hạn, Claim Ledger có đoạn dẫn, hai trục quality/relevance, conflict, uncertainty và human review. Đề xuất Python/Streamlit/Gemini sau khi người dùng cung cấp nền tảng kỹ thuật; native search được so sánh với Tavily. Thiết kế mười test cases và milestone M0–M5. Toàn bộ thiết kế kỹ thuật mới vẫn là AI-PROPOSAL.

**Nguồn bằng chứng:** Báo cáo PDF Mission 1, Evidence Log EL-001–EL-006, Research Brief/Claim Ledger và prompt hiện tại. Nguồn kỹ thuật gồm tài liệu Google về grounding, structured output, pricing, rate limits, URL context; tài liệu Streamlit về deploy/secrets; tài liệu Tavily Search/Extract. URL đầy đủ tại mục nguồn của kế hoạch kỹ thuật.

**Hành động kiểm chứng:** Đã tìm thấy và đọc tài liệu trong workspace; báo cáo chính được đọc qua văn bản trích từ PDF. Đã kiểm tra tài liệu kỹ thuật chính thức. Chưa xác minh endpoint bằng key của người dùng, quota, model khả dụng, tính đọc được của nguồn thực tế, chi phí, chất lượng kết quả, tài khoản deploy hoặc GitHub. Không dùng các claim thị trường cũ như kết quả kiểm thử Mission 2.

**Quyết định người dùng:** Giữ framing và các nguyên tắc Mission 1; phải xử lý nhiều câu hỏi, không hard-code MABINOGI MOBILE; phải có actual test results; người dùng duyệt phương án trước khi lập trình. Chưa duyệt stack, model hay budget.

**Lý do do người dùng nêu:** Muốn giữ vai trò quyết định kỹ thuật và chứng minh MVP thật sự hoạt động, không giao toàn bộ dự án cho AI.

## M2-EL-002 Thông tin lựa chọn công nghệ

**Công cụ/model:** Codex assistant và công cụ hỏi đáp bất đồng bộ.

**Nguyên văn câu hỏi của AI:**

> Để chốt stack bạn có thể hiểu và tự bảo vệ khi demo: bạn quen Python hay JavaScript/TypeScript hơn, đã có API key dịch vụ nào và muốn giới hạn chi phí thử nghiệm ở mức nào? Chỉ cần tên dịch vụ, không gửi API key.

**Nguyên văn trả lời của người dùng:**

> tôi quen Python hơn và đã có gemini API key

**Mục tiêu:** Điều chỉnh phương án cho phù hợp kỹ năng và tài nguyên sẵn có của người dùng.

**Kết quả AI:** Đề xuất Python + Streamlit + Gemini; thử native search trước để giảm số dịch vụ phải thiết lập. Không yêu cầu người dùng gửi key vào chat.

**Nguồn bằng chứng:** Trả lời trực tiếp của người dùng, USER-PROVIDED. Đây là thông tin về khả năng và key sẵn có, chưa xác minh key hoạt động.

**Hành động kiểm chứng:** Chưa truy cập key, gọi API hoặc kiểm tra tài khoản. Chưa có ngân sách được xác nhận.

**Quyết định người dùng:** Xác nhận quen Python và có Gemini API key. Chưa xác nhận Streamlit, native search, model ID, ngân sách hoặc deploy.

**Lý do do người dùng nêu:** Quen Python hơn; Gemini key đã sẵn có.

## Decision Register Mission 2

| ID | Phân loại | Nội dung | Nguồn |
|---|---|---|---|
| M2-UD-01 | USER-DECISION | Duy trì quyền phê duyệt kỹ thuật; chưa lập trình trước khi duyệt | M2-EL-001 |
| M2-UD-02 | USER-DECISION | Nhiều câu hỏi trong Game Market Intelligence; không hard-code case | M2-EL-001 |
| M2-UD-03 | USER-DECISION | Chỉ ghi code chạy/test pass/deploy khi có bằng chứng thực | M2-EL-001 |
| M2-UP-01 | USER-PROVIDED | Quen Python, có Gemini API key | M2-EL-002 |
| M2-AI-01 | AI-PROPOSAL | Python, Streamlit, Gemini grounding, đọc nguồn riêng và JSON export | Kế hoạch kỹ thuật |
| M2-AI-02 | AI-PROPOSAL | Research/Screening; scope hữu hạn; quality/relevance tách riêng | Kế hoạch kỹ thuật |
| M2-AI-03 | AI-PROPOSAL | Mười test, tối thiểu ba live runs, audit claim và fault injection tách biệt | Kế hoạch kỹ thuật |
| M2-AI-04 | AI-PROPOSAL | M0–M5, model/budget xác nhận trước live run | Kế hoạch kỹ thuật |

## M2-EL-003 Duyệt phương án và chuyển sang Codex

**Công cụ/model:** Codex assistant, kiểm tra môi trường bằng shell và tạo tài liệu bàn giao.

**Nguyên văn các prompt mới của người dùng:**

> tôi xác nhận phương án nhé

> Tôi đang có API Key của nguời khác cho cũng không biết hạn mức như thế nào ?

> bây giờ bạn hãy giúp tôi khởi tạo 1 repo mới và làm với phiên codex mới trên đó, tôi không muốn làm trên work nữa

**Mục tiêu:** Ghi nhận stack đã được duyệt, giới hạn về key/chi phí và yêu cầu chuyển sang repo cùng phiên Codex riêng.

**Kết quả AI:** Đã soạn tài liệu bàn giao `mission2-handoff.md`. Đã kiểm tra env chỉ ở mức có/không; chưa có key Gemini được cấu hình. Đã thử thiết lập môi trường: lỗi cache gốc chỉ đọc; khi dùng cache riêng, tạo được venv nhưng cài dependencies offline thất bại. Chưa có mã ứng dụng hoặc test thực tế.

**Nguồn bằng chứng:** Prompt người dùng, đầu ra kiểm tra môi trường và thông báo lỗi dependency install; handoff ghi đúng các giới hạn này.

**Hành động kiểm chứng:** Xác nhận workspace cũ chưa là Git repository và thư mục `mission2-mvp` chỉ có `.venv`. Chưa gọi Gemini hoặc bật billing. Việc khởi tạo repo/phiên mới chỉ được ghi hoàn thành sau khi công cụ xác nhận.

**Quyết định người dùng:** Duyệt Python + Streamlit + Gemini, tìm nguồn qua Gemini và đọc nội dung riêng; yêu cầu repo và phiên Codex mới thay cho Work. Ngân sách/quota chưa được xác nhận.

**Lý do do người dùng nêu:** Muốn làm trong Codex; API key được người khác cấp và không biết hạn mức.

## Trạng thái thực tế

- Đã thực hiện: đọc tài liệu và tài liệu kỹ thuật; soạn kế hoạch và log Mission 2.
- Chưa thực hiện: implementation, gọi API MVP, test, tạo GitHub repository, deploy, quay video hoặc nộp bài.
- Đã duyệt phương án kỹ thuật; đang chuyển sang repo và phiên Codex mới theo yêu cầu.
- Chưa rõ: budget, model/quota trên tài khoản và thời hạn Mission 2 chính xác.

## M2-EL-004 Repository local và implementation offline

**Công cụ/model:** Codex local, Git, Python/pytest, Streamlit AppTest, trình duyệt local; đọc tài liệu SDK Google chính thức. Không gọi Gemini của người dùng.

**Nguyên văn trả lời mới của người dùng:**

> Đã được phép — tôi sẽ cung cấp giới hạn

> Tôi sẽ đăng nhập trong tab

**Mục tiêu:** Tiếp tục Mission 2 tại repository local riêng theo handoff và stack đã duyệt.

**Kết quả AI:** Tạo Git repo `project/` trên nhánh main vì `.git` ở root phiên chỉ đọc; commit khởi tạo thành công bằng identity Git có sẵn. Copy chọn lọc tám tài liệu vào docs/mission1 và docs/mission2, giữ nguyên bản gốc. Cài dependencies stack thành công sau khi dùng cache riêng và quyền network. Viết schema, reader, Gemini adapter, pipeline, validators, export, replay và UI/review. Live mặc định tắt; không gọi API Gemini. Viết report actual offline, bản thảo Forced Decisions và kịch bản video.

**Nguồn bằng chứng:** Handoff, technical plan, Mission 1 PDF/Word/ledger/log; source code và actual test artifacts. SDK usage đối chiếu với https://github.com/googleapis/python-genai và tài liệu Google/Streamlit trong README.

**Hành động kiểm chứng:** Lần test đầu 30 passed/3 failed (hai đường dẫn UI test và một giả định HTML title). Sau sửa test assumptions: 33 passed. App local mở được tại 127.0.0.1:8501; quote/source quality/relevance hiển thị được. Tám acceptance cases synthetic/fault injection đã chạy; O08 chưa đạt ngữ nghĩa vì quote có thật nhưng claim đảo nghĩa vẫn vượt validator. Test regression O08 PASS chỉ vì tái hiện đúng giới hạn. Không coi các fixture là evidence thị trường hoặc live Gemini.

**Quyết định người dùng:** USER-DECISION: key được phép sử dụng cho MVP; sẽ cung cấp giới hạn. USER-DECISION: sẽ đăng nhập GitHub trong tab. Chưa nhận giới hạn/model/key local hoặc xác nhận đăng nhập hoàn tất. Không tự coi lựa chọn trên là phép dùng API không giới hạn.

**Đề xuất/chi tiết AI:** AI-PROPOSAL: triển khai offline trước, một search call + một extraction call, cap attempts theo browser session và public demo giữ live tắt. Các bản thảo Forced Decisions cần người dùng rà soát. Không thay stack đã duyệt hoặc tự thêm dịch vụ retrieval trả phí.

**Trạng thái mới thay thế phần “Trạng thái thực tế” cũ:** Có implementation và tests offline/local demo. Chưa có live research, reviewer audit, public repo được xác minh, deploy online hoặc video bài nộp cuối. Quota/budget/model và deadline vẫn chưa chốt. Không có timestamp cuộc trò chuyện trong log; ngày publication/access/cutoff trong evidence schemas là metadata nghiên cứu.
