# Evidence Log — NextGen Gamota Mission 1

## Quy ước trạng thái

- `FACT-VERIFIED`: dữ kiện đã đối chiếu với nguồn được ghi rõ.
- `USER-PROVIDED`: thông tin do người dùng cung cấp, chưa mặc nhiên được xem là đã xác minh độc lập.
- `HYPOTHESIS`: giả thuyết cần kiểm chứng.
- `AI-PROPOSAL`: phương án/nhận định do AI đề xuất, chưa phải quyết định của người dùng.
- `USER-DECISION`: quyết định đã được người dùng xác nhận rõ ràng.
- `PENDING`: chưa thực hiện hoặc chưa có đủ thông tin.

## Chỉ mục

| ID | Công cụ/model | Mục tiêu | Trạng thái |
|---|---|---|---|
| EL-001 | Codex assistant; model hiển thị chính xác chưa được ghi nhận | Lập kế hoạch, thiết kế Evidence Log, bắt đầu Problem Framing | Chờ người dùng phản biện tại Checkpoint 1 |
| EL-002 | Codex assistant; model hiển thị chính xác chưa được ghi nhận | Ghi nhận Forced Decision 1; bắt đầu Solution & Trust Flow | Chờ người dùng phản biện tại Checkpoint 2 |
| EL-003 | Codex assistant; model hiển thị chính xác chưa được ghi nhận | Ghi nhận Solution & Trust Flow; thiết kế logic khuyến nghị và phản biện MVP 3 ngày | Chờ người dùng phản biện tại Checkpoint 3 |
| EL-004 | Codex assistant + web search/open; model hiển thị chính xác chưa được ghi nhận | Ghi nhận logic khuyến nghị và nghiên cứu shortlist case thực tế | Chờ người dùng chọn case |
| EL-005 | Codex assistant + web search/open; model hiển thị chính xác chưa được ghi nhận | Ghi nhận lựa chọn MABINOGI MOBILE; lập Research Brief và Claim Ledger | Chờ người dùng phản biện Research Brief/Claim Ledger |
| EL-006 | Codex assistant + web search/open + document/PDF tooling; model hiển thị chính xác chưa được ghi nhận | Chốt thiết kế và tạo bản thảo Mission 1 cùng Evidence Log hoàn chỉnh | Bản thảo đã tạo; chờ người dùng kiểm tra lần cuối |

---

## EL-001 — Khởi động quy trình hợp tác

**Công cụ/model:** Codex assistant + công cụ web search/open; model hiển thị chính xác chưa được ghi nhận  
**Nguyên văn prompt:**

> Tôi đang tham gia chương trình tuyển chọn NextGen của Gamota và được giao Mission 1 — Bài test A: Game Market Intelligence.
>
> **Bối cảnh:** Gamota cần một sản phẩm ứng dụng AI giúp nghiên cứu thị trường game nhanh hơn, có hệ thống hơn và tạo ra những nhận định có thể sử dụng cho việc ra quyết định kinh doanh. Thông tin trên Internet phân tán, có mức độ tin cậy khác nhau, có thể lỗi thời hoặc mâu thuẫn. Câu hỏi cốt lõi: Làm thế nào để kết quả nghiên cứu vừa đáng tin cậy, vừa thực sự giúp người dùng đưa ra quyết định?
>
> **Yêu cầu Mission 1:** Chưa cần code. Cần phân tích vấn đề và người dùng; giải pháp và luồng hoạt động; vai trò AI, dữ liệu và con người; các quyết định và rủi ro; kiểm chứng và MVP. Bài nộp là PDF/DOCX tối đa 5 trang.
>
> **Ba Forced Decisions bắt buộc:**
>
> 1. Nếu chỉ giải quyết một vấn đề quan trọng nhất, tôi chọn vấn đề nào, cho người dùng nào, và họ cần kết quả gì?
> 2. Nếu có 3 ngày xây MVP, tôi làm gì trước, chưa làm gì và vì sao?
> 3. Nếu hai nguồn đáng tin đưa ra kết luận trái ngược, hệ thống xử lý thế nào?
>
> **Tiêu chí đánh giá:** Problem Framing 40%, Execution 35%, Decision Quality 25%. Hạn nộp 07:00 ICT ngày 09/10/2026.
>
> Tôi muốn thực sự tham gia tư duy và ra quyết định, không giao hoàn toàn bài làm cho AI.
>
> Hãy làm việc theo vai trò Product Research Mentor, AI Solution Architect và Critical Reviewer.
>
> **Quy tắc hợp tác:**
>
> - Không tự động viết toàn bộ bài nộp ngay.
> - Phân chia công việc thành những giai đoạn rõ ràng.
> - Với mỗi quyết định quan trọng, đề xuất các phương án, ưu nhược điểm, trade-off và yêu cầu tôi tự lựa chọn.
> - Phân biệt dữ kiện đã xác minh, giả thuyết và đề xuất của AI.
> - Không tự tạo thông tin phỏng vấn người dùng, kết quả thử nghiệm, số liệu nghiên cứu hay nguồn tham khảo.
> - Không thay quyết định của tôi bằng quyết định của AI.
> - Sau mỗi giai đoạn, dừng tại điểm kiểm tra để tôi phản biện hoặc chỉnh sửa trước khi tiếp tục.
>
> **Evidence Log — yêu cầu bắt buộc xuyên suốt:**\
> Ngay từ bây giờ, duy trì một nhật ký gồm: ID, thời gian, công cụ/model, nguyên văn prompt, mục tiêu, kết quả AI, nguồn bằng chứng, hành động kiểm chứng, quyết định của tôi và lý do.
>
> Phải phân biệt rõ đề xuất do AI đưa ra và quyết định do tôi thực sự xác nhận. Không tự ghi một thao tác là đã hoàn thành nếu chưa thực hiện.
>
> Lưu ý: Trước cuộc trò chuyện Work này, tôi đã sử dụng ChatGPT để tìm hiểu yêu cầu. Hãy ghi nhận đó là hỗ trợ AI ở giai đoạn chuẩn bị; tôi sẽ cung cấp thông tin bổ sung nếu cần.
>
> Trước tiên, hãy đưa ra kế hoạch làm việc, cách tổ chức Evidence Log và bắt đầu bằng việc khám phá Problem Framing. Chưa tạo tài liệu nộp cuối cùng.

