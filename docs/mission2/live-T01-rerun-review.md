# T01 lần 2 — tìm nguồn chưa đáp ứng

**Artifact:** `runs/66f919b8-382a-4ded-a777-5f021a3dd3c6/run.json`. Internal run ID: `1255ecd2-96b1-42f0-b08d-6845a0d94e98`.

**Kỳ vọng:** kiểm chứng việc Gemini tự sinh khoảng ngày đo và trả claim có nguồn sau bản sửa kỳ đo.

**Kết quả thực tế:** 2 API attempts, 1 search query được báo, 45.726 giây. Search total tokens 883; extraction total tokens 1,992. Chỉ một URL Nexon được đọc; 692 ký tự là menu/navigation, không có nội dung bài. Nguồn bị model đánh giá unsuitable. Không có claim hoặc finding; có gaps cụ thể, không có exception. Trạng thái partial. Chưa xác định chi phí tiền tệ.

**Đạt/Chưa đạt:** chưa đạt câu hỏi nghiên cứu; chưa có bằng chứng kiểm chứng bản sửa kỳ đo trên output live. Model không bịa claim khi chỉ có navigation là hành vi phù hợp, nhưng không làm lần nghiên cứu này thành PASS. Việc không có errors không đồng nghĩa dữ liệu đủ.

**Điều học được:** retrieval có thể biến động mạnh giữa các lần chạy. Một query về release date không đủ cho câu hỏi commercial performance. Reader trước đó cho phép fallback thu cả menu và gắn read_status=read; số ký tự đủ dài không chứng minh có article body.

## Thay đổi sau quan sát

- Search prompt yêu cầu tìm theo chỉ số/kỳ đo, ưu tiên article/report thay vì homepage và bao phủ loại nguồn phù hợp trong cùng discovery call. Không thêm search call hoặc tự retry. Đây là cải tiến prompt, chưa có kết quả live xác nhận.
- HTML reader dùng fast + favor_precision để bỏ backup extraction có thể thu navigation. Test navigation shell synthetic bị từ chối; chưa fetch lại URL thật bằng reader sửa nên không tuyên bố đã sửa mọi trang Nexon. Có thể mất một số bài khó trích, giữ giới hạn này công khai.
- Thêm CLI `--sources-from` để tách phép thử extraction khỏi retrieval: dùng snapshots của câu hỏi cũ, loại unsuitable và exact duplicate, giữ ngày truy cập, gọi extraction một lần. Output gắn **replay với new_model_extraction=true**, không phải fresh live retrieval. Có parent run ID và hash. Không dùng search snippets hoặc brief AI đã sửa làm evidence.

## Phép thử tiếp theo được chuẩn bị

Dùng snapshots hữu ích từ lần đầu (Sensor Tower, Mobile Index, Newsis) và prompt/schema hiện tại. Một API attempt mới, không network document retrieval. Mục đích là quan sát model tự tạo period_start/end, quote coverage, cautious findings và Research dimensions rỗng. Không coi câu trả lời là human-verified hoặc chứng minh discovery đã tốt.

```sh
.venv/bin/python -m scripts.live_research --scope docs/mission2/live-T01-scope.json --sources-from runs/9e512f9c-3771-472a-9cba-3e1a5a87ae10/run.json --run
```

Chạy trong Terminal đã cấu hình key/model nếu tiếp tục dùng thêm một attempt trong giới hạn được cho phép. Chưa chạy phép thử này. Không cần chạy lại full discovery chỉ để chẩn đoán extraction.

## Kiểm tra đã thực hiện

**50 tests passed**: thêm navigation-shell rejection, snapshot dedup/filter, đúng một extraction invocation, nguồn cha giữ nguyên và chặn dùng nhầm câu hỏi trước API call. Các tests này là offline; không có Gemini call mới trong phiên chẩn đoán.
