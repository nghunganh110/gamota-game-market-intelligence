# Tiến độ kiểm chứng bằng model thật

Mọi dòng dưới đây giữ kết quả gốc; AI audit chưa phải human verification. Status pipeline không thay thế acceptance chất lượng.

| Phép thử | Loại | Calls | Latency | Claim qua cơ học/tổng | Kết quả chính |
|---|---|---:|---:|---:|---|
| T01 lần 1 | Fresh discovery + extraction | 2 | 67.636 s | 0/5 | Partial; period string gate loại kỳ con; semantic overclaims |
| T01 lần 2 | Fresh discovery + extraction | 2 | 45.726 s | 0/0 | Partial; chỉ đọc navigation, model trả gaps |
| T01 snapshot extraction | Saved sources + model extraction mới | 1 | 16.279 s | 5/6 | Partial; period fix hoạt động, quote ghép bị loại, causal overclaim còn |
| T02 | Fresh discovery + extraction | 2 | 83.657 s | 6/10 | Partial; game khác và PDF/HTML hoạt động, quarterly/July scope bị loại, semantic errors còn |
| T03 lỗi kết nối | Attempt trong sandbox, không có response | 1 reservation | 0.379 s | 0/0 | Failed, ConnectError; giữ log, không biết request có tới server không |
| T03 ngoài sandbox sau cấp quyền | Fresh discovery + extraction | 2 | 56.477 s | 1/5 | Partial; chỉ 2/6 nguồn đọc được, genre qualitative evidence, market/portfolio data bị loại |
| T06 / T09 | Chưa chạy | — | — | — | Rights unknown / D30 missing-data challenge |

Tổng **10 local API attempt reservations** quan sát trong các artifacts, gồm 1 ConnectError không có response metadata và 9 attempts có response metadata; không phải số search queries, billed requests hay chi phí tiền tệ. Không cộng offline derivatives thành model runs.

T01/T02/T03 đã được thực thi với nguồn/model thật, bao gồm hai game và một câu hỏi thể loại. **Chưa có case nghiên cứu end-to-end được human audit chấp nhận**, chưa có đo hữu ích với reviewer hoặc chi phí tiền tệ. Bộ test phần mềm không được dùng để thay thế acceptance nghiên cứu.

**Cập nhật 2026-10-15:** [A01/A02 trên MVP mới](mvp-live-results-2026-10-15.md) đã dùng thêm 3 API attempts theo giới hạn mới của người dùng (A01 guided 1, A02 auto 1 lỗi `ServerError`, A02 guided 1). A01 `completed` về pipeline nhưng chưa được human audit; A02 guided `partial`. Một lượt thử A01 trong sandbox không đọc được URL vì DNS và dừng trước Gemini. Tổng cũ 10 reservations ở bảng trên không bao gồm 3 attempts mới. Bộ test phần mềm mới: 78 passed.

Báo cáo chi tiết: [T01 ban đầu](live-T01-review.md), [T01 lần 2](live-T01-rerun-review.md), [T01 extraction](live-T01-extraction-review.md), [T02](live-T02-review.md).

[T03 và lỗi kết nối ban đầu](live-T03-review.md).