**Mục tiêu:** Lập kế hoạch theo giai đoạn; thiết kế Evidence Log; đưa ra các phương án Problem Framing để người dùng lựa chọn; chưa tạo bài nộp cuối.  
**Kết quả AI:** Đề xuất quy trình 5 giai đoạn có checkpoint; thiết kế quy ước phân loại dữ kiện/giả thuyết/đề xuất/quyết định; đưa ra ba phương án Problem Framing: (A) sàng lọc cơ hội phát hành cho Publishing/Strategy, (B) lập kế hoạch launch cho Product/Marketing, (C) ưu tiên cơ hội scouting cho BD. AI nghiêng về A nhưng chỉ ở phạm vi quyết định “có nên đưa vào thẩm định sâu hơn”, không phải quyết định đầu tư/phát hành cuối cùng. Tất cả vẫn là `AI-PROPOSAL`, đang chờ người dùng phản biện và lựa chọn.  
**Nguồn bằng chứng:** Prompt của người dùng (`USER-PROVIDED`). Chưa sử dụng nguồn Internet.  
**Hành động kiểm chứng:** Chưa kiểm chứng độc lập yêu cầu chương trình, tiêu chí hoặc hạn nộp.  
**Quyết định của người dùng:** Đã xác nhận các quy tắc hợp tác và yêu cầu chưa tạo tài liệu nộp cuối. Chưa xác nhận target user, vấn đề trọng tâm, outcome, scope MVP hoặc quy tắc xử lý nguồn mâu thuẫn.  
**Lý do:** Người dùng muốn trực tiếp tham gia tư duy và giữ quyền ra quyết định.

---

## EL-002 — Xác nhận Forced Decision 1

**Công cụ/model:** Codex assistant; model hiển thị chính xác chưa được ghi nhận  
**Nguyên văn prompt:**

> Mình chọn phương án A — Sàng lọc cơ hội phát hành game.
>
> - Người dùng chính: Publishing/Strategy Lead tại Gamota,
> - Quyết định họ phải đưa ra: Một tựa game hoặc phân khúc game có đủ tiềm năng để dành thêm thời gian và nguồn lực nghiên cứu sâu hơn hay không.
> - Kết quả họ cần nhận: Mình muốn hệ thống đưa ra một bản phân tích ngắn gọn, có dẫn chứng rõ ràng, chỉ ra cơ hội, rủi ro và những thông tin còn thiếu. Từ đó đề xuất nên tiếp tục nghiên cứu, tạm giữ để bổ sung dữ liệu hay dừng lại.
> - Sai lầm nguy hiểm hơn: Theo mình, ở giai đoạn sàng lọc ban đầu, bỏ lỡ một cơ hội thực sự tốt có thể đáng tiếc hơn việc đưa một cơ hội chưa tốt vào vòng nghiên cứu tiếp theo. Vì đây chưa phải quyết định đầu tư hay phát hành chính thức nên nếu đánh giá nhầm một cơ hội xấu là tốt, chúng ta vẫn còn bước thẩm định để phát hiện. Tuy nhiên, mình cũng không muốn hệ thống quá dễ dãi vì như vậy sẽ lãng phí nguồn lực. Với những trường hợp chưa đủ bằng chứng, mình nghiêng về việc đánh dấu cần nghiên cứu thêm thay vì vội kết luận.
> - Lý do lựa chọn: Mình chọn A vì thấy nó gắn với một quyết định kinh doanh khá rõ ràng và phù hợp với vấn đề đề bài đang đặt ra: làm sao biến thông tin trên Internet thành nhận định đáng tin cậy. So với B thì phương án này ít phụ thuộc vào dữ liệu nội bộ của một game cụ thể hơn. Còn so với C, mình thấy A có phạm vi dễ xác định hơn và không nhất thiết phải xây dựng hệ thống xếp hạng nhiều game ngay từ đầu.

**Mục tiêu:** Xác nhận target user, quyết định cần hỗ trợ, đầu ra mong muốn và chi phí tương đối của hai loại sai lầm trong giai đoạn sàng lọc.  
**Kết quả AI:** AI chuyển quyết định thành problem statement dự thảo và đề xuất luồng 8 bước: xác lập brief, phân rã câu hỏi, tìm nguồn, lập claim ledger, đối chiếu, tổng hợp, tạo decision brief và người dùng phê duyệt/ghi lý do. Ba chế độ được đưa ra: (1) nguồn do người dùng cung cấp, (2) AI tìm nguồn nhưng hiển thị đầy đủ bằng chứng và con người quyết định cuối, (3) AI nghiên cứu gần như tự động. AI nghiêng về chế độ (2). AI cũng đề nghị tách confidence khỏi recommendation và không dùng “độ tự tin của mô hình” làm thước đo độ tin cậy. Tất cả phần thiết kế giải pháp vẫn là `AI-PROPOSAL`; đang chờ người dùng chọn chế độ vận hành và đối tượng sàng lọc của MVP.  
**Nguồn bằng chứng:** Prompt của người dùng (`USER-PROVIDED`, `USER-DECISION`). Chưa sử dụng nguồn Internet.  
**Hành động kiểm chứng:** Chưa kiểm chứng bằng phỏng vấn Publishing/Strategy Lead hoặc dữ liệu quy trình nội bộ Gamota. Cần xem đây là problem framing do người tham gia bài test lựa chọn, không phải nhu cầu người dùng đã được xác thực.  
**Quyết định của người dùng:** Chọn bài toán sàng lọc cơ hội phát hành cho Publishing/Strategy Lead. Đầu ra là bản phân tích ngắn có dẫn chứng, cơ hội, rủi ro và khoảng trống thông tin; khuyến nghị `tiếp tục nghiên cứu / tạm giữ để bổ sung dữ liệu / dừng`. Ưu tiên giảm nguy cơ bỏ lỡ cơ hội tốt, nhưng không chấp nhận cơ chế quá dễ dãi; trường hợp thiếu bằng chứng nên chuyển sang nghiên cứu thêm.  
**Lý do:** Quyết định kinh doanh rõ; phù hợp bài toán biến thông tin Internet thành nhận định đáng tin; ít phụ thuộc dữ liệu nội bộ hơn phương án launch; phạm vi rõ hơn và không cần xếp hạng nhiều game như phương án scouting.

---

## EL-003 — Xác nhận Solution & Trust Flow

**Công cụ/model:** Codex assistant; model hiển thị chính xác chưa được ghi nhận  
**Nguyên văn prompt:**

