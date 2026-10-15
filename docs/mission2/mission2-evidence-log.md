# Evidence Log Mission 2

## Giao diện kết luận và deploy

**Người dùng hỏi:** `oke nhung toi thay hinh nhu web hien tai chua duoc deploy ?`. Xác minh README/remote: repo đã public nhưng chưa có URL Streamlit online; lựa chọn trước đó là giữ local khi Streamlit xin kết nối GitHub. Tài liệu Streamlit chính thức xác nhận deploy Community Cloud cần repository + entrypoint và kết nối tài khoản GitHub. Không có browser surface khả dụng trong phiên hiện tại; IAB báo unavailable. Chưa deploy hoặc xác minh URL online.

**Cải tiến UI sau phản hồi thiếu kết luận:** Đưa câu trả lời sơ bộ, claim hỗ trợ và bước kiểm chứng lên đầu. Review từng claim có supported/unsupported/unclear, tên và lý do; findings phụ thuộc claim bị đánh dấu unsupported/unclear bị loại khỏi brief và UI; review cuối sau thay đổi được lưu history. Export Markdown ghi verdict. Regression UI dùng O08: review unsupported chặn finding đảo nghĩa. 56 tests passed, không gọi Gemini. Chưa khẳng định reviewer đã chấp nhận UI mới hoặc lỗi semantic được tự động phát hiện.

## Phản hồi người dùng: brief T01 thiếu kết luận

**Nguyên văn:** `toi da doc xong brief T01 va toi chua thay co ket luan gi duoc dua ra`.

**Đánh giá:** Phản hồi thực tế về tính hữu ích: brief được đọc nhưng người dùng chưa nhận ra kết luận. Chưa đạt tiêu chí giúp ra quyết định; không ghi thành human verification hoặc user acceptance.

**Sửa tài liệu:** Đưa câu trả lời trực tiếp lên đầu: evidence hỗ trợ launch strength tại Korea tháng 3–5, viện dẫn rank và analytics claims; giới hạn June/long-term/Vietnam rõ. Thêm hàm ý Tạm giữ — targeted validation và điều kiện chuyển trạng thái theo logic đã thống nhất. Đề xuất này vẫn AI-PROPOSAL, không gán thành quyết định mới của người dùng. Giữ artifact trước đó; không sửa hoặc gọi model. Bản sửa văn bản thủ công chưa chứng minh app tự sinh được kết luận hữu ích. Đây là product usability failure cần đưa vào Forced Decisions/đánh giá MVP.

## T03 tự chạy với .env private

**Người dùng xác nhận:** `da cau hinh xong`. Preflight đủ cấu hình; không in key hoặc đọc .env ra output.

**Thực thi:** CLI T03 trong sandbox failed ConnectError sau 1 local attempt reservation, không response metadata, artifact `runs/36aaf481-49d5-4082-9cf5-43495c3191b9/`. Yêu cầu escalation nêu rõ chạy lại ngoài sandbox với tối đa 2 attempts mới; được phép thực thi. Run ngoài sandbox `runs/e747a968-3a3a-4b62-b152-0d8e4d85f895/`: partial, 2 calls, 5 claims, 56.477 giây. Không automatic SDK retry; không gọi thêm sau lượt này.

**Audit:** 2/6 nguồn đọc được, 1/5 claim mechanically checked, 4 rejected subject/relevance; một finding định tính còn lại, không dimensions/recommendation. AI review nhận định phải giữ joint genres, attribution Gamota summary và giới hạn số riêng MMORPG; legal text gán nhầm period, VNG portfolio không tương đương genre, C5 có chi tiết ngoài quote. Không human_verified, không tính pipeline status là chất lượng đạt. Ghi báo cáo `live-T03-review.md` và cập nhật test progress.

**Quyền/chi phí:** Lượt kết nối lỗi vẫn ghi riêng, không khẳng định server không nhận hoặc phí bằng 0. Tổng artifacts hiện có 10 local reservations, 9 có response metadata; chi phí tiền tệ unknown. .env vẫn gitignored. Không chạy test suite lại vì không đổi code; 53 passed là kết quả kiểm thử loader trước đó.

## Cấu hình .env để Codex tự chạy

**Yêu cầu người dùng:** Muốn đặt API key/model trong .env để Codex tự chạy thay vì chạy lệnh qua Terminal riêng.

