const runForm = document.getElementById("run-form");
const startBtn = document.getElementById("start-btn");
const stopBtn = document.getElementById("stop-btn");
const clearBtn = document.getElementById("clear-btn");
const downloadBtn = document.getElementById("download-btn");
const logOutput = document.getElementById("log-output");
const finalOutput = document.getElementById("final-output");
const statusEl = document.getElementById("status");

let controller = null;
let currentLog = "";
let finalPayload = null;

function appendLog(line) {
  currentLog += `${line}\n`;
  logOutput.textContent = currentLog;
  logOutput.scrollTop = logOutput.scrollHeight;
}

function setRunning(isRunning) {
  startBtn.disabled = isRunning;
  stopBtn.disabled = !isRunning;
}

function updateStatus(text) {
  statusEl.textContent = text;
}

function parseSseChunk(buffer) {
  const blocks = buffer.split("\n\n");
  const complete = blocks.slice(0, -1);
  const rest = blocks.at(-1) ?? "";

  for (const block of complete) {
    if (!block.trim()) continue;
    const lines = block.split("\n");
    const event = lines.find((l) => l.startsWith("event:"))?.replace("event:", "").trim() || "message";
    const dataText = lines
      .filter((l) => l.startsWith("data:"))
      .map((l) => l.replace("data:", "").trim())
      .join("\n");

    appendLog(`event: ${event}`);

    if (dataText) {
      appendLog(`data: ${dataText}`);
      try {
        const parsed = JSON.parse(dataText);
        if (["WorkflowCompleted", "RunCompleted", "WorkflowRunOutputEvent"].includes(event) || parsed.event === "WorkflowCompleted") {
          finalPayload = parsed;
          finalOutput.textContent = JSON.stringify(parsed, null, 2);
        }
      } catch {
        // keep raw data only
      }
    }

    appendLog("");
  }

  return rest;
}

runForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (controller) controller.abort();

  const baseUrl = document.getElementById("base-url").value.replace(/\/$/, "");
  const message = document.getElementById("message").value;
  const sessionId = document.getElementById("session-id").value;
  const userId = document.getElementById("user-id").value;
  const version = document.getElementById("version").value;

  const formData = new URLSearchParams();
  formData.append("message", message);
  formData.append("stream", "true");
  formData.append("session_id", sessionId);
  formData.append("user_id", userId);
  formData.append("version", version);

  const endpoint = `${baseUrl}/workflows/content-creation-workflow/runs`;

  controller = new AbortController();
  setRunning(true);
  updateStatus(`Connecting to ${endpoint} ...`);
  finalPayload = null;
  finalOutput.textContent = "";

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        accept: "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData,
      signal: controller.signal,
    });

    if (!response.ok || !response.body) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    updateStatus(`Streaming from ${endpoint}`);

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      buffer = parseSseChunk(buffer);
    }

    if (buffer.trim()) {
      appendLog(buffer);
    }

    updateStatus("Stream finished");
  } catch (error) {
    if (error.name === "AbortError") {
      updateStatus("Stream stopped by user");
      appendLog("[stream aborted]");
    } else {
      updateStatus("Error while streaming");
      appendLog(`[error] ${error.message}`);
    }
  } finally {
    setRunning(false);
    controller = null;
  }
});

stopBtn.addEventListener("click", () => {
  if (controller) controller.abort();
});

clearBtn.addEventListener("click", () => {
  currentLog = "";
  finalPayload = null;
  logOutput.textContent = "";
  finalOutput.textContent = "";
  updateStatus("Idle");
});

downloadBtn.addEventListener("click", () => {
  const now = new Date().toISOString().replace(/[:.]/g, "-");
  const logBlob = new Blob([currentLog || "[empty log]\n"], { type: "text/plain" });
  const url = URL.createObjectURL(logBlob);

  const a = document.createElement("a");
  a.href = url;
  a.download = `workflow-stream-log-${now}.txt`;
  a.click();

  URL.revokeObjectURL(url);
});