> Mình đồng ý với hướng giải quyết bạn đề xuất, nhưng có một vài điểm mình muốn làm rõ thêm.
> 1. Về chế độ vận hành: Mình chọn phương án 2 — Evidence-centered hybrid.
> Theo mình, nếu chọn phương án 1 thì hệ thống vẫn phụ thuộc khá nhiều vào việc người dùng tự tìm tài liệu, trong khi một trong những vấn đề ban đầu là quá trình thu thập và tổng hợp thông tin đang tốn thời gian. Còn phương án 3 thì mình thấy hơi rủi ro, nhất là khi AI có thể tìm được nhiều nguồn nhưng chưa chắc những nguồn đó thực sự phù hợp với câu hỏi.
> Mình muốn AI chủ động tìm kiếm, tổng hợp và đối chiếu thông tin, nhưng phải cho người dùng kiểm tra lại được những bằng chứng quan trọng. Tuy nhiên, cũng không nên bắt người dùng xác minh thủ công tất cả các nguồn. Mình nghĩ nên ưu tiên những nhận định ảnh hưởng trực tiếp đến khuyến nghị, những nguồn có độ tin cậy thấp hoặc đang mâu thuẫn nhau.
> 2. Về quyền quyết định: Mình đồng ý để AI đưa ra đề xuất, còn Publishing/Strategy Lead là người quyết định cuối cùng.
> Lý do là AI chỉ có thể phân tích dựa trên những dữ liệu được cung cấp hoặc thu thập được, trong khi quyết định kinh doanh thực tế còn phụ thuộc vào nhiều yếu tố nội bộ mà AI chưa biết, chẳng hạn ngân sách, chiến lược phát hành hoặc nguồn lực của công ty.
> Mình cũng muốn người dùng có thể thay đổi đề xuất của AI và ghi lại lý do. Điều này sẽ giúp hệ thống minh bạch hơn, đồng thời có dữ liệu để đánh giá và cải thiện chất lượng khuyến nghị về sau.
> 3. Về phạm vi MVP: Mình chọn một tựa game mobile cụ thể tại thị trường Việt Nam.
> Mình nghĩ trong 3 ngày, việc tập trung vào một trường hợp cụ thể sẽ dễ triển khai và kiểm chứng hơn so với nghiên cứu cả một phân khúc. Mình muốn chứng minh được toàn bộ quy trình từ đặt câu hỏi, thu thập nguồn, đối chiếu thông tin đến đưa ra một decision brief có thể sử dụng được.
> Tuy nhiên, mình chưa muốn chốt tên game ngay. Mình muốn chọn một game có đủ dữ liệu công khai để kiểm thử, nhưng vẫn tồn tại những điểm cần phân tích hoặc đối chiếu. Nếu dữ liệu quá ít thì khó đánh giá được hệ thống, còn nếu chỉ chọn một trường hợp quá đơn giản thì kết quả demo cũng chưa thuyết phục.
> Một điểm nữa mình muốn bổ sung: Với ba trạng thái Tiếp tục / Tạm giữ / Dừng, mình nghĩ cần xác định rõ điều kiện đưa ra từng khuyến nghị, thay vì để AI tự quyết định theo cảm nhận. Đặc biệt, thiếu thông tin không nên mặc định là lý do để loại bỏ một cơ hội.
> Bạn hãy ghi nhận ba lựa chọn này vào Evidence Log.
> Sau đó, hãy giúp mình thiết kế các điều kiện để hệ thống đưa ra ba trạng thái khuyến nghị và phản biện xem phạm vi MVP này có khả thi trong 3 ngày không. Mình muốn làm rõ logic trước khi chuyển sang phần công nghệ.

**Mục tiêu:** Ghi nhận ba lựa chọn thiết kế; xây dựng điều kiện giải thích được cho `Tiếp tục / Tạm giữ / Dừng`; đánh giá tính khả thi của MVP 3 ngày trước khi bàn công nghệ.  
**Kết quả AI:** AI đề xuất phân biệt `Tiếp tục` (mở vòng thẩm định đầy đủ), `Tạm giữ` (chỉ thực hiện kiểm chứng hẹp, có thời hạn) và `Dừng` (loại khỏi pipeline hiện tại). Logic đề xuất là hybrid: hard gate do con người cấu hình; evidence gate; sau đó mới đánh giá opportunity thesis và rủi ro. Thiếu dữ liệu hoặc mâu thuẫn có khả năng đảo chiều dẫn đến `Tạm giữ`, không tự động dẫn đến `Dừng`; `Dừng` đòi hỏi hard blocker đã được xác minh hoặc bằng chứng đủ bao phủ và tín hiệu tiêu cực hội tụ. MVP được đánh giá là khả thi trong 3 ngày nếu được định nghĩa là prototype theo một case, có claim ledger, conflict card, decision brief và human override; không khả thi nếu kỳ vọng sản phẩm tự động hóa tổng quát hoặc chứng minh độ chính xác trên thị trường. Đây là `AI-PROPOSAL`, chưa được người dùng xác nhận.  
**Nguồn bằng chứng:** Prompt của người dùng (`USER-PROVIDED`, `USER-DECISION`). Chưa sử dụng nguồn Internet.  
**Hành động kiểm chứng:** Chưa thực hiện kiểm thử trên game cụ thể, chưa phỏng vấn người dùng và chưa xác thực tính sẵn có của nguồn.  
**Quyết định của người dùng:** (1) Chọn Evidence-centered hybrid; AI chủ động tìm, tổng hợp và đối chiếu, còn việc kiểm tra thủ công ưu tiên claim ảnh hưởng trực tiếp đến khuyến nghị, nguồn yếu và nguồn mâu thuẫn. (2) AI đề xuất; Publishing/Strategy Lead quyết định cuối, có thể override và ghi lý do. (3) MVP tập trung vào một game mobile tại Việt Nam; chưa chọn tên game; game thử nghiệm phải đủ dữ liệu công khai nhưng vẫn có điểm cần đối chiếu. Thiếu thông tin không được mặc định thành lý do loại bỏ.  
**Lý do:** Cân bằng tốc độ với khả năng kiểm tra; giữ bối cảnh và trách nhiệm quyết định ở con người; giới hạn một trường hợp để chứng minh toàn bộ quy trình trong 3 ngày.

---

## EL-004 — Chuyển sang nghiên cứu case thực tế

**Công cụ/model:** Codex assistant; model hiển thị chính xác chưa được ghi nhận  
**Nguyên văn prompt:**