**Thực hiện:** Thêm loader literal cho các biến key/model/policy đã có, không shell execution/interpolation; process env ưu tiên. CLI và app đọc root .env. Tạo .env private mode 600 bằng exclusive-create, key/model trống; không ghi đè file đã tồn tại. Thêm .env.example không secret. Xác nhận `git check-ignore .env` đúng; không in giá trị key. Mẫu giới hạn một T03 run tối đa 2 API attempts/no retry, không cấp quyền chạy vô hạn. 53 tests passed, gồm loader không ghi đè env, không thực thi chuỗi lệnh, lỗi không chứa secret và parse lỗi không ghi env một phần. Chưa gọi Gemini, chờ người dùng điền cấu hình riêng.

## T02 live: game thứ hai và giới hạn scope/semantic

**Người dùng gửi:** Artifact `runs/a4f15d87-1b8f-41c5-9f01-dbb048483c95`, live, partial, 2 calls, 10 claims, human audit pending.

**Đã kiểm tra:** 5 nguồn PDF/HTML gồm corporate Nexon/Tencent và journalism; 4 search queries báo, 83.657 giây; 6/10 claims mechanically checked, 4 rejected vì Q2 gồm tháng 4 hoặc tới July. 4 findings bị loại do dependency, 1 còn lại. Không quote mismatch; Research dimensions rỗng. AI audit trên snapshots phát hiện composite claim vượt period, attribution thứ cấp, gross/net/tax overinterpretation, proposed “zero evidence” về rights quá rộng và revisit dates quá khứ. Ghi `live-T02-review.md`, giữ artifact nguyên vẹn.

**Hành động:** Cập nhật bảng tiến độ, tổng 7 model attempts đã quan sát (3 full live runs + 1 snapshot extraction). Chưa human-accepted research case; không tính gate chặn dependency là semantic safety. Chuẩn bị chuyển T03, không lặp T02 để chọn output thuận lợi. Không đổi code, không gọi API hoặc đọc secret mới trong phiên audit; suite 50 tests là kết quả trước, không tuyên bố rerun.

## T01 extraction trên snapshots: xác nhận period gate, giữ lỗi ngữ nghĩa

**Người dùng gửi:** Artifact `runs/c58b7de4-34ca-4903-933d-90af85908e4b`, partial, replay, 1 API call, 6 claims, human audit pending.

**Kiểm chứng:** Đọc run và proposed extraction: 3 snapshots nguồn cũ, 16.279 giây, 8,245 total tokens theo usage. 5/6 claims mechanically checked; C3 rejected do quote nối hai đoạn bằng ellipsis; 1 finding phụ thuộc bị loại. Không có period mismatch, dimensions/blockers rỗng. AI audit phát hiện causal inference PC và official attribution quá mức còn tồn tại; bounds ngày 16/5 suy ra từ khoảng 50 ngày không phải ngày chốt có chứng cứ. Ghi `live-T01-extraction-review.md`. Giữ nguyên artifact và human audit pending.

**Hành động tiếp:** Không sửa validator để nhận quote ghép; không chạy lặp T01 để chọn output thuận lợi. Chuẩn bị chuyển T02 theo test plan game khác, tối đa hai attempts nếu người dùng thực hiện trong giới hạn sử dụng. Không Gemini call mới trong phiên đọc/audit này. Không thay đổi code; suite 50 passed từ lần sửa trước, không tuyên bố chạy lại tests ở phiên chỉ cập nhật báo cáo.

## T01 live lần 2: 0 claims và chẩn đoán retrieval

**Người dùng cung cấp:** Kết quả CLI và artifact `runs/66f919b8-382a-4ded-a777-5f021a3dd3c6`, partial, 2 API calls, 0 claims.

**Đã kiểm tra:** Artifact ghi 1 search query về release date, 1 nguồn Nexon chỉ 692 ký tự navigation, extraction trả gaps và không bịa claim, 45.726 giây, errors rỗng. Đây không phải exception/schema failure; chưa có claim để chứng minh bản sửa kỳ đo. Lưu báo cáo `live-T01-rerun-review.md`, không sửa run gốc.

