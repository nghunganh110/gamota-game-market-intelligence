# A01/A02 — kiểm thử Gemini trên MVP mới (2026-10-15)

Người dùng cho phép tối đa 4 Gemini API attempts theo [kế hoạch đã chốt](mvp-live-acceptance-plan.md). Đã dùng **3 attempts có response hoặc ServerError**; còn **1 chưa dùng**. Không tự retry sau lỗi ServerError. Một lượt A01 trong sandbox lỗi DNS ở cả hai URL, dừng trước Gemini nên không tính API attempt. Các artifact `runs/` chỉ ở local vì có snapshot nội dung nguồn; không public toàn văn.

| Case | Artifact local | Calls mới | Expected → actual | Đánh giá |
|---|---|---:|---|---|
| A01, URL đã chọn | `runs/565fe68c-2460-4abb-8eea-b24ceeef6768/` | 1 | Hai nguồn đọc được; 6/6 claim qua gate cơ học, 5 findings, pipeline `completed`. Câu trả lời đề xuất có số liệu tải, doanh thu và người dùng tháng 4. | **Thành công kỹ thuật, human audit chưa hoàn tất**. Có claim diễn giải mạnh hơn quote; chưa gọi research acceptance PASS. |
| A02, Gemini tự tìm nguồn | `runs/613f0767-ac41-4a5e-832a-1f8fb439a910/` | 1 | Search call trả `ServerError`; 0 nguồn, 0 claim, pipeline `failed`. | **FAIL discovery**. Không thử lại tự động. |
| A02, URL Gamota đã chọn | `runs/830a2780-6fcb-4877-a2ee-2330023abdea/` | 1 | Nguồn đọc được; ban đầu 0/3 claim qua gate vì `Subject mismatch`, pipeline `partial`. | **Một phần**. Nguồn chỉ nói MMORPG cùng 4X/Team Battle thuộc nhóm chủ lực, không có số riêng MMORPG. |
| A02, áp lại gate đã sửa | `runs/eae583f4-2cf1-4cee-a41e-9054faae4cc4/` | 0 | C2 qua gate cơ học; C1 số toàn thị trường và C3 pháp lý vẫn bị loại. Một finding còn lại nói thiếu doanh thu riêng MMORPG. | **Một phần, replay**. Không phải lần trích xuất Gemini mới hay bằng chứng độc lập. |

## Audit nội dung cần người review quyết định