> Mình đồng ý với hướng thiết kế này. Mình thấy việc chia thành ba trạng thái và sử dụng các bước kiểm tra trước khi đưa ra khuyến nghị sẽ hợp lý hơn là để AI tự đánh giá rồi kết luận.
> 1. Về ba trạng thái
> Mình đồng ý với cách định nghĩa Tiếp tục, Tạm giữ và Dừng.
> Tuy nhiên, mình muốn làm rõ thêm trạng thái Tạm giữ. Theo mình, nếu hệ thống chỉ nói cần nghiên cứu thêm thì chưa thực sự giúp ích cho người dùng. Nó cần chỉ ra cụ thể đang thiếu thông tin gì, thông tin đó quan trọng như thế nào và nên tìm ở đâu.
> Ngoài ra, không nên để một cơ hội ở trạng thái Tạm giữ mãi. Nếu sau một khoảng thời gian hoặc một số bước kiểm chứng nhất định mà vẫn không có đủ dữ liệu, người phụ trách cần quyết định có tiếp tục dành nguồn lực cho nó không.
> 2. Về cách đưa ra khuyến nghị
> Mình chọn phương án Hybrid: hard gate + evidence gate + đánh giá có cấu trúc.
> Mình không muốn dùng hoàn toàn điểm số có trọng số vì ở giai đoạn đầu, chúng ta chưa có đủ cơ sở để biết trọng số nào là hợp lý. Nếu tự gán điểm thì kết quả có vẻ khách quan nhưng thực chất vẫn phụ thuộc khá nhiều vào giả định ban đầu.
> Tuy nhiên, mình cũng không muốn hệ thống quá cứng nhắc. Các hard blocker cần được xác định trước và phải có bằng chứng rõ ràng. Còn khi đánh giá tiềm năng của game, AI nên tổng hợp cả tín hiệu tích cực lẫn tiêu cực, giải thích lý do đề xuất thay vì chỉ kiểm tra một danh sách điều kiện rồi kết luận.
> Với những trường hợp chưa chắc chắn, mình vẫn ưu tiên Tạm giữ để kiểm chứng thêm. Đặc biệt, mình muốn hạn chế việc hệ thống loại bỏ một cơ hội chỉ vì thiếu dữ liệu.
> 3. Về phạm vi MVP
> Mình đồng ý giới hạn MVP trong một case cụ thể, một game mobile tại thị trường Việt Nam.
> Mục tiêu trước mắt của mình là chứng minh hệ thống có thể xử lý được một quy trình nghiên cứu hoàn chỉnh: tìm nguồn, trích xuất thông tin, đối chiếu bằng chứng, phát hiện vấn đề và đưa ra một báo cáo có thể kiểm tra lại.
> Mình không muốn tuyên bố rằng hệ thống có khả năng dự đoán thành công của game chỉ sau một lần thử nghiệm. Theo mình, điều cần chứng minh trước là quy trình có hoạt động đúng và giúp người dùng đánh giá thông tin tốt hơn hay không.
> Về bước tiếp theo, mình muốn bắt đầu nghiên cứu thực tế thay vì tiếp tục thiết kế trên giả định.
> Bạn hãy tìm giúp mình khoảng 2–3 tựa game phù hợp với các tiêu chí đã đề xuất. Với mỗi game, hãy kiểm tra dữ liệu công khai hiện có, những thông tin còn thiếu, rủi ro khi lựa chọn và khả năng xây dựng một case nghiên cứu trong 3 ngày.
> Mình muốn xem bằng chứng thực tế rồi tự chọn game, chứ không muốn chọn trước một game và sau đó chỉ đi tìm thông tin để chứng minh lựa chọn đó là đúng.
> Hãy cập nhật ba quyết định trên vào Evidence Log, phân biệt rõ đâu là đề xuất của AI và đâu là những lý do mình đã đưa ra. Sau đó chuyển sang bước nghiên cứu và lựa chọn case thử nghiệm.

**Mục tiêu:** Xác nhận semantics của ba trạng thái, cơ chế hybrid và giới hạn chứng minh của MVP; sau đó nghiên cứu 2–3 game bằng cùng một rubric để người dùng tự chọn case.  
**Kết quả AI:** Đã áp dụng cùng một rubric sơ bộ cho ba ứng viên: `MABINOGI MOBILE`, `Dungeon&Fighter Mobile` và `Roco Kingdom`. `AI-PROPOSAL`: MABINOGI MOBILE là case cân bằng nhất vì có dữ liệu performance, rollout nhiều thị trường và mâu thuẫn giữa tín hiệu thương mại với rating cửa hàng; Dungeon&Fighter Mobile có dữ liệu vòng đời mạnh nhưng khả năng chuyển dịch từ Trung Quốc và quyền phát hành Việt Nam là khoảng trống lớn; Roco Kingdom có dữ liệu China breakout nhưng global rollout đã do MoreFun Studios công bố, khiến câu hỏi cơ hội phát hành cho Gamota dễ bị chi phối bởi availability of rights. Chưa có game nào được chọn.  
**Nguồn bằng chứng:** Prompt của người dùng (`USER-PROVIDED`, `USER-DECISION`) và các nguồn web sau:

- Nexon product catalogue: <https://www.nexon.co.jp/en/products/>
- Nexon 2026 Capital Markets Briefing: <https://www.nexon.co.jp/en/ir/uploads/CMB%202026%20Presentation%20Slides%20with%20Speech%20Script.pdf>
- Nexon press release về Dungeon&Fighter Mobile tại Trung Quốc: <https://www.businesswire.com/news/home/20240521410069/en/Nexons-Highly-Anticipated-DungeonFighter-Mobile-Now-Available-in-China>
- Sensor Tower analysis về MABINOGI MOBILE: <https://sensortower.com/ko/blog/Mabinogi-Mobile-achieves-cumulative-revenue-of-30-million>
- Google Play Korea listing của MABINOGI MOBILE: <https://play.google.com/store/apps/details?gl=kr&id=com.nexon.devcat.mm>
- Nexon news index về rollout MABINOGI MOBILE: <https://www.nexon.co.jp/en/news/>
- Tencent Q1 2026 results/presentation về Roco Kingdom: <https://static.www.tencent.com/uploads/2026/05/13/59cf8219adbb046153f69387479350ac.pdf>
- MoreFun/Proxima Beta press release về global CBT của Roco Kingdom: <https://prtimes.jp/main/html/rd/p/000000001.000188702.html>
- Steam listing Roco Kingdom: <https://store.steampowered.com/app/4821880/Roco_Kingdom/?l=vietnamese>

