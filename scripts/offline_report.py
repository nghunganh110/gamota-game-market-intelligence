"""Re-run observable acceptance cases and retain actual artifacts."""
from pathlib import Path
import json
from gmi.replay import replay
from gmi.validation import validate_run
from gmi.models import Run
from gmi.pipeline import run_research
class FaultProvider:
    usage={}
    def search(self,scope): raise TimeoutError('Injected fault')
class EmptyReader:
    def read(self,url,source_id): raise AssertionError('Must not read after discovery fails')

root = Path('docs/mission2/test-artifacts')
root.mkdir(parents=True,exist_ok=True)
rows=[]
def record(id, label, expected, run, passed, lesson):
    result={'id':id,'type':'synthetic / offline','expected':expected,'actual':{'status':run.status,'recommendation':run.recommendation,'claim_statuses':[c.status for c in run.extraction.claims],'findings':[f.text for f in run.extraction.findings],'errors':run.errors},'product_result':'Đạt' if passed else 'Chưa đạt','lesson':lesson}
    rows.append((label,result))
    (root/f'{id}.json').write_text(run.model_dump_json(indent=2))

r=replay('good'); record('O01','Tình huống tốt','Các chiều đủ synthetic evidence → Tiếp tục; xuất ledger truy vết được',r,r.recommendation=='Tiếp tục' and r.status=='completed','Workflow hoạt động trên đầu vào synthetic; chưa chứng minh chất lượng Gemini.')
r=replay('other_game'); record('O02','Game/thị trường/câu hỏi khác','Xử lý Game Beta ở China; Research không ép recommendation',r,r.scope.market=='China' and r.recommendation is None and r.status=='completed','Logic không hard-code MABINOGI; chưa thay thế ba live runs.')
r=replay('conflict'); record('O03','Khó: hai nguồn mâu thuẫn','Giữ C1 và C4, Tạm giữ, có bước phân xử',r,r.recommendation=='Tạm giữ' and r.extraction.conflicts[0].claim_ids==['C1','C4'],'Không lấy trung bình hoặc bỏ một phía.')
r=replay('missing'); record('O04','Thiếu D30 retention','Không thay bằng doanh thu; partial và gap cụ thể',r,r.status=='partial' and not r.extraction.findings,'Câu hỏi chưa được đáp ứng; xử lý thiếu dữ liệu đúng. Case synthetic, không phải T09 live.')
r=replay('good'); r.extraction.claims[0].quote='A nonexistent invented quote'; r=validate_run(r); record('O05','Citation giả','Loại claim và findings phụ thuộc; Tạm giữ',r,r.extraction.claims[0].status=='rejected' and not r.extraction.findings,'Chặn trích đoạn giả bằng nội dung đã đọc.')
r=replay('good'); r.extraction.claims[0].market='Korea'; r=validate_run(r); record('O06','Nguồn sai thị trường','Không dùng Korea evidence vượt gate Vietnam',r,r.recommendation=='Tạm giữ' and r.extraction.claims[0].status=='rejected','Uy tín nguồn không thay thế độ phù hợp.')
r=run_research(replay('good').scope,FaultProvider(),EmptyReader()); record('O07','Lỗi kỹ thuật','failed; không tạo claim, không Dừng opportunity',r,r.status=='failed' and r.recommendation=='Tạm giữ' and not r.extraction.claims,'Fault injection PASS kỹ thuật; không tự tính thành case thị trường thất bại.')
r=replay('semantic_failure'); record('O08','Thất bại sản phẩm: ngữ nghĩa','Nhận ra claim nói mạnh trong khi quote nói không mạnh',r,False,'Actual: claim và finding sai vẫn qua quote matching. Cần semantic audit người dùng; ưu tiên thêm entailment assessment và audit set khi chạy live.')
(root/'acceptance-results.json').write_text(json.dumps([r for _,r in rows],ensure_ascii=False,indent=2))
lines=['# Actual offline test report','Toàn bộ O01–O08 là synthetic hoặc fault injection; không có Gemini live call. Không dùng claim thị trường cũ như output MVP.',
'## Kiểm thử tự động','Lần đầu: 30 passed, 3 failed. Hai UI tests sai đường dẫn; một HTML test giả định library chọn title tag trong khi chọn heading. Đã sửa assumptions của test. Kết quả trước sửa giữ ở pytest-initial.xml.',
'Lần sau: 33 passed; sau khi thêm kiểm tra sửa đánh giá nguồn, blocker định nghĩa trước, PDF reader và pipeline mock đầy đủ: **37 passed**. Bao gồm kiểm tra UI/review, API disabled, mock SDK/schema/attribution, scope/cutoff/citation, lỗi thu thập và reader. `test_known_semantic_failure...` PASS vì tái hiện được giới hạn sản phẩm; không phải semantic support PASS.',
'## Các tình huống có kết quả thực tế']
for label,r in rows:
    lines += [f'### {r["id"]} — {label}',f'**Loại:** {r["type"]}',f'**Kỳ vọng:** {r["expected"]}',f'**Kết quả thực tế:** `{json.dumps(r["actual"],ensure_ascii=False)}`',f'**Đạt/Chưa đạt:** {r["product_result"]}',f'**Điều học được:** {r["lesson"]}',f'**Artifact:** [Run JSON](test-artifacts/{r["id"]}.json)']
lines += ['## Còn thiếu trước bài nộp','T01–T03 và T06/T09 live chưa chạy; chưa có audit của người tham gia/Lead thực; chưa đo chất lượng nghiên cứu, latency live, chi phí hay tiết kiệm thời gian. O08 là thất bại synthetic đã quan sát; chưa đáp ứng yêu cầu case sản phẩm thất bại từ live research.']
Path('docs/mission2/test-report.md').write_text('\n\n'.join(lines))
print(f'Actual offline acceptance cases: {len(rows)}; product limitation: O08 Chưa đạt')