**Thay đổi và bằng chứng:** Search prompt tập trung metric/period/article; reader bỏ backup extraction, favor precision. Thêm chế độ diagnostic --sources-from dùng snapshots cùng câu hỏi, loại unsuitable và exact duplicates, gọi extraction một lần, evidence_mode=replay và parent hash. 50 tests passed, gồm navigation fixture và snapshot provenance/filter. Chưa live-validate prompt/reader sửa; không tự tuyên bố đã giải quyết retrieval thật.

**Giới hạn:** Phiên Codex không có key từ Terminal của người dùng; không gọi Gemini mới. Chuẩn bị lệnh snapshot extraction, chưa chạy. Cần giới hạn sử dụng phù hợp cho attempt tiếp theo; không tự lặp full discovery. Không gán AI audit thành human verification.

## Tiếp tục sau AI audit T01

**Yêu cầu người dùng:** `lam buoc tiep theo di`. Tiếp tục sửa brief và chuẩn bị kiểm chứng bản sửa; không coi đây là xác nhận ngữ nghĩa từng claim.

**Kết quả:** Tạo `live-T01-corrected-brief.md` bằng tiếng Việt và derivative có cấu trúc tại `runs/9e512f9c-3771-472a-9cba-3e1a5a87ae10/ai-corrected/`. Giữ quote gốc, thu hẹp claim/limitations theo evidence, bỏ causal inference PC, bỏ Screening dimensions trong Research, thay owner/deadline tự gán bằng mặc định cần review. Derivative labeled replay, 5 mechanically checked claims, 2 findings; human review pending; run cha giữ nguyên, có hash provenance. Không gọi API mới.

**Cấu hình:** Kiểm tra boolean trong môi trường Codex vẫn chưa có key/model/live flags. Không đọc process environment của Terminal khác hoặc tìm key trong file riêng. Người dùng cần chạy lệnh trong Terminal đã cấu hình; không cần gửi key trong chat. Chuẩn bị thêm scope T02/T03, chưa chạy, chưa có kết quả hoặc quyền tự suy ra dùng thêm nhiều lượt API.

**Kiểm tra:** Parse tất cả scope bằng Pydantic; kiểm tra artifact derivative, quote matching và hash cha. Không có thay đổi code kể từ suite 47 passed trước đó; không tuyên bố đã chạy live lại hoặc có human audit.

## T01 live thực tế và sửa lỗi kỳ đo

**Thông tin người dùng:** Đã tự cấu hình private key/model trong terminal và chạy CLI, gửi artifact directory `runs/9e512f9c-3771-472a-9cba-3e1a5a87ae10`, partial, 2 calls, 5 claims, human audit pending. Không gửi key trong chat.

**Kiểm chứng thực tế:** Đọc artifact: 67.636 giây, 7 search queries được báo, 6 tài liệu đọc được nhưng 2 duplicate và 1 chỉ navigation. Cả 5 claim bị loại do so period bằng chuỗi; 2 findings bị loại. AI audit đối chiếu snapshots và mở Sensor Tower/Mobile Index/Newsis: có chi tiết vượt quote, metadata phương pháp chưa có bằng chứng và causal inference PC revenue không đủ cơ sở. Chưa có human verification. Chi tiết tại `live-T01-review.md`.

**Thay đổi:** Thêm measurement bounds có schema validation, kiểm tra containment thay vì chuỗi khi scope có bounds; giữ fallback cho scope cũ; UI/scope/export/prompt hỗ trợ dates. Prompt sửa yêu cầu Research dimensions và causal caution, chưa live-validated. 47 tests passed. Replay local với khoảng ngày do AI đề xuất: 5 mechanically checked, completed cơ học; vẫn có lỗi ngữ nghĩa, không gọi lại API, không ghi human_verified. Giữ nguyên run gốc và lưu parent hash/provenance.

**Còn thiếu:** Người dùng audit claim, kiểm chứng prompt sửa bằng run live mới trong giới hạn được xác nhận, T02/T03/T06/T09 và bài nộp cuối. T01 gốc là actual live product failure, không được đổi thành PASS bằng replay.

## Chuẩn bị bước live tiếp theo trong phiên tiếp nối

**Yêu cầu người dùng:** `vay bat dau lam buoc tiep theo thoi`.