**Hành động kiểm chứng:** Đã đối chiếu trang sản phẩm/IR/thông cáo chính thức với storefront và nguồn ước tính có nêu phương pháp. Đã kiểm tra tình trạng rollout hiện tại, tín hiệu performance, rating công khai và kế hoạch global khi có nguồn. Chưa xác minh được quyền phát hành tại Việt Nam, dữ liệu nhu cầu người chơi Việt Nam, chi phí acquisition, retention, unit economics hoặc yêu cầu nội bộ Gamota; các mục này được giữ là `PENDING`, không suy diễn từ thành công tại nước ngoài. Các truy vấn chính đã thực hiện gồm: `MABINOGI MOBILE official launch Korea/revenue/global/Vietnam`, `Dungeon&Fighter Mobile China launch/revenue/global/Vietnam`, `Roco Kingdom China launch/global CBT/Vietnam`, cùng các truy vấn giới hạn trên trang IR và product catalogue của Nexon/Tencent.  
**Quyết định của người dùng:** (1) Xác nhận định nghĩa `Tiếp tục / Tạm giữ / Dừng`; `Tạm giữ` phải nêu thiếu gì, mức độ quan trọng, nơi tìm và phải có điểm tái quyết định sau thời gian/số bước kiểm chứng nhất định. (2) Chọn hybrid: hard gate + evidence gate + đánh giá có cấu trúc; không dùng trọng số chưa có cơ sở; hard blocker phải xác định trước và có bằng chứng; AI phải giải thích cả tín hiệu tích cực và tiêu cực. (3) Giới hạn MVP ở một game mobile cho thị trường Việt Nam nhằm chứng minh quy trình và khả năng kiểm tra lại, không tuyên bố dự đoán thành công hay tổng quát hóa từ một case.  
**Lý do:** Tránh trạng thái chờ vô hạn; tránh tính khách quan giả của trọng số tự gán; giữ độ linh hoạt nhưng không loại cơ hội chỉ vì thiếu dữ liệu; ưu tiên chứng minh chất lượng quy trình trước độ chính xác dự báo.

---

## EL-005 — Chọn MABINOGI MOBILE làm case MVP

**Công cụ/model:** Codex assistant + công cụ web search/open; model hiển thị chính xác chưa được ghi nhận  
**Nguyên văn prompt:**

> Sau khi xem ba phương án thì mình quyết định chọn **MABINOGI MOBILE** để làm case nghiên cứu cho MVP.
> **1. Lý do mình chọn**
> Mình thấy MABINOGI MOBILE phù hợp nhất vì game đã có dữ liệu ở một số thị trường và có nhiều loại nguồn để đối chiếu, từ thông tin của Nexon, báo cáo Sensor Tower đến đánh giá của người chơi.
> Điều mình quan tâm là game có tín hiệu thương mại khá tốt trong giai đoạn đầu nhưng điểm đánh giá trên cửa hàng lại không cao. Tuy nhiên, mình không nghĩ có thể kết luận ngay rằng game thành công về doanh thu nhưng thất bại về trải nghiệm. Hai chỉ số này phản ánh những khía cạnh khác nhau, và rating thấp cũng có thể đến từ những nguyên nhân như khóa vùng hoặc vấn đề kỹ thuật.
> Mình muốn xem hệ thống có phân biệt được những điều này hay không, thay vì chỉ nhìn vào một vài con số rồi đưa ra kết luận.
> **2. Mâu thuẫn mình muốn hệ thống xử lý**
> Mình muốn tập trung vào sự khác biệt giữa tín hiệu thành công ban đầu, phản hồi của người chơi và khả năng duy trì hiệu quả về lâu dài.
> Ví dụ, doanh thu giai đoạn ra mắt tốt chưa chắc đồng nghĩa với việc game sẽ tiếp tục tăng trưởng. Ngược lại, điểm đánh giá thấp cũng chưa đủ để kết luận game không có tiềm năng.
> Mình muốn AI phân tích được các nguồn đang nói về điều gì, dữ liệu thuộc giai đoạn nào, có thực sự trái ngược nhau không và còn thiếu bằng chứng gì để đưa ra nhận định đáng tin cậy.
> **3. Những rủi ro không được bỏ qua**
> Điều mình lo ngại nhất là hệ thống lấy thành công của game tại Hàn Quốc rồi suy ra game cũng sẽ thành công tại Việt Nam. Mức độ nhận diện IP, thị hiếu người chơi và khả năng chi trả giữa các thị trường có thể rất khác nhau.
> Ngoài ra, quyền phát hành tại Việt Nam cũng là một vấn đề quan trọng. Nếu Nexon không có nhu cầu hợp tác với nhà phát hành địa phương thì dù game có tiềm năng, cơ hội kinh doanh thực tế của Gamota vẫn có thể không tồn tại.
> Vì vậy, mình muốn tách riêng hai câu hỏi: game có tiềm năng tại Việt Nam không, và Gamota có khả năng tham gia phát hành game đó không. Những gì chưa xác minh được phải được ghi rõ là chưa biết.
> **4. Mốc nghiên cứu**
> Mình chọn sử dụng dữ liệu công bố trước thời hạn nộp Mission 1, tức 07:00 ICT ngày 09/10/2026.
> Mình không muốn dùng những kết quả xuất hiện sau mốc này để củng cố cho nhận định trước đó. Đặc biệt, game mới ra mắt tại Nhật nên chưa nên dùng kết quả thị trường Nhật để đánh giá hiệu quả dài hạn.
> **5. Bước tiếp theo**
> Bạn hãy ghi nhận lựa chọn MABINOGI MOBILE vào Evidence Log là USER-DECISION, đồng thời ghi rõ đây là lựa chọn được đưa ra sau khi mình xem xét shortlist do AI đề xuất, chứ không phải do mình tự phát hiện game.
> Sau đó, hãy xây dựng Research Brief và Claim Ledger cho game này. Mình muốn ưu tiên kiểm tra lại các nguồn gốc, phân biệt dữ kiện đã xác minh với ước tính hoặc suy luận.
> Trước khi chuyển sang thiết kế công nghệ, mình muốn biết những bằng chứng hiện có đã đủ để đưa ra khuyến nghị sơ bộ hay chưa, và nếu chưa đủ thì chính xác chúng ta đang thiếu gì.

**Mục tiêu:** Ghi nhận case do người dùng chọn; thiết lập cutoff bằng chứng; lập Research Brief và Claim Ledger theo hai decision tracks; đánh giá evidence sufficiency trước khi bàn công nghệ.  
**Kết quả AI:** Đã tạo Research Brief với hai decision tracks và Claim Ledger gồm 18 claim. Kết luận sơ bộ của AI là `TẠM GIỮ — targeted validation`, vì đã có đủ bằng chứng về launch strength tại Hàn Quốc nhưng chưa đạt evidence gate cho Vietnam-specific demand và rights/business access. Đây là `AI-PROPOSAL`, chưa phải quyết định của người dùng. Verification plan ưu tiên: xác nhận quyền với Nexon, kiểm tra Vietnam fit bằng dữ liệu trực tiếp/comparable, phân loại review có hệ thống, kiểm tra transferability từ TW/HK/Macau và đánh giá feasibility nội bộ Gamota.  
**Nguồn bằng chứng:** Prompt của người dùng (`USER-PROVIDED`, `USER-DECISION`), shortlist ở EL-004 (`AI-PROPOSAL`) và các nguồn công bố trước cutoff, gồm:

