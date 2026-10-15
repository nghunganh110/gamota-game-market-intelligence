# T02 — Game thứ hai, China, nguồn thật

**Trạng thái:** partial; chưa đạt chất lượng end-to-end; AI audit, chưa human verification.

Artifact: `runs/a4f15d87-1b8f-41c5-9f01-dbb048483c95/run.json`. Internal ID: `cbf694e6-7821-4895-9f61-4dde7b614bc7`.

## Kỳ vọng → Thực tế → Đạt/Chưa đạt → Điều học được

**Kỳ vọng:** cùng pipeline xử lý Dungeon & Fighter Mobile ở China trong tháng 5–6/2024; tách company reporting, chart observations và estimates; không ngoại suy Vietnam demand hoặc quyền Gamota.

**Thực tế:** 2 API attempts; 4 reported search queries; 83.657 giây. Response total tokens lần lượt 4,633 và 18,323. Đọc được 5 nguồn với URL/content khác nhau, gồm Nexon prepared remarks, Tencent earnings release, SCMP và 2 bài Game World Observer. Không còn tình huống chỉ có navigation trong run này. PDF publication dates vẫn unknown; strict_cutoff=false nên không tự loại vì thiếu metadata ngày. Không có bằng chứng snapshot lịch sử.

10 claim được tạo: **6 mechanically checked, 4 rejected** do khoảng đo vượt scope; cả 10 quote khớp cơ học. 4/5 findings bị loại vì phụ thuộc claim không hợp lệ; một finding được giữ. Research dimensions/blockers rỗng, không có recommendation. Chi phí tiền tệ chưa xác định.

**Đạt về hành vi kỹ thuật:** discovery, PDF/HTML reading, structured extraction, scope gate và dependency gate chạy trên game/thị trường khác. Không hard-code MABINOGI MOBILE. Không đủ cơ sở nói search prompt đã cải thiện ổn định chỉ từ một run.

**Chưa đạt chất lượng nghiên cứu:** semantic audit phát hiện claim trộn kỳ/phạm vi, diễn giải gross/net quá chắc và generalization về rights/Vietnam trong proposed output. Số claim nhiều hoặc mechanically checked không chứng minh chất lượng brief.

**Điều học được:** quarterly reporting là nguồn bối cảnh hữu ích nhưng không tự trở thành số liệu hai tháng. Không nới scope hoặc đổi period của claim chỉ để làm test PASS. Có thể cần phân biệt evidence hỗ trợ trực tiếp và context trong thiết kế tiếp theo, nhưng vẫn phải bảo vệ phạm vi kết luận.

## AI audit theo claim

| Claim | Gate | Nhận xét |
|---|---|---|
| CLM-S1-01 | Qua | Quote chứa ngày launch và thành tích hơn 11 tuần, vượt tháng 6. Text bổ sung tăng trưởng doanh thu franchise cả Q2 từ chỗ khác của PDF nhưng gắn bounds May–June. Cần tách launch date, chart duration và quarterly franchise context; không giữ nguyên composite claim. |
| CLM-S1-02 | Loại | Q2 bắt đầu tháng 4, ngoài scope. Giữ nguyên kỳ quý dưới nhãn context; không gọi franchise revenue là standalone game revenue. |
| CLM-S2-01 | Loại | Tổng doanh thu Domestic Games Q2 không phải doanh thu riêng game hoặc chỉ tháng 5–6. Gate bảo thủ phù hợp; có thể đọc làm context với nhãn rõ. |
| CLM-S2-02 | Loại | Management assessment gắn Q2. Không suy ra retention định lượng hay hiệu quả dài hạn. |
| CLM-S3-01 | Qua | Snapshot hỗ trợ vị trí chart vào thứ Tư sau launch; không tự chứng minh giữ hạng cả hai ngày. Cần gắn attribution “SCMP reported” thay vì như app tự quan sát storefront. |
| CLM-S4-01 | Qua | Bài thứ cấp thuật lại Bloomberg dẫn Sensor Tower; giữ đủ attribution chain. Không coi là nguồn Sensor Tower gốc. Kỳ “first week” là mô tả của báo, cần thận trọng ngày chốt chính xác. |
| CLM-S4-02 | Qua | Ước tính Niko được bài thứ cấp dẫn; iOS+Android là phạm vi store, không tự bao gồm PC. Không biến estimates thành company revenue. |
| CLM-S4-03 | Qua | Quote chứa IAP definition và số downloads, nhưng limitations diễn giải thuế thành “after applicable taxes” trong khi wording nguồn không tương đương. Không đồng nhất IAP estimate với audited publisher net receipts. |
| CLM-S5-01 | Qua | Nguồn thứ cấp báo first-month estimate; ngày kết thúc 21/6 do model suy từ launch, không phải ngày chốt công bố chính xác. |
| CLM-S5-02 | Loại | Bounds kéo tới 8/7; không dùng tổng tích lũy này để khẳng định kết quả tới 30/6. Không thay end date bằng June để qua gate. |

## Findings và quyền phát hành

Finding được giữ trộn các số iOS IAP estimate, iOS consumer spending và iOS+Android spending. Không trình bày chúng như lower/upper bounds của cùng một đại lượng. Bản viết thận trọng nên tách thành các chỉ số khác nhau, ghi source/attribution và không so như-for-like.

Proposed finding “zero evidence in public disclosures” về Gamota quá rộng: một lần tìm kiếm không chứng minh không có bằng chứng công khai ở mọi nơi. Cách viết phù hợp: **các nguồn đã thu thập trong run này chưa xác nhận quyền phát hành Gamota tại Việt Nam; trạng thái unknown**. Finding này bị gate loại do phụ thuộc claim ngoài scope, không phải vì validator hiểu và phát hiện lỗi absence-of-evidence. Không được coi đó là semantic safety đã đạt.

Proposed Vietnam-transferability finding trộn hiểu biết về lịch sử IP, distribution và quan hệ nhân quả; những chi tiết không được các claim hợp lệ bao phủ cần chuyển thành giả thuyết/next validation, không phải kết luận chắc chắn.

Gaps nêu Vietnam demand, rights và breakdown là hợp lý về hướng nghiên cứu; owner/deadline do model đặt là đề xuất. Các revisit dates 2024/2025 đã nằm trong quá khứ so với ngày chạy năm 2026, không phải lịch hành động đã được thống nhất.

## Phạm vi kiểm chứng

Đã đọc captured source text và đối chiếu quotes với snapshots, không mở web hoặc fetch lại nguồn trong phiên audit này. Không có API call mới. Không sửa artifact, không gán human_verified. Nguồn thứ cấp cùng dẫn dữ liệu analytics không tự là nhiều phép đo độc lập; 5 unique documents không có nghĩa 5 independent measurement systems.

## Bước tiếp theo

Giữ T02 là actual partial với cả hành vi tốt và lỗi đã quan sát. Chuyển T03, câu hỏi thể loại Mobile MMORPG ở Vietnam trong năm 2025. Không lặp T02 chỉ để tăng tỷ lệ PASS. T03 phải giữ khác biệt genre-specific so với whole-market context và Vietnam so với regional aggregates. Chưa chạy T03; dùng scope đã chuẩn bị.
