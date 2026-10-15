# Khảo sát sản phẩm tham chiếu cho MVP Mission 2

Khảo sát ngày 2026-10-15, dựa trên tài liệu công khai của chính các nhà cung cấp; chưa dùng thử các gói dữ liệu trả phí. Mục đích là chọn cách cải thiện vòng **câu hỏi → nguồn → nhận định có căn cứ → người dùng kiểm chứng**, không sao chép độ phủ dữ liệu của các nền tảng thương mại.

| Sản phẩm | Điều họ công bố | Bài học áp dụng cho Gamota |
|---|---|---|
| [Sensor Tower Game IQ](https://sensortower.com/product/mobile-app/game-iq) | Phân loại mobile game theo subgenre, chủ đề, cơ chế kiếm tiền; lọc ước tính lượt tải/doanh thu theo kỳ, quốc gia và thiết bị trên App Store/Google Play. | Khóa rõ game, thị trường, kỳ, chỉ số và nền tảng trước khi so sánh. Mỗi số liệu phải mang nhãn **ước tính** và phạm vi đo. |
| [AppMagic](https://appmagic.rocks/) và [mô tả cách thu dữ liệu](https://appmagic.rocks/articles/how-appmagic-collects-your-data?hl=en) | Công cụ tìm/so sánh game và app; AppMagic nói các chỉ số dùng trong mô hình có độ phủ nền tảng khác nhau: revenue/download cả Android và iOS, iOS retention, Android DAU/MAU. [Báo cáo 2026](https://appmagic.rocks/files/view/upload/Reports/EN_MobileMarkeLandscape2026.pdf) ghi rõ ước tính, phạm vi store và giới hạn D2C. | Hiện rõ **định nghĩa và phạm vi chỉ số**: chỉ số là gì, dữ liệu đo hay ước tính, store/kênh nào, vùng/kỳ nào, điều gì bị bỏ ngoài. Không suy doanh thu toàn game từ IAP store. |
| [Newzoo Game Performance Monitor](https://newzoo.com/products/game-performance-monitor) | Theo dõi engagement/doanh thu và benchmark theo game, thị trường, taxonomy cho **PC/console**. | Lấy ý tưởng đặt game bên cạnh đối thủ cùng phân khúc, nhưng chỉ sau khi đã có dữ liệu so sánh cùng định nghĩa. Newzoo không phải nguồn dữ liệu mobile trực tiếp cho case Liên Quân. |
| [Gemini Notebook](https://support.google.com/gemininotebook/answer/16179559?hl=en) | Người dùng chọn nguồn để hỏi; trích dẫn có thể xem đoạn trích và mở đúng ngữ cảnh. | Cho người dùng duyệt danh sách nguồn trước extraction; từ từng câu nhận định mở được ngay quote và trang gốc. |
| [Elicit Systematic Review](https://elicit.com/solutions/literature-review) | Sàng lọc tài liệu với lý do loại, đánh giá theo tiêu chí, liên kết phần trích xuất với quote/figure gốc. | Lưu lý do nguồn bị loại: không đọc được, sai thời gian, sai thị trường, thiếu phương pháp. Đưa provenance vào báo cáo thay vì chỉ báo lỗi kỹ thuật. Đây là mẫu quy trình nghiên cứu, không phải nguồn game data. |
| [AlphaSense Generative Search](https://help.alpha-sense.com/hc/en-us/articles/41666587181203-Interacting-with-Generative-Search) | Trả lời câu hỏi kinh doanh với research plan, kết luận ngắn, citation trực tiếp tới đoạn nguồn được tô sáng và câu hỏi tiếp theo. | Đưa câu trả lời ngắn lên đầu, mỗi ý gắn chứng cứ kiểm tra được; nếu thiếu chứng cứ, nêu chính xác phần chưa thể kết luận và nguồn cần tìm tiếp. |

## Khoảng trống hiện tại của MVP

MVP đã có tiêu chí câu hỏi, URL nguồn do người dùng cung cấp, quality/relevance riêng, claim ledger, review từng claim và xuất JSON/brief. Vì vậy, không cần xây lại các cơ chế này. Các lượt live trước vẫn partial: có nguồn không đọc được, claim đúng chữ nhưng sai nghĩa hoặc sai phạm vi, và chưa có brief live được người dùng chấp nhận. [Kiểm toán Mission 2](acceptance-gap-audit.md) và [báo cáo kiểm thử](test-report.md) ghi bằng chứng cụ thể. Khảo sát trên gợi ý cải thiện **đường đi từ nguồn được chọn đến câu kết luận được duyệt**, thay vì thêm dashboard chỉ số.

## Thứ tự cải thiện đề xuất

| Ưu tiên | Thay đổi MVP | Vì sao / tiêu chí nghiệm thu |
|---|---|---|
| P0 | **Thẻ phạm vi cho từng metric và nguồn**: game, quốc gia, khoảng ngày, đơn vị, measured/reported/estimated, store/kênh, phạm vi bị loại. Cho reviewer sửa hoặc đánh dấu unknown. | Case Liên Quân đã trượt từ “thành công” sang “đứng đầu doanh thu”; app phải phân biệt engagement Tết với doanh thu cả Q1 và không coi app-store IAP là mọi kênh. Nghiệm thu: báo cáo không đưa ra kết luận rộng hơn các thẻ phạm vi. |
| P0 | **Sàng lọc nguồn trước extraction** cho chế độ Gemini tự tìm: hiển thị title/URL cuối/ngày/độ dài nội dung/trạng thái đọc; người dùng chọn tối đa vài nguồn hoặc thay URL; lưu lý do loại. | Đưa nguồn lỗi/nav-only ra khỏi prompt trước khi tốn extraction call. Nghiệm thu: nguồn được dùng đều có nội dung đọc được, và run lưu được vì sao nguồn khác bị loại. Một lần tìm nguồn vẫn dùng API; bước chọn nguồn không cần gọi Gemini. |
| P0 | **Câu trả lời theo từng luận điểm có dẫn chứng ngay cạnh**: mỗi câu nối tới claim đã duyệt, quote, nguồn gốc, phạm vi và giới hạn; dòng “chưa biết” riêng. | Người review không phải tự nối Claim ID với đoạn trích ở nhiều expander. Nghiệm thu: người khác mở run JSON/brief có thể đi từ từng kết luận tới văn bản nguồn và thấy rõ điều nguồn *không* chứng minh. |
| P1 | **Nhóm nguồn phụ thuộc và đối chiếu số liệu cùng định nghĩa**: bài đăng lại cùng thông cáo chỉ tính một gốc; số liệu khác kỳ/kênh không gọi là mâu thuẫn trực tiếp. | Tránh đếm lại cùng một bằng chứng và so sánh sai mẫu. Nghiệm thu: các case repost, Q1 vs sự kiện Tết, IAP vs web recharge được gắn nhãn đúng. |
| Sau MVP | Benchmark nhiều game, live-ops calendar, theo dõi liên tục, bộ dữ liệu ước tính/licensed. | Có thể hữu ích cho sản phẩm dài hạn, nhưng không kiểm chứng được core loop Mission 2 khi nguồn/nhận định live còn yếu. |

## Phép thử nhỏ cho lần cải thiện kế tiếp

1. Dùng lại các run T01–T03 đã lưu, **không gọi Gemini**, để kiểm tra giao diện thẻ phạm vi, lý do loại nguồn và đường dẫn kết luận → quote. Dùng phản hồi Liên Quân người dùng đã cung cấp làm ca kiểm tra phạm vi; chỉ replay trên UI nếu có run JSON. Ghi expected/actual cho ít nhất một claim đúng, một claim sai nghĩa và một nguồn không đọc được.
2. Khi có giới hạn API mới được chủ key xác nhận, chạy [hai câu hỏi thật đã chốt](mvp-live-acceptance-plan.md) trên cùng pipeline. Reviewer kiểm tra các câu ảnh hưởng kết luận và duyệt/sửa brief; chỉ gọi PASS nếu cả nguồn lẫn nhận định đúng phạm vi.
3. Báo cáo riêng tỷ lệ nguồn đọc được, claim qua kiểm tra cơ học, claim được người duyệt, và số câu trả lời hữu ích. Số test code đạt không thay cho chất lượng nghiên cứu.