- Nexon launch announcement: <https://www.nexon.co.jp/en/news/detail/?id=20250327-441557ea>
- Nexon Q1 2025 Earnings Letter: <https://pdf.irpocket.com/C3659/vAfC/Bwkm/njVR.pdf>
- Sensor Tower analysis: <https://sensortower.com/ko/blog/Mabinogi-Mobile-achieves-cumulative-revenue-of-30-million>
- Nexon Q4 2025 Earnings Release: <https://pdf.irpocket.com/C3659/YpwX/lT2o/uIbd.pdf>
- Nexon Q1 2026 Earnings Letter: <https://pdf.irpocket.com/C3659/WUpy/ecSw/IVuJ.pdf>
- Nexon Q2 2026 company release distributed by Yahoo Finance: <https://sg.finance.yahoo.com/news/nexon-releases-earnings-second-quarter-171900722.html>
- Nexon regional expansion release: <https://www.publicnow.com/view/C7631B8E97618EA73627BCDAE772599C141B0AA4>
- Nexon Japan launch announcement: <https://www.nexon.co.jp/news/detail/?id=20260917-44ed4a21>
- Google Play Korea: <https://play.google.com/store/apps/details?gl=kr&id=com.nexon.devcat.mm>
- Apple App Store Korea reviews: <https://apps.apple.com/kr/app/%EB%A7%88%EB%B9%84%EB%85%B8%EA%B8%B0-%EB%AA%A8%EB%B0%94%EC%9D%BC/id1441742921?platform=iphone&see-all=reviews>
- Gamota report summary: <https://gamota.com/en_GB/gamota-lab/understanding-the-market-to-optimize-game-publishing-strategies-gamota-introduces-the-report-vietnam-mobile-gaming-year-in-review-2025/>
- Gamota portfolio/publishing model: <https://gamota.com/en_GB/games/> và <https://gamota.com/en_GB/services/publishing-model/>
- PocketGamer.biz secondary reporting on Gamota report: <https://www.pocketgamer.biz/over-50-of-vietnam-population-plays-mobile-games/>

**Hành động kiểm chứng:** Đã truy về nguồn publisher/IR cho launch và performance claims; phân loại số Sensor Tower là estimate với giới hạn kênh; kiểm tra rating ở cả Google Play và Apple App Store; kiểm tra public rollout regions; kiểm tra summary báo cáo thị trường và capability công khai của Gamota. Chưa truy cập full Gamota report vì yêu cầu đăng ký; chưa liên hệ Nexon; chưa thực hiện social listening, survey/concept test, review coding đầy đủ hoặc internal feasibility review. Không ghi các hoạt động này là đã hoàn thành.  
**Quyết định của người dùng:** Chọn `MABINOGI MOBILE` làm case MVP sau khi xem shortlist do AI đề xuất; không phải game do người dùng tự phát hiện độc lập. Hai câu hỏi phải được tách riêng: (A) tiềm năng tại Việt Nam và (B) khả năng Gamota tham gia phát hành. Cutoff bằng chứng là 07:00 ICT ngày 09/10/2026; không dùng kết quả xuất hiện sau cutoff, và không dùng launch Nhật vừa diễn ra để suy luận hiệu quả dài hạn.  
**Lý do:** Có nhiều loại nguồn và thị trường để đối chiếu; tồn tại căng thẳng giữa tín hiệu thương mại ban đầu, rating và sustainability; cần kiểm tra khả năng AI phân biệt ý nghĩa, phạm vi và thời kỳ của từng chỉ số; tránh suy diễn từ Hàn Quốc sang Việt Nam hoặc bỏ qua quyền phát hành.

---

## EL-006 — Chốt thiết kế và tạo bản thảo Mission 1

**Công cụ/model:** Codex assistant + công cụ web search/open + Python DOCX builder + LibreOffice/Poppler render; model hiển thị chính xác chưa được ghi nhận  
**Nguyên văn prompt:**

> Mình thấy đến đây chúng ta đã phân tích khá kỹ rồi, nên mình muốn chốt các quyết định còn lại và chuyển sang hoàn thiện bài nộp Mission 1, tránh sa đà quá nhiều vào một case cụ thể.
>
> Về ba điểm bạn hỏi:
>
> 1\. Mình đồng ý với trạng thái Tạm giữ — targeted validation.
>
> Với những bằng chứng hiện tại, mình chưa thấy đủ cơ sở để kết luận nên tiếp tục thẩm định đầy đủ hay loại bỏ MABINOGI MOBILE. Mình muốn hệ thống thể hiện rõ những gì đã biết, những gì chưa biết và vì sao những khoảng trống đó quan trọng.
>
> 2\. Mình đồng ý ưu tiên kiểm tra khả năng hợp tác và quyền phát hành, nhưng không muốn việc này chặn toàn bộ quá trình nghiên cứu.
>
> Theo mình, nếu quyền phát hành không khả thi thì các phân tích thị trường tiếp theo có thể không còn nhiều giá trị đối với quyết định của Gamota. Tuy nhiên, việc chưa nhận được xác nhận từ Nexon không đồng nghĩa với việc không có cơ hội hợp tác. Trong MVP, mình muốn hệ thống ghi nhận đây là một vấn đề chưa được xác minh, đồng thời vẫn có thể phân tích Vietnam fit bằng dữ liệu công khai.
>
> 3\. Về quy tắc Day 2 và gia hạn Hold một lần:
>
> Mình đồng ý cần có thời điểm đánh giá lại để tránh giữ một cơ hội vô thời hạn. Tuy nhiên, mình nghĩ giới hạn này nên được xem là quy tắc thử nghiệm trong MVP, không phải chính sách cố định của Gamota. Trong thực tế, thời gian kiểm chứng còn phụ thuộc vào loại thông tin cần thu thập và khả năng tiếp cận nguồn.
>
> Bây giờ mình muốn chuyển sang hoàn thiện Mission 1.
>
> Mình nghĩ chúng ta đã có đủ cơ sở để xây dựng tài liệu. MABINOGI MOBILE chỉ là case minh họa nhằm kiểm chứng hướng thiết kế, không phải toàn bộ phạm vi mà sản phẩm hướng đến.
>
> Hãy thực hiện các bước tiếp theo:
>
> 1. Chốt kiến trúc giải pháp, MVP 3 ngày, các tính năng chủ động chưa làm và phương pháp đánh giá. Giữ phạm vi đơn giản, khả thi.
> 2. Tổng hợp các quyết định mình đã đưa ra trong Evidence Log. Không tự gán những đề xuất của AI thành quyết định của mình.
> 3. Soạn ba câu Forced Decisions dựa trên các ý kiến mình đã thực sự xác nhận. Giữ cách viết tự nhiên, rõ lập luận và tránh văn phong quá máy móc.
> 4. Tạo báo cáo Mission 1 chuyên nghiệp bằng DOCX và PDF, tối đa 5 trang, bao phủ đầy đủ năm nội dung đề bài.
> 5. Rà soát Evidence Log, giữ lại prompt thực tế, các nguồn được sử dụng, phần AI hỗ trợ, phần mình quyết định và những gì vẫn chưa được kiểm chứng.
> 6. Kiểm tra tính chính xác của trích dẫn, số trang thực tế, tính nhất quán của các lập luận và yêu cầu nộp.
>
> Mình muốn ưu tiên hoàn thành một bài nộp tốt, có chiều sâu nhưng súc tích, hơn là tiếp tục mở rộng nghiên cứu.
>
> Từ bây giờ, bạn không cần tạo thêm checkpoint cho những lựa chọn nhỏ. Hãy sử dụng những quyết định mình đã xác nhận, chỉ hỏi lại khi xuất hiện vấn đề thực sự ảnh hưởng đến hướng giải quyết.
>
> Hãy tạo bản thảo bài nộp và Evidence Log hoàn chỉnh để mình kiểm tra lần cuối. Chưa nộp thay mình.

