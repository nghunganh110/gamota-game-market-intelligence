# T03 — Câu hỏi thể loại tại Việt Nam

**Trạng thái:** partial; có một nhận định định tính truy vết được, chưa đủ kết luận cơ hội đầu tư; AI audit, human review pending.

## Thực thi và giới hạn sử dụng

Root `.env` được đọc bằng loader; preflight báo ready mà không in giá trị key. Không sửa hoặc công bố secret.

Lần đầu trong sandbox: `runs/36aaf481-49d5-4082-9cf5-43495c3191b9/`, failed, ConnectError, 1 local API attempt reservation, 0 response usage entries, 0 nguồn, 0 claim, 0.379 giây. Không xác định phía server có nhận request hay không; không gọi đây là một research result hoặc khẳng định phí bằng không.

Đã yêu cầu quyền chạy lại ngoài sandbox, nêu rõ tối đa **2 attempts mới**. Sau khi được phép, chạy một lượt và không tự retry tiếp.

Artifact kết quả: `runs/e747a968-3a3a-4b62-b152-0d8e4d85f895/run.json`; internal ID `fe2ca847-3814-4844-9606-120810b242b7`. Live, 2 API attempts, 4 reported search queries, 56.477 giây. Response total tokens 4,833 và 5,796. Cost và billable search units chưa xác định.

## Kỳ vọng → Thực tế → Đạt/Chưa đạt → Điều học được

**Kỳ vọng:** nghiên cứu Mobile MMORPG tại Vietnam trong năm 2025; không dùng whole-market hoặc regional aggregates thay số riêng thể loại; không giấu thiếu dữ liệu.

**Thực tế:** tìm 6 nguồn, chỉ 2 nguồn đọc được. Bốn nguồn lỗi HTTPStatusError hoặc ValueError; chưa lưu đủ chi tiết để kết luận riêng từng lỗi là JS, paywall, redirect hay extraction. Nguồn đọc được là summary báo cáo Gamota và corporate release VNG. Model sinh 5 claims, 1 mechanically checked và 4 rejected vì subject mismatch/indirect relevance. Ba findings phụ thuộc bị loại; một finding còn lại. Research không có dimensions hoặc recommendation.

**Đạt về thành phần:** pipeline nhận câu hỏi thể loại, đọc nguồn Việt, phân biệt chất lượng nguồn với relevance, giữ market-wide/company-portfolio data ngoài bằng chứng trực tiếp cho MMORPG. Gaps chỉ ra thiếu số riêng thể loại.

**Chưa đạt về coverage:** chỉ có một nguồn publisher summary trực tiếp hỗ trợ nhận định định tính. Chưa có full report, quantitative genre split hay independent corroboration. Không thể suy cơ hội game cụ thể, dự báo tăng trưởng hoặc khả năng sinh lời từ run này. Human acceptance chưa thực hiện.

**Điều học được:** genre research khác single-game research; nguồn uy tín/đúng thị trường vẫn có thể sai đơn vị phân tích. Không tìm được dữ liệu trong run không chứng minh dữ liệu không tồn tại. Chất lượng retrieval/reader vẫn là hạn chế lớn.

## AI audit theo claim

| Claim | Gate | Rà soát nội dung |
|---|---|---|
| C1 | Loại | Số toàn thị trường và người chơi không phải số riêng MMORPG; có thể là bối cảnh, không phải genre evidence. Không đổi subject thành MMORPG để qua gate. |
| C2 | Qua | Summary Gamota mô tả nhóm MMORPG, 4X và Team Battle cùng nắm phần lớn doanh thu. Không được diễn giải MMORPG một mình có majority share. Nội dung là nhận định do Gamota báo cáo, chưa xác minh độc lập phương pháp hoặc tỷ lệ. |
| C3 | Loại | Chủ đề regulation khác genre metric; đoạn nguồn nằm trong mục vận hành 2026, model gán năm 2025 thiếu căn cứ thời gian. Không dùng làm tư vấn pháp lý hay khẳng định pháp luật đã được kiểm chứng. |
| C4 | Loại | Company portfolio bookings không phải Vietnam MMORPG revenue. Số overseas share của toàn tập đoàn không tự xác định phân bổ địa lý riêng mảng game. |
| C5 | Loại | Portfolio paying-user rate không phải genre rate. Claim thêm quarterly user count ngoài quote đính kèm, dù có ở chỗ khác trong nguồn; cần split/quote tương ứng trước khi dùng. |

## Cách viết kết luận thận trọng để người dùng review

“Trong phần tóm tắt báo cáo 2025, Gamota xếp MMORPG cùng 4X và Team Battle vào nhóm thể loại nắm phần lớn doanh thu tại Việt Nam. Đây là tín hiệu định tính từ một nhà phát hành; nguồn đã đọc không cung cấp riêng doanh thu, thị phần hoặc mức tăng trưởng của MMORPG. Vì vậy, bằng chứng hiện tại chỉ hỗ trợ tiếp tục kiểm chứng giả thuyết, chưa đủ để định lượng cơ hội hoặc khuyến nghị đầu tư.”

Đây là **bản diễn đạt do AI sửa**, không thay finding gốc hoặc gán human_verified. Câu gốc “allocations were not published” quá rộng nếu hiểu là mọi nơi; chỉ có thể nói phần tài liệu đã đọc không cung cấp các số đó. Gaps owners/revisit dates do model tạo là đề xuất, không phải việc đã giao.

## Nguồn và phạm vi audit

Đã đọc snapshots Gamota và các đoạn liên quan của VNG, đối chiếu các claim/quote. Không gọi model hoặc tìm nguồn bổ sung trong audit này. Nguồn trực tiếp là summary report, không phải bản report đầy đủ. Nhận định “audited” về corporate release không chứng minh tất cả operational metrics đều được kiểm toán riêng.

Nguồn summary được lưu: https://gamota.com/gamota-lab/reports/gamota-releases-vietnam-mobile-gaming-year-in-review-2025-report-revenue-reaches-825-million/

## Tiến độ kế hoạch

T01/T02/T03 đều đã được chạy ít nhất một lượt full pipeline; thêm diagnostic snapshot extraction. Yêu cầu ba câu hỏi theo kế hoạch đã **thực thi**, nhưng acceptance chất lượng chưa hoàn tất. Các case có failure evidence thật, không phải synthetic thay thế. Tiếp theo ưu tiên người dùng review nhận định/claim trọng yếu và xử lý giới hạn ngữ nghĩa/retrieval. T06/T09 và bài nộp cuối vẫn chưa hoàn tất. Dừng gọi thêm model sau lượt đã được phép.
