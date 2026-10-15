# Mission 2 — kiểm thử MVP hiện tại

Ngày cập nhật: 2026-10-15. **Phần mềm đã có đủ luồng nghiên cứu và review để thử nghiệm; giả thuyết về chất lượng nghiên cứu live chưa được xác nhận.** Lần cập nhật này không gọi Gemini. Bộ test phần mềm: **72 passed** (`.venv/bin/python -m pytest -q`). Con số này không đo độ đúng của nhận định thị trường.

Core loop trong app: câu hỏi và tiêu chí → Gemini tìm URL **hoặc** người dùng cung cấp 1–6 URL → đọc HTML/PDF → Gemini đề xuất claim/finding → kiểm tra quote, game, market, kỳ đo, cutoff → hiển thị chất lượng và độ phù hợp của từng nguồn → người review kiểm tra ý nghĩa claim → viết nhận định cuối với claim đã duyệt → tải brief/JSON. JSON có thể mở lại để tiếp tục review.

## Kỳ vọng → thực tế → đánh giá → bài học

| Case | Kỳ vọng | Thực tế quan sát | Đánh giá | Bài học |
|---|---|---|---|---|
| O01, synthetic good | Nguồn/claim đủ → kết luận sàng lọc và ledger | `completed`, đề xuất Tiếp tục, 3 claim qua kiểm tra cơ học | **Đạt luồng phần mềm**, không phải bằng chứng thị trường | Cần chạy cùng luồng với nguồn thật |
| O02, synthetic câu hỏi khác | Game Beta/China trong research không dùng logic MABINOGI | `completed`, không ép recommendation | **Đạt luồng phần mềm** | Code không hard-code một game; chưa đo chất lượng Gemini |
| O03/O04, synthetic khó | Mâu thuẫn hoặc thiếu D30 retention phải hiện rõ | Mâu thuẫn giữ hai phía; thiếu D30 → `partial`, gap, không thay bằng doanh thu | **Đạt hành vi bảo thủ** | Không được biến thiếu số liệu thành kết luận chắc chắn |
| O08, synthetic lỗi ngữ nghĩa | Quote phủ định phải chặn claim khẳng định | Quote matching vẫn cho claim sai qua kiểm tra cơ học | **Chưa đạt tự động** | Bắt buộc review ngữ nghĩa; bản mới cho reviewer bác claim và viết nhận định cuối |
| T01 MABINOGI MOBILE, live cũ | Nguồn thật hỗ trợ launch strength và giới hạn metric | Một lượt có 0/5, một lượt 0/0; replay snapshot 5/6 qua cơ học nhưng còn suy luận nhân quả quá mức | **Chưa đạt research acceptance** | Retrieval và diễn giải chưa đủ tin cậy; [chi tiết](live-T01-extraction-review.md) |
| T02 Dungeon & Fighter Mobile, live cũ | Cùng pipeline xử lý game/market khác, tách báo cáo và ước tính | 6/10 claim qua cơ học, còn trộn kỳ/chỉ số; `partial` | **Chưa đạt research acceptance** | Cần thận trọng với dữ liệu quý và số riêng game; [chi tiết](live-T02-review.md) |
| T03 Mobile MMORPG Vietnam, live cũ | Nhận định đúng đơn vị thể loại, chỉ ra phần thiếu | 2/6 nguồn đọc được, 1/5 claim qua cơ học; tín hiệu định tính hẹp, `partial` | **Một phần** | Nguồn uy tín nhưng sai đơn vị phân tích không được tính trực tiếp; [chi tiết](live-T03-review.md) |
| Liên Quân Mobile, online do người dùng báo | Câu hỏi “thành công” phải có tiêu chí, kỳ và subject nhất quán | Trước bản sửa: MOBA thay tên game; ngày Q1 và ô Oct–Dec chỉ mâu thuẫn nếu đã bật nhập ngày thủ công (không rõ); 0/5 claim hợp lệ và 3 nguồn lỗi | **Chưa đạt** | Bản mới chặn câu hỏi đánh giá thiếu tiêu chí và cho nhập URL nguồn; chưa có rerun |
| Guided URLs, offline mock | Không tốn call tìm kiếm; nguồn hỏng vẫn hiển thị; chỉ trích xuất nguồn đọc được | Test bỏ discovery, trích xuất nguồn đọc được trong một lần; nếu tất cả URL hỏng thì 0 model calls | **Đạt kỹ thuật**, chưa có live run | Cần thử bằng URL thật và Gemini thực tế |
| Human-reviewed answer, offline UI | Chỉ dẫn claim đã kiểm tra ngữ nghĩa; sửa nguồn phải vô hiệu kết luận cũ | AppTest và unit test qua; export/JSON giữ kết luận; sửa source hủy review hiện hành | **Đạt kỹ thuật**, chưa có human acceptance nguồn thật | Review là một hành động có trách nhiệm, không phải quote match |

Artifacts O01–O08 ở [offline results](test-artifacts/offline-current/offline-results.md); báo cáo cũ giữ tại [lịch sử kiểm thử](test-report-history.md). Live artifacts T01–T03 nằm trong `runs/` local và không được public vì chứa snapshot toàn văn của nguồn.

## Phép thử còn cần để xác nhận giả thuyết

Chạy bản online mới trên ít nhất **hai câu hỏi thật khác nhau**: một câu có nguồn trực tiếp đủ cho nhận định hẹp, một câu thiếu hoặc mâu thuẫn nguồn. Trước mỗi lượt ghi câu hỏi, tiêu chí, market, kỳ và kết quả mong đợi. Lưu JSON, mở lại, kiểm tra ít nhất các claim ảnh hưởng kết luận với trang gốc, rồi ghi actual, verdict và lý do. Một câu trả lời `partial` vẫn có thể hữu ích nếu nêu đúng phát hiện có nguồn và giới hạn; không được gọi “đạt” chỉ vì pipeline chạy xong.

Người dùng/chủ đề tài là người xác nhận cuối. Chưa có xác nhận đó trên bản mới; video và Forced Decisions cần cập nhật theo hai lượt thực tế này.