**Mục tiêu:** Chốt thiết kế sản phẩm; viết ba Forced Decisions bằng tiếng nói của người nộp; tạo bản thảo DOCX/PDF tối đa 5 trang; hoàn thiện và kiểm tra Evidence Log; không thực hiện nộp bài.  
**Kết quả AI:** AI đã chốt một kiến trúc năm lớp gồm Research Brief, Search and Source Capture, Claim Ledger, Conflict and Gate Logic, Decision Brief cùng Decision Log. Bản thảo sử dụng logic hard gate + evidence gate + structured assessment, mô tả MVP ba ngày, danh sách chủ động chưa làm, phương pháp đánh giá và ba Forced Decisions dựa trên các lựa chọn đã xác nhận. Case MABINOGI MOBILE chỉ chiếm phần kiểm chứng thiết kế và giữ khuyến nghị `Tạm giữ — targeted validation`. Đã tạo `Mission_1_Game_Market_Intelligence.docx` và `Mission_1_Game_Market_Intelligence.pdf`. Đây là phần tổng hợp và diễn đạt của AI; kiến trúc chi tiết, câu chữ và bố cục tài liệu không được ghi thành `USER-DECISION`.  
**Nguồn bằng chứng:** Toàn bộ prompt EL-001 đến EL-006; Research Brief/Claim Ledger ở EL-005; tám nguồn được trích trong bản thảo:

- Gamota Vietnam Mobile Gaming Year-in-Review 2025 summary: <https://gamota.com/en_GB/gamota-lab/understanding-the-market-to-optimize-game-publishing-strategies-gamota-introduces-the-report-vietnam-mobile-gaming-year-in-review-2025/>
- Nexon Q1 2025 Earnings Letter: <https://pdf.irpocket.com/C3659/vAfC/Bwkm/njVR.pdf>
- Sensor Tower MABINOGI MOBILE analysis: <https://sensortower.com/ko/blog/Mabinogi-Mobile-achieves-cumulative-revenue-of-30-million>
- Nexon Q1 2026 Earnings Letter: <https://pdf.irpocket.com/C3659/WUpy/ecSw/IVuJ.pdf>
- Nexon Capital Markets Briefing 2026: <https://www.nexon.co.jp/en/ir/uploads/CMB%202026%20Presentation%20Slides%20with%20Speech%20Script.pdf>
- Google Play Korea listing: <https://play.google.com/store/apps/details?gl=kr&id=com.nexon.devcat.mm>
- Apple App Store Korea reviews: <https://apps.apple.com/kr/app/%EB%A7%88%EB%B9%84%EB%85%B8%EA%B8%B0-%EB%AA%A8%EB%B0%94%EC%9D%BC/id1441742921?platform=iphone&see-all=reviews>
- Gamota Publishing Model: <https://gamota.com/en_GB/services/publishing-model/>

**Hành động kiểm chứng:** Đã mở lại nguồn Nexon, Sensor Tower, storefront và Gamota; giữ đúng nhãn company-reported, estimate, observed snapshot và unknown. Đã loại bỏ việc dùng absence of evidence về quyền như evidence of absence. DOCX được render thành ảnh và kiểm tra trực quan toàn bộ năm trang sau lần sửa cuối; PDF có 5 trang Letter, được gắn thẻ, không mã hóa. Đã kiểm tra tám hyperlink trong DOCX, trích xuất text PDF để tìm placeholder/tool token, và chạy accessibility audit với kết quả 0 high, 0 medium, 0 low. Chưa nộp bài.  
**Quyết định của người dùng:** (1) Xác nhận `Tạm giữ — targeted validation` cho MABINOGI MOBILE. (2) Ưu tiên kiểm tra quyền/khả năng hợp tác nhưng không dừng toàn bộ nghiên cứu; chưa có phản hồi từ Nexon phải được ghi là chưa xác minh, không phải không có cơ hội. (3) Day 2 và một lần gia hạn Hold là quy tắc thử nghiệm MVP, không phải chính sách Gamota. (4) MABINOGI MOBILE chỉ là case minh họa. (5) Cho phép chuyển sang tạo bản thảo hoàn chỉnh, bỏ checkpoint cho lựa chọn nhỏ và không nộp thay người dùng.  
**Lý do:** Bằng chứng hiện tại chưa đủ cho Continue hoặc Stop; rights có thể làm thay đổi giá trị kinh doanh nhưng absence of response không xác nhận blocker; timebox cần ngăn Hold vô hạn nhưng phải thích ứng với loại thông tin; bài nộp cần ưu tiên độ sâu, tính súc tích và phạm vi sản phẩm thay vì mở rộng thêm case.

---

## Decision Register chỉ gồm quyết định người dùng đã xác nhận

