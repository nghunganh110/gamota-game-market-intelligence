# Kịch bản video — tối đa 4 phút 50 giây

AI-PROPOSAL lịch sử, chưa sẵn sàng quay/nộp. Các mốc 37 tests và giả định chưa có live runs bên dưới đã cũ; xem [kiểm toán Mission 2](acceptance-gap-audit.md). Quay phiên bản cuối sau khi có một case thật được reviewer audit. Không nói replay là Gemini research.

| Mốc | Nội dung |
|---|---|
| 0:00–0:30 | Bài toán: Publishing/Strategy Lead cần nhận định truy được về bằng chứng để sàng lọc, không cần AI dự đoán doanh thu. |
| 0:30–1:00 | Phần chọn hiện thực hóa: source → quote/claim → conflict/gap → brief → human review. Python/Streamlit/Gemini là stack đã chọn. |
| 1:00–2:00 | Demo tình huống tốt: ghi rõ synthetic nếu chưa live. Mở claim, xem đoạn trích, quality/relevance và scope; tải JSON/Markdown. |
| 2:00–2:40 | Demo câu hỏi/game khác để cho thấy không hard-code case. Chưa live thì nói engine offline cùng input schema, chưa chứng minh retrieval đa game. |
| 2:40–3:20 | Tình huống khó: conflict giữ hai phía và Hold có action; thiếu D30 retention không thay bằng proxy. |
| 3:20–4:10 | O08: claim đảo nghĩa quote vẫn qua validator. Trình bày actual failure; nhấn mechanically checked khác human verified; demo review và lý do. |
| 4:10–4:50 | 37 tests offline, các yêu cầu live còn thiếu, ba Forced Decisions và ưu tiên audit/entailment. Đưa repo/demo URL chỉ khi đã được kiểm tra. |

Tài liệu này là kịch bản, không phải video đã quay. Video demo offline nếu tạo chỉ dùng để review tiến độ, chưa coi là video bài nộp cuối.