**Kết quả thực tế:** Kiểm tra có/không của cấu hình trong môi trường tiến trình: chưa có GEMINI_API_KEY/GOOGLE_API_KEY, GEMINI_MODEL, GMI_LIVE_ENABLED, GMI_KEY_AUTHORIZED, GMI_BUDGET_NOTE hoặc GMI_MAX_CALLS. Không đọc/in giá trị secret, không gọi Gemini. Chuẩn bị CLI preflight mặc định không network; chỉ chạy khi có --run và cấu hình đủ, tối đa hai attempts, lưu artifact riêng trong runs/ đã gitignore. Thêm scope T01 và mẫu audit pending, hướng dẫn cấu hình key riêng. Bộ test hiện tại: 40 passed, gồm chặn CLI chưa cấu hình trước khi tạo provider và giữ audit ngữ nghĩa ở pending.

**AI-PROPOSAL:** T01 là current retrieval cho kỳ launch March–June 2025 tại South Korea; không tuyên bố tái dựng cutoff Mission 1. Đã hỏi người dùng model và giới hạn thử nghiệm; chưa nhận câu trả lời tại thời điểm ghi log. Chưa có live output, human audit hoặc kết luận về chất lượng nghiên cứu.

**Nguồn kỹ thuật đối chiếu:** Google grounding https://ai.google.dev/gemini-api/docs/google-search/ và pricing https://ai.google.dev/gemini-api/docs/pricing. Giới hạn API attempts không đồng nghĩa trần tiền hoặc số search queries.

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

## M2-EL-005 Repo public, cold start và lựa chọn demo local

**Công cụ/model:** Git, GitHub browser, Python/pytest, Streamlit browser, FFmpeg; không gọi Gemini API.

**Nguyên văn trả lời mới của người dùng:**

> Giữ demo local trước

**Mục tiêu:** Đưa mã đã kiểm thử lên GitHub public, xác minh fresh local run, chuẩn bị gói review và thử điều kiện deploy.

**Kết quả AI:** Tạo repo public `nghunganh110/gamota-game-market-intelligence`, merge README khởi tạo GitHub với README đầy đủ local; push main thành công và xác nhận app.py/gmi/tests/docs hiện trên trang public. Thêm reviewer sửa source assessment và lưu history; hard blocker phải định nghĩa trước. Kiểm thử cuối 37 passed. Tạo source checkout sạch từ Git archive và venv mới, cài requirements từ cache offline, 37 passed. Demo browser tái hiện good/conflict/missing/semantic failure. Có video preview offline 88 giây bằng ảnh màn hình thực và phụ đề, không có narration và không phải live research.

**Nguồn bằng chứng:** Git push result, repo URL, pytest-final/pytest-clean artifacts, browser screenshots và metadata video. Secret-pattern scan không phát hiện key/private-key patterns ở tracked text; .env/.streamlit/secrets.toml/.venv bị ignore; không commit key.

**Hành động kiểm chứng và lỗi giữ lại:** Bản server đang chạy trước thay đổi module giữ import cũ và báo thiếu SourceReview khi hot reload. Restart server và browser cold start chạy được. Repo public đã được kiểm tra trên trang; GitHub CI chỉ ghi đạt sau khi nhìn thấy kết quả cụ thể. Video preview được kiểm tra duration và frame ngữ nghĩa. Không tạo snapshot thị trường giả.

**Quyết định người dùng:** USER-DECISION: giữ demo local trước sau khi thấy Streamlit yêu cầu quyền GitHub rộng (public repositories, webhooks/services, Codespaces, email/tổ chức). Không cấp quyền thay người dùng; dừng deploy và đóng tab authorize. Quyền dùng Gemini đã xác nhận ở M2-EL-004; budget/model/key local vẫn chưa có.

**AI-PROPOSAL và phần chờ:** Ba Forced Decisions/kịch bản video vẫn là bản thảo để người dùng rà soát. Chưa chạy T01–T03/T06/T09 live, chưa có human audit thực, chi phí live, demo online hoặc video bài nộp cuối. Preview offline không thay thế các yêu cầu này. Deadline chính xác chưa được cung cấp.

**Cập nhật kiểm chứng bổ sung:** GitHub Actions `Offline tests` đã hiển thị completed successfully cho implementation commit `21e3e14`: https://github.com/nghunganh110/gamota-game-market-intelligence/actions/runs/38584626587. Main local và remote đã đồng bộ sau báo cáo môi trường sạch. Video preview offline đã xác minh H.264, 88 giây, ảnh màn hình thực và phụ đề đọc được; đây là video minh họa tiến độ, không phải live research hoặc video bài nộp cuối.