**A01:** [Sensor Tower](https://sensortower.com/ko/blog/Mabinogi-Mobile-achieves-cumulative-revenue-of-30-million) ghi ước tính hơn 1 triệu lượt tải và khoảng 30 triệu USD doanh thu kể từ ra mắt đến bài đăng ngày 20/05/2025; bài cũng nêu hạng 1 lượt tải, hạng 2 doanh thu. Phương pháp ở cuối bài giới hạn App Store/Google Play và loại chợ Android bên thứ ba. [Mobile Index](https://www.mobileindex.com/home/blog/post/mobilegame_chart_2504) ghi 1,24 triệu người dùng và 26,9 tỷ KRW doanh thu tháng 4/2025, lần lượt hạng 5 và 4 trong các bảng của họ. Đây là **số do hai nhà cung cấp dữ liệu công bố**, chưa phải dữ liệu tài chính đã kiểm toán hay chứng minh nhu cầu ở Việt Nam.

- C1: quote chỉ nêu hơn 1 triệu lượt tải; hạng 1 nằm ở câu kế tiếp trong nguồn. Cần mở nguồn khi review hoặc thu hẹp claim về lượt tải.
- C2/C6: nguồn nói `매출`/`doanh thu`, không định nghĩa rõ `gross revenue` như nhãn AI dùng. Cần bỏ `gross` hoặc xác minh phương pháp trước khi duyệt.
- C3: quote hỗ trợ tỷ trọng 52,8%; nguồn cũng nói thứ hạng Nexon tăng sau ra mắt, nhưng từ `lifting/propelling` hàm ý quan hệ nhân quả mạnh hơn đoạn quote.
- C4: tỷ lệ 64,4% organic và 18,2% paid nằm trong quote; giải thích bằng sức mạnh IP là diễn giải của Sensor Tower, cần gắn attribution.
- C5: nguồn ghi 1,24 triệu `người dùng` trong bảng tháng 4, chưa công bố định nghĩa MAU/active user trong văn bản đọc được. Nên diễn đạt là “người dùng theo bảng tháng 4 của Mobile Index”.

**A02:** [Bài giới thiệu báo cáo của Gamota](https://gamota.com/gamota-lab/reports/gamota-releases-vietnam-mobile-gaming-year-in-review-2025-report-revenue-reaches-825-million/) nêu MMORPG, 4X và Team Battle **cùng nhau** thuộc nhóm nắm phần lớn doanh thu; không tách giá trị hay tốc độ tăng của MMORPG. C2 giờ qua gate chủ thể vì claim ghi rõ nhóm gồm `Mobile MMORPG`; điều đó **không** cho phép suy doanh thu riêng thể loại. Finding còn lại của AI nói “public evidence” quá rộng: chỉ có một bài công bố của Gamota trong lượt này. C1 về tổng doanh thu toàn thị trường và C3 về pháp lý không trả lời trực tiếp câu hỏi thể loại. Không dùng bài công bố này làm bằng chứng độc lập về quy mô cơ hội MMORPG.

**Dự thảo nhận định để người review kiểm tra, chưa phải kết luận đã duyệt:**

- A01: “Tại Hàn Quốc, Sensor Tower ước tính MABINOGI MOBILE vượt 1 triệu lượt tải và đạt khoảng 30 triệu USD doanh thu trên App Store/Google Play từ khi phát hành 27/03 đến bài đăng 20/05/2025. Mobile Index báo 1,24 triệu người dùng và 26,9 tỷ KRW doanh thu trong bảng tháng 4/2025. Các số liệu là tín hiệu ra mắt; chưa chứng minh lợi nhuận hay nhu cầu tại Việt Nam.”
- A02: “Bài giới thiệu báo cáo của Gamota nói MMORPG cùng 4X Strategy và Team Battle thuộc nhóm nắm phần lớn doanh thu game mobile Việt Nam năm 2025. Bài không tách số của MMORPG, nên chưa thể lượng hóa quy mô hoặc tốc độ tăng của riêng thể loại này.”

Hai câu dự thảo trên được viết sau khi đọc snapshot nguồn. Chúng **không** thay thế review từng claim trong app; đặc biệt các claim AI có câu chữ rộng hơn nguồn cần được sửa hoặc bác trước khi dùng làm citation của nhận định cuối.

## Thay đổi phần mềm từ phép thử

- Gate chủ thể nhận một chủ thể khi được ghi **nguyên vẹn** trong danh sách phân tách dấu phẩy; vẫn loại tên chỉ chứa chuỗi con hoặc chỉ là toàn thị trường. Gate cơ học không chứng minh ý nghĩa claim.
- Câu trả lời sơ bộ nay hiển thị **từng finding với đúng claim ID của finding đó**, thay cho chỉ finding đầu nhưng liệt kê ID của tất cả findings.
- Bộ test Python: **76 passed**. Đây là kiểm tra phần mềm, không tính là người dùng đã chấp nhận brief thật.

## Kết luận phép thử

Đã có một case live `completed` về mặt pipeline và một case thể loại có gap đúng hướng, nhưng **chưa có brief end-to-end được người review xác nhận**. Để demo trung thực: mở A01 JSON trong app, kiểm tra từng claim ảnh hưởng nhận định và sửa/bác diễn giải vượt quote; sau đó làm tương tự với A02, chỉ kết luận rằng bài Gamota nêu nhóm thể loại mà không tách MMORPG. Màn hình review hiện chưa cho sửa câu chữ claim/metric, nên các claim cần thu hẹp có thể phải bị đánh dấu `unsupported`/`unclear` cho đến khi có cơ chế chỉnh hoặc trích xuất lại. Không dùng attempt còn lại chỉ để thay đổi status.
