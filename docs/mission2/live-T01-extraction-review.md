# T01 — Extraction trên snapshots với model thật

**Artifact:** `runs/c58b7de4-34ca-4903-933d-90af85908e4b/run.json`. Internal run ID: `0de6d76f-539b-4077-8663-8d4a93ca420d`. Parent: `fb2fa171-ae9f-4d9e-96e0-e365c469d67c`, có hash provenance trong usage.

## Kỳ vọng → Thực tế → Đạt/Chưa đạt → Điều học được

**Kỳ vọng:** model tự sinh bounds cho kỳ con, trích quote nguyên văn, Research không sinh Screening dimensions, diễn giải thận trọng trên nguồn hữu ích đã lưu.

**Thực tế:** 1 API call thật, không tìm hoặc tải nguồn mới; 3 snapshots độc lập về URL/content từ lần đầu, 16.279 giây, 8,245 total tokens theo response usage. Tạo 6 claim: 5 mechanically checked, 1 rejected vì quote không liên tục. Không có period mismatch. Dimensions và blocker_claim_ids rỗng. Một trong ba findings bị loại vì phụ thuộc claim rejected; hai findings còn lại được giữ cơ học. Trạng thái partial, evidence_mode=replay, new_model_extraction=true. Chi phí tiền tệ chưa xác định.

**Đạt:** schema khoảng ngày và xử lý kỳ con hoạt động trên output do model thực sự sinh ra; không còn lỗi string equality. Validator chặn quote ghép bằng dấu ba chấm. Research dimensions không còn xuất hiện.

**Chưa đạt:** bộ trích xuất vẫn không luôn trả quote nguyên văn liên tục; một finding còn khẳng định nguyên nhân chênh lệch doanh thu là PC và gọi báo cáo thứ cấp là xác nhận chính thức. Chưa có human audit; chưa chứng minh discovery mới hoặc chất lượng nghiên cứu end-to-end.

**Điều học được:** cải thiện prompt không bảo đảm semantic correctness. Việc claim vượt validation không chứng minh finding suy ra từ claim đó là đúng. Dừng vòng lặp T01 tại đây để giữ failure evidence và kiểm tra tính tổng quát bằng T02 thay vì chạy đến khi có output thuận lợi.

## AI audit theo claim

Các source IDs trong run này đã được đánh lại: S1=Sensor Tower, S2=Mobile Index, S3=Newsis. Không dùng source IDs của run cha để tra mà bỏ qua ánh xạ mới.

| Claim | Kết quả cơ học | Kết quả AI review và sửa cần thiết |
|---|---|---|
| C1 | Qua | Nội dung doanh thu khoảng 50 ngày có trong nguồn; ngày 16/5 là suy ra từ khoảng thời gian xấp xỉ, không phải ngày chốt được công bố. Không coi là exact measurement end. |
| C2 | Qua | Quote hỗ trợ ước tính lượt tải. Ngày chốt 16/5 cũng chưa được xác nhận; giữ khoảng tháng 5 thay vì ngày chính xác. |
| C3 | Loại | Quote nối hai đoạn bằng `...`, không phải substring của snapshot. Giữ validator; cần tách claim xếp hạng và claim tỷ trọng, mỗi claim có quote riêng. Không tự thay quote để biến output model thành PASS. |
| C4 | Qua | Nguồn hỗ trợ người dùng tháng 4 và hạng năm. Nhãn metric MAU, cách ước tính và việc loại PC chưa được giải thích đầy đủ trong bài; giữ giới hạn unknown. |
| C5 | Qua | Số liệu tháng 4 và hạng tư có căn cứ. PC billing exclusion trong limitations chưa được bài chứng minh. |
| C6 | Qua | Newsis thuật lại phát biểu về mốc tháng 5; phải giữ attribution thứ cấp. Phạm vi mobile+PC của mốc tháng 10 không tự xác định breakdown riêng cho mốc tháng 5. |

## AI audit findings và conflict

- Finding đầu bị loại cùng C3: cơ chế chặn dependency hoạt động, nhưng tổng hợp launch traction vẫn cần nhãn inference.
- Finding về số liệu tháng 4 có thể giữ dưới dạng Mobile Index báo cáo; không bổ sung phương pháp/kênh chưa xác minh.
- Finding cuối **chưa đạt ngữ nghĩa**: nguồn thứ cấp không phải official confirmation trực tiếp; sự khác nhau giữa số liệu không chứng minh đóng góp PC. Sửa theo hướng chưa thể đối chiếu định lượng/căn nguyên khi kỳ đo, kênh và accounting chưa tương thích.
- Conflict C1/C6 còn diễn giải causal quá chắc. Different scope chỉ là một khả năng cần xác minh, không phải phép phân rã chênh lệch doanh thu đã được chứng minh.
- Gaps về tháng 6 và breakdown có giá trị. Owner và ngày revisit do model tự sinh vẫn là đề xuất, không phải việc đã giao hoặc deadline người dùng đã chốt.

## Quyết định về bước kiểm chứng tiếp theo

Giữ ba kết quả T01 riêng biệt: live lần đầu (lỗi period gate), live lần hai (discovery chỉ có navigation), extraction snapshots (period gate hoạt động nhưng quote/semantic còn lỗi). Không thay thế run gốc bằng bản sửa AI. Không gán human_verified.

T02 kiểm tra game khác tại China bằng cùng pipeline, không dùng nguồn T01. Kỳ vọng đã thiết kế: tìm evidence thật theo input, tách publisher report/estimate, không suy từ China sang Vietnam hoặc suy quyền Gamota từ app availability. Chưa có kết quả T02. Scope tại `live-T02-scope.json` đã sẵn sàng; một full run tối đa hai API attempts, không retry.