| ID | Quyết định của người dùng | Nguồn xác nhận | Lý do do người dùng nêu |
|---|---|---|---|
| UD-01 | Chọn bài toán sàng lọc cơ hội phát hành cho Publishing hoặc Strategy Lead | EL-002 | Quyết định kinh doanh rõ, phù hợp bài toán biến dữ liệu Internet thành nhận định, ít phụ thuộc dữ liệu nội bộ hơn launch planning và hẹp hơn multi-game scouting |
| UD-02 | Đầu ra là decision brief có nguồn với Tiếp tục, Tạm giữ hoặc Dừng | EL-002 | Người dùng cần cơ hội, rủi ro và khoảng trống thông tin gắn với quyết định |
| UD-03 | Ở screening, false negative nguy hiểm hơn false positive; thiếu dữ liệu không tự động dẫn đến Dừng | EL-002, EL-003, EL-004 | Full diligence còn cơ hội loại bỏ game yếu; bỏ lỡ cơ hội tốt khó phục hồi hơn, nhưng cần tránh lãng phí nguồn lực |
| UD-04 | Chọn Evidence-centered hybrid | EL-003 | AI cần giảm thời gian thu thập/tổng hợp, nhưng người dùng phải kiểm tra được claim ảnh hưởng quyết định, nguồn yếu và mâu thuẫn |
| UD-05 | AI đề xuất; Publishing hoặc Strategy Lead quyết định cuối, có thể override và ghi lý do | EL-003 | AI thiếu ngân sách, chiến lược và nguồn lực nội bộ; override tăng minh bạch và tạo dữ liệu cải thiện hệ thống |
| UD-06 | MVP dùng một game mobile cho thị trường Việt Nam | EL-003, EL-004 | Ba ngày phù hợp để chứng minh quy trình end to end, không phù hợp để chứng minh dự báo hay tổng quát hóa |
| UD-07 | Dùng hard gate + evidence gate + đánh giá có cấu trúc, chưa dùng trọng số | EL-004 | Trọng số chưa có dữ liệu hiệu chỉnh tạo cảm giác khách quan giả; hard blocker phải có bằng chứng |
| UD-08 | Tạm giữ phải nêu thiếu gì, tầm quan trọng, nơi tìm và điểm tái quyết định | EL-004 | Một lời khuyên nghiên cứu thêm không đủ hữu ích và Hold không được kéo dài vô thời hạn |
| UD-09 | Chọn MABINOGI MOBILE sau khi xem shortlist do AI đề xuất | EL-005 | Case có nhiều loại nguồn và căng thẳng giữa launch strength, rating và sustainability; phù hợp để kiểm tra reasoning |
| UD-10 | Tách Vietnam market potential khỏi khả năng Gamota tham gia phát hành | EL-005 | Thành công Hàn Quốc không thể suy rộng sang Việt Nam; game tốt vẫn có thể không tạo cơ hội kinh doanh cho Gamota |
| UD-11 | Cutoff bằng chứng là 07:00 ICT ngày 09/10/2026 | EL-005 | Không dùng dữ liệu tương lai để củng cố nhận định trước cutoff; launch Nhật quá mới để suy luận dài hạn |
| UD-12 | Khuyến nghị sơ bộ cho case là Tạm giữ với targeted validation | EL-006 | Chưa đủ cơ sở cho full diligence hoặc loại bỏ; cần nêu knowns, unknowns và tầm quan trọng |
| UD-13 | Ưu tiên rights check nhưng tiếp tục Vietnam-fit research song song | EL-006 | Rights có thể trở thành blocker, nhưng chưa có phản hồi không đồng nghĩa không có cơ hội |
| UD-14 | Day 2 và một lần gia hạn Hold chỉ là quy tắc thử nghiệm MVP | EL-006 | Timebox thực tế phụ thuộc loại thông tin và khả năng tiếp cận nguồn |
| UD-15 | MABINOGI MOBILE là case minh họa, không phải toàn bộ phạm vi sản phẩm | EL-006 | Bài nộp phải tập trung vào thiết kế sản phẩm tổng quát, không sa đà vào một game |

## Phần AI hỗ trợ nhưng không phải quyết định của người dùng

| ID | Hỗ trợ của AI | Trạng thái |
|---|---|---|
| AI-01 | Đề xuất ba problem framing và nghiêng về sàng lọc cơ hội phát hành | Người dùng tự chọn phương án A và đưa lý do ở EL-002 |
| AI-02 | Đề xuất luồng evidence-centered, Claim Ledger, Conflict Card và tách confidence khỏi recommendation | Một số nguyên tắc được người dùng xác nhận; chi tiết kiến trúc và cách diễn đạt vẫn là AI synthesis |
| AI-03 | Đề xuất điều kiện Continue Hold Stop và timebox Day 2 | Người dùng xác nhận logic; giới hạn Day 2 được xác nhận chỉ ở vai trò thử nghiệm MVP |
| AI-04 | Nghiên cứu shortlist gồm MABINOGI MOBILE, Dungeon&Fighter Mobile và Roco Kingdom | Người dùng chọn MABINOGI MOBILE sau khi xem shortlist; không phải tự phát hiện game |
| AI-05 | Tìm nguồn, lập Research Brief và Claim Ledger, đề xuất sơ bộ Hold targeted validation | Người dùng xác nhận trạng thái Hold ở EL-006; các claim/inference vẫn giữ provenance riêng |
| AI-06 | Viết kiến trúc năm lớp, kế hoạch MVP, phương pháp đánh giá, ba Forced Decisions và tạo DOCX/PDF | Đang chờ người dùng kiểm tra lần cuối; không được xem là trải nghiệm hay kết quả thử nghiệm do người dùng tự thực hiện |

## Những gì vẫn chưa được kiểm chứng

- Chưa phỏng vấn Publishing hoặc Strategy Lead của Gamota; problem framing là lựa chọn của người tham gia bài test, chưa phải user research đã xác thực.
- Chưa có dữ liệu nội bộ về quy trình hiện tại, thời gian nghiên cứu, ngân sách, strategic priority, capacity, acquisition cost, retention hoặc unit economics.
- Chưa liên hệ hoặc nhận xác nhận từ Nexon về quyền Việt Nam, partner willingness hay mô hình self-publish, license hoặc co-publish.
- Chưa truy cập bản đầy đủ của Vietnam Mobile Gaming Year-in-Review 2025; bản thảo chỉ dùng nội dung trên trang summary của Gamota.
- Chưa thực hiện social listening, survey, concept test hoặc review coding có hệ thống cho MABINOGI MOBILE tại Việt Nam.
- Chưa thử MVP với reviewer thực tế; các tiêu chí đánh giá là phương pháp dự kiến, không phải kết quả đã đạt.
- Chưa xác minh yêu cầu Mission 1, hạn nộp và tiêu chí chấm từ nguồn chương trình độc lập; các mục này vẫn dựa trên thông tin người dùng cung cấp.

## Trạng thái bàn giao

- Bản thảo DOCX và PDF đã được tạo, render và kiểm tra; PDF có đúng 5 trang.
- Evidence Log đã tổng hợp prompt thực tế trong cuộc trò chuyện Work, quyết định người dùng, hỗ trợ AI, nguồn và các khoảng trống chưa kiểm chứng.
- `PENDING`: người dùng kiểm tra lần cuối và tự thực hiện nộp bài.
