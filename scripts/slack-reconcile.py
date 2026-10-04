"""One-time owner-authorized recovery of the already-observed synthetic thread.
No business payloads or tokens are printed. Never posts the report parent again.
"""
import json
import os
from pathlib import Path
import sys
import urllib.error
from urllib.parse import urlparse
from notify_bridge import api, request, write_json, mirror
import importlib.util
spec = importlib.util.spec_from_file_location("smoke", Path(__file__).with_name("slack-smoke.py"))
smoke = importlib.util.module_from_spec(spec)
spec.loader.exec_module(smoke)

TEST_ID = "slack-synthetic-20261004-v1"
PARENT = "1791080816.617629"
CHANNEL = "C0C6LGRJ30R"
KNOWN_ERRORS = {"invalid_auth", "missing_scope", "no_permission", "not_in_channel", "file_uploads_disabled", "file_upload_size_restricted", "file_type_not_allowed", "storage_limit_reached", "invalid_arguments", "missing_argument", "not_allowed_token_type", "ratelimited", "internal_error", "service_unavailable"}

def classified_api(method, data, token):
    body = json.loads(request("https://slack.com/api/" + method, data=data, token=token))
    if body.get("ok") is not True:
        code = body.get("error")
        raise RuntimeError(code if code in KNOWN_ERRORS else "unclassified_api_rejection")
    return body

def main():
    dest = Path(".reconcile-state/reconcile-result.json")
    if dest.exists() or os.environ.get("GITHUB_RUN_ATTEMPT") != "1":
        print("::error::Prior recovery receipt or rerun detected; reconcile manually")
        return 1
    prior = [json.loads(p.read_text()) for p in Path(".original-receipts").glob("*.json")]
    result = {"test_id": TEST_ID, "parent_ts": PARENT, "channel": CHANNEL, "status": "started", "stage": "validate"}
    write_json(dest, result)
    try:
        assert os.environ.get("GITHUB_REPOSITORY") == "kaionn/lazy-product-lab"
        assert os.environ.get("SLACK_REPORT_CHANNEL_ID") == CHANNEL
        assert any(x.get("test_id") == TEST_ID and x.get("status") == "needs_review" for x in prior)
        assert any(x.get("parts") == [PARENT] and x.get("status") == "needs_reconciliation" and not x.get("file_id") for x in prior)
        result["identity"] = smoke.identity()
        token = os.environ["SLACK_BOT_TOKEN"]
        image = Path(".reconcile-state/synthetic-migration-test.png")
        smoke.synthetic_png(image)
        payload = image.read_bytes()
        result["stage"] = "get_upload_url"; write_json(dest, result)
        upload = classified_api("files.getUploadURLExternal", {"filename": image.name, "length": len(payload)}, token)
        result["file_id"] = upload["file_id"]
        # Save allocated ID before binary transport; uncertain delivery is never retried.
        result["stage"] = "validate_upload_url"; write_json(dest, result)
        parsed = urlparse(upload.get("upload_url", ""))
        if parsed.scheme != "https" or not (parsed.hostname or "").endswith(".slack.com"):
            raise RuntimeError("upload_url_host_rejected")
        result["stage"] = "upload_bytes"; write_json(dest, result)
        request(upload["upload_url"], data=payload, binary=True)
        result["stage"] = "complete_upload"; write_json(dest, result)
        classified_api("files.completeUploadExternal", {"files": [{"id": result["file_id"], "title": image.name}], "channel_id": CHANNEL, "thread_ts": PARENT}, token)
        result["file_complete"] = True
        result["stage"] = "dedup_check"; write_json(dest, result)
        os.environ["NOTIFICATION_MODE"] = "shadow"
        os.environ["NOTIFY_STATE_DIR"] = ".reconcile-state"
        os.environ["GITHUB_RUN_ID"] = "37171067253"
        text = {"content": f"[SYNTHETIC MIGRATION TEST {TEST_ID}] Report text + generated color-pattern image. No private data. Discord remains active."}
        # Rebuild original event receipt with confirmed image state. mirror must do zero I/O.
        receipt = next(x for x in prior if x.get("parts") == [PARENT])
        receipt.update(status="sent", file_id=result["file_id"], file_sent=True)
        write_json(Path(".reconcile-state") / (receipt["key"] + ".json"), receipt)
        duplicate = mirror(text, "reports", "synthetic:" + TEST_ID, str(image))
        result["report_dedup"] = duplicate["status"]
        if duplicate["status"] != "already_sent":
            raise RuntimeError("dedup_check_failed")
        result["stage"] = "alert"; write_json(dest, result)
        alert = mirror({"content": f"[SYNTHETIC MIGRATION TEST {TEST_ID}] Alert transport check only. This is not a real failure. No private data."}, "alerts", "synthetic:" + TEST_ID)
        result["alert"] = alert
        write_json(dest, result)
        if alert["status"] != "sent":
            raise RuntimeError("alert_incomplete")
        result["alert_dedup"] = mirror({"content": f"[SYNTHETIC MIGRATION TEST {TEST_ID}] Alert transport check only. This is not a real failure. No private data."}, "alerts", "synthetic:" + TEST_ID)["status"]
        if result["alert_dedup"] != "already_sent":
            raise RuntimeError("dedup_check_failed")
        result["status"] = "api_accepted"; result["stage"] = "complete"
        write_json(dest, result); print(json.dumps(result)); return 0
    except Exception as error:
        allowed = KNOWN_ERRORS | {"unclassified_api_rejection", "upload_url_host_rejected", "dedup_check_failed", "alert_incomplete"}
        result["error_class"] = str(error) if isinstance(error, RuntimeError) and str(error) in allowed else "transport_or_validation_failure"
        result["status"] = "needs_reconciliation"
        write_json(dest, result)
        print(json.dumps(result)); return 1

if __name__ == "__main__":
    raise SystemExit(main())
