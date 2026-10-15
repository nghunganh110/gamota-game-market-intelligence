# Kiểm toán lại Mission 2 theo đề gốc

Trạng thái: **chưa đạt giả thuyết cốt lõi**. Bản online đã gọi Gemini và hiện kết quả, nhưng chưa có một lượt nghiên cứu live nào đi hết vòng *câu hỏi → nguồn đọc được → nhận định đúng phạm vi, có dẫn chứng → người dùng kiểm chứng và chấp nhận*. Số test Python đạt đo độ ổn định của code, không đo chất lượng nghiên cứu.

Nguồn đối chiếu: [nguyên văn yêu cầu](mission2-evidence-log.md), [kế hoạch đã duyệt](mission2-technical-plan.md), [tiến độ live](live-test-progress.md), báo cáo T01–T03 và kết quả Liên Quân Mobile do người dùng cung cấp.

| Yêu cầu Mission 2 | Bằng chứng hiện có | Đánh giá |
|---|---|---|
| MVP chạy thực tế | Repo và app Streamlit online do người dùng xác nhận; đã gọi Gemini, sinh claim và lỗi có thể quan sát | **Đạt kỹ thuật một phần**; core loop nghiên cứu chưa đạt |
| Nhiều hơn một câu hỏi | T01–T03 và Liên Quân Mobile khác game/thể loại/thị trường; đều có live run | **Có chạy nhiều câu hỏi**, chưa chứng minh đầu ra hữu ích ổn định |
| Kết luận quan trọng có nguồn kiểm chứng | T01/T02 có claim qua cơ học nhưng AI audit thấy suy luận vượt nguồn; T03 chỉ 1/5; Liên Quân 0/5 hợp lệ; chưa có human-verified brief | **Chưa đạt** |
| Không coi mọi nguồn như nhau | Code tách quality và relevance, chặn scope/cutoff, giữ metadata và review | **Có cơ chế**, đánh giá nguồn trên dữ liệu live chưa được người dùng audit/chấp nhận |
| Hiện thiếu dữ liệu, bất định, mâu thuẫn | App giữ gaps và loại finding sai reference; các lượt partial có lỗi hiển thị | **Đạt một phần**; gap đôi khi trượt sang tiêu chí không được hỏi (Liên Quân: “thành công” bị ngầm hiểu là highest-grossing) |
| Ít nhất 5 test cases thực tế, có tốt/khó/thất bại | 8 case synthetic/fault có actual output; T01–T03 live và Liên Quân là partial/failure | **Chưa đủ bằng chứng sản phẩm** cho một case live làm tốt; cần report tổng hợp kỳ vọng → thực tế → đạt/chưa đạt → bài học, tách rõ synthetic/live |
| Public repo, README, demo, video ≤5 phút, 3 Forced Decisions | Repo/README có; user xác nhận app online nhưng môi trường kiểm tra bị chuyển login; video hiện chỉ là preview offline, script và Forced Decisions là draft cũ | **Bài nộp chưa hoàn tất** |

## Sai hướng cần sửa

1. **Ưu tiên số test và form trước giá trị đầu ra.** Các lượt live hiện chưa trả một decision brief vừa đúng nguồn vừa giúp người phụ trách ra quyết định. Không gọi `mechanically_checked` là “đã kiểm chứng”.
2. **Chưa chốt tiêu chí của câu hỏi trước khi tìm nguồn.** “Game thành công” không xác định thành công theo người chơi, doanh thu, tăng trưởng, retention hay tính phù hợp phát hành. Gemini đã tự trượt sang “highest-grossing”, một câu hỏi khác.
3. **Retrieval chưa đủ tin cậy.** Grounding cho URL redirect; nhiều trang timeout, chặn request, chỉ có navigation hoặc thiếu full text. Không có nguồn đọc được thì schema/UI tốt cũng không tạo được bằng chứng.
4. **Semantic validation chưa giải quyết.** Quote tồn tại trong trang vẫn có thể không hỗ trợ claim hoặc finding. O08 và audit T01/T02 chứng minh lỗi này. Human review phải kiểm tra đúng các claim ảnh hưởng kết luận, không chỉ nhìn số lượng claim.
5. **Nộp bài còn thiếu.** Test report và video script chứa mốc lịch sử; chưa có video cuối và ba Forced Decisions được người dùng rà soát theo kết quả mới.

## Thứ tự phục hồi core loop

1. **Chọn một câu hỏi hẹp làm case chứng minh.** Giữ scope T01 đã định trước: “MABINOGI MOBILE có tín hiệu launch strength nào tại Hàn Quốc trong tháng 3–6/2025?” Tiêu chí là rank/engagement/doanh thu đã được nguồn đo, ghi rõ phần tháng 6 thiếu, không suy Vietnam fit. Giữ T02 làm game thứ hai, Liên Quân làm failure về scope/retrieval.
2. **Audit thủ công evidence đã thu, không gọi Gemini thêm.** Chọn nguồn đọc được và có ngày; với từng claim quyết định, kiểm tra nguyên văn quote, kỳ/market/chỉ số, attribution, rồi sửa hoặc loại finding vượt nguồn. Trình người dùng duyệt một brief cụ thể. Nếu không đủ, ghi case thất bại và tập trung sửa retrieval trước lượt API mới.
3. **Sửa retrieval bằng phép thử nhỏ, không thêm nhiều UI.** Đo tỷ lệ URL Gemini trả về có thể đọc toàn văn và nguồn gốc thực. Dùng snapshots hiện có và fetch không tốn Gemini để kiểm tra redirect/article/PDF; nếu grounding redirect là nút thắt, chọn lại phương án retrieval theo trade-off đã thống nhất.
4. **Chạy lại bộ test sản phẩm và audit.** Cần một case tốt được reviewer xác nhận, một case khó, một case thất bại; lưu actual result, artifact và chi phí/usage. Không chỉnh scope sau khi thấy kết quả chỉ để biến case thành PASS.
5. **Hoàn thiện bài nộp.** Cập nhật test report, ba Forced Decisions và video ≤5 phút từ kết quả cuối; smoke test link online trong phiên có quyền truy cập. Nếu core loop vẫn chưa đạt, báo rõ là MVP chưa chứng minh giả thuyết, không che bằng số unit tests.

Không thực hiện thêm Gemini API call trong lần kiểm toán này. Lượt live tiếp theo cần một giới hạn sử dụng mới và mục tiêu kiểm chứng rõ trước khi chạy.
