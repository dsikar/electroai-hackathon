const state = {
  pollTimer: null,
  latest: null,
};

const inputDir = document.getElementById("inputDir");
const outputRoot = document.getElementById("outputRoot");
const ltspicePngEnabled = document.getElementById("ltspicePngEnabled");
const message = document.getElementById("message");
const overallValue = document.getElementById("overallValue");
const overallBar = document.getElementById("overallBar");
const runStatus = document.getElementById("runStatus");
const runTimer = document.getElementById("runTimer");
const currentTask = document.getElementById("currentTask");
const currentTaskMeta = document.getElementById("currentTaskMeta");
const agentSummary = document.getElementById("agentSummary");
const agentConfig = document.getElementById("agentConfig");
const toolConfig = document.getElementById("toolConfig");
const imageCount = document.getElementById("imageCount");
const imageList = document.getElementById("imageList");
const taskList = document.getElementById("taskList");
const debugError = document.getElementById("debugError");
const debugLog = document.getElementById("debugLog");
const agentMetricTemplate = document.getElementById("agentMetricTemplate");
const taskTemplate = document.getElementById("taskTemplate");
const previewModal = document.getElementById("previewModal");
const previewModalImage = document.getElementById("previewModalImage");
const previewModalCaption = document.getElementById("previewModalCaption");
const previewModalClose = document.getElementById("previewModalClose");

function formatSeconds(seconds) {
  if (seconds == null) return "Not started";
  const whole = Math.max(0, Math.floor(seconds));
  const mins = Math.floor(whole / 60);
  const secs = whole % 60;
  return mins ? `${mins}m ${secs}s` : `${secs}s`;
}

function formatTimer(task) {
  if (!task.started_at) return "Pending";
  if (task.finished_at) return `Completed in ${formatSeconds(task.duration_seconds)}`;
  const elapsed = (Date.now() / 1000) - task.started_at;
  return `Running for ${formatSeconds(elapsed)}`;
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    cache: "no-store",
    ...options,
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Request failed");
  return data;
}

function setMessage(text, isError = false) {
  message.textContent = text || "";
  message.dataset.error = isError ? "true" : "false";
}

function renderImages(images) {
  imageList.innerHTML = "";
  imageCount.textContent = `${images.length} file${images.length === 1 ? "" : "s"}`;
  for (const image of images) {
    const item = document.createElement("li");
    item.textContent = image.split("/").pop();
    imageList.appendChild(item);
  }
}

function renderAgentSummary(summary) {
  agentSummary.innerHTML = "";
  const agents = summary.by_agent || {};
  Object.entries(agents).forEach(([agentKey, agent]) => {
    const node = agentMetricTemplate.content.firstElementChild.cloneNode(true);
    node.dataset.agent = agentKey;
    node.querySelector(".agent-label").textContent = agent.label;
    node.querySelector(".agent-value").textContent = agent.running
      ? `${agent.finished} / ${agent.total} complete • ${agent.running} active`
      : `${agent.finished} / ${agent.total}`;
    const fill = node.querySelector(".bar-fill");
    fill.style.width = `${agent.progress}%`;
    fill.dataset.active = agent.running > 0 ? "true" : "false";
    agentSummary.appendChild(node);
  });
}

function renderAgentConfig(config) {
  agentConfig.innerHTML = "";
  Object.entries(config || {}).forEach(([agentKey, item]) => {
    const row = document.createElement("p");
    row.className = "config-row";
    row.dataset.configured = item.configured ? "true" : "false";
    row.textContent = item.configured
      ? `${item.label}: configured`
      : `${item.label}: missing ${item.env_vars.join(" or ")}`;
    agentConfig.appendChild(row);
  });
}

function renderToolConfig(config) {
  toolConfig.innerHTML = "";
  const ltspiceSvg = config?.ltspice_svg;
  const ltspicePng = config?.ltspice_png;
  if (ltspiceSvg) {
    const row = document.createElement("p");
    row.className = "config-row";
    row.dataset.configured = ltspiceSvg.available ? "true" : "false";
    row.textContent = ltspiceSvg.available
      ? `LTSpice SVG: ready (${ltspiceSvg.path})`
      : `LTSpice SVG: install ltspice2svg or set ${ltspiceSvg.env_var}`;
    toolConfig.appendChild(row);
  }
  if (ltspicePng) {
    const row = document.createElement("p");
    row.className = "config-row";
    row.dataset.configured = ltspicePng.available ? "true" : "false";
    row.textContent = ltspicePng.available
      ? `LTSpice PNG: ready (${ltspicePng.renderer})`
      : `LTSpice PNG: install Playwright in the project virtualenv`;
    toolConfig.appendChild(row);
  }
}

function taskStatusLabel(status) {
  return status.replaceAll("_", " ");
}

function previewPathAndLabel(task, previewKind) {
  if (previewKind === "falstad") {
    if (!task.falstad_preview_path) return null;
    return {
      path: task.falstad_preview_path,
      label: "Falstad",
      message: task.falstad_preview_message || "Falstad preview unavailable",
    };
  }

  if (task.ltspice_png_status === "available" && task.ltspice_png_path) {
    return {
      path: task.ltspice_png_path,
      label: "LTSpice PNG",
      message: null,
    };
  }
  if (task.ltspice_svg_status === "available" && task.ltspice_svg_path) {
    return {
      path: task.ltspice_svg_path,
      label: "LTSpice SVG",
      message: null,
    };
  }
  return null;
}

function previewFallbackMessage(task, previewKind) {
  if (previewKind === "falstad") {
    return task.falstad_preview_message || "Falstad preview unavailable";
  }
  return task.ltspice_png_message
    || task.ltspice_svg_message
    || "LTSpice preview unavailable";
}

function renderTaskFiles(task, container) {
  container.innerHTML = "";
  const entries = Object.entries(task.expected_files || {});
  for (const [name, path] of entries) {
    const row = document.createElement("p");
    row.className = "file-row";
    if (task.produced_files && task.produced_files[name]) {
      const link = document.createElement("a");
      link.href = `/api/file?path=${encodeURIComponent(path)}`;
      link.textContent = name;
      link.target = "_blank";
      row.appendChild(link);
    } else {
      row.textContent = `${name} missing`;
      row.classList.add("missing");
    }
    container.appendChild(row);
  }
  if (task.falstad_url) {
    const row = document.createElement("p");
    row.className = "file-row";
    const link = document.createElement("a");
    link.href = task.falstad_url;
    link.textContent = "falstad_url";
    link.target = "_blank";
    row.appendChild(link);
    container.appendChild(row);
  }
  if (task.ltspice_svg_path) {
    const row = document.createElement("p");
    row.className = "file-row";
    if (task.ltspice_svg_status === "available") {
      const link = document.createElement("a");
      link.href = `/api/file?path=${encodeURIComponent(task.ltspice_svg_path)}`;
      link.textContent = "ltspice_svg";
      link.target = "_blank";
      row.appendChild(link);
    } else {
      row.textContent = `ltspice_svg ${task.ltspice_svg_status}`;
      if (task.ltspice_svg_message) {
        row.textContent += `: ${task.ltspice_svg_message}`;
      }
      row.classList.add("missing");
    }
    container.appendChild(row);
  }
  if (task.ltspice_png_path) {
    const row = document.createElement("p");
    row.className = "file-row";
    if (task.ltspice_png_status === "available") {
      const link = document.createElement("a");
      link.href = `/api/file?path=${encodeURIComponent(task.ltspice_png_path)}`;
      link.textContent = "ltspice_png";
      link.target = "_blank";
      row.appendChild(link);
    } else {
      row.textContent = `ltspice_png ${task.ltspice_png_status}`;
      if (task.ltspice_png_message) {
        row.textContent += `: ${task.ltspice_png_message}`;
      }
      row.classList.add("missing");
    }
    container.appendChild(row);
  }
}

function openPreview(task, previewKind) {
  const preview = previewPathAndLabel(task, previewKind);
  if (!preview) return;
  previewModalImage.src = `/api/file?path=${encodeURIComponent(preview.path)}`;
  previewModalImage.alt = `${preview.label} preview for ${task.agent_label} ${task.image_name}`;
  previewModalCaption.textContent = `${preview.label} • ${task.agent_label} • ${task.image_name}`;
  previewModal.hidden = false;
  document.body.classList.add("modal-open");
}

function closePreview() {
  previewModal.hidden = true;
  previewModalImage.removeAttribute("src");
  previewModalCaption.textContent = "";
  document.body.classList.remove("modal-open");
}

function renderTaskPreview(task, previewKind, node) {
  const button = node.querySelector(`.${previewKind}-preview-button`);
  const image = node.querySelector(`.${previewKind}-preview-image`);
  const placeholder = node.querySelector(`.${previewKind}-preview-placeholder`);
  const preview = previewPathAndLabel(task, previewKind);

  if (preview) {
    button.hidden = false;
    image.src = `/api/file?path=${encodeURIComponent(preview.path)}`;
    image.alt = `${preview.label} preview for ${task.agent_label} ${task.image_name}`;
    button.addEventListener("click", () => openPreview(task, previewKind));
    placeholder.hidden = true;
  } else {
    button.hidden = true;
    placeholder.hidden = false;
    placeholder.textContent = previewFallbackMessage(task, previewKind);
  }
}

function renderTasks(tasks) {
  taskList.innerHTML = "";
  for (const task of tasks) {
    const node = taskTemplate.content.firstElementChild.cloneNode(true);
    node.dataset.status = task.status;
    node.querySelector(".task-title").textContent = `${task.agent_label} • ${task.image_name}`;
    node.querySelector(".task-subtitle").textContent = task.image_path;
    node.querySelector(".task-status").textContent = taskStatusLabel(task.status);
    const signpost = node.querySelector(".task-signpost");
    if (task.status === "running") {
      signpost.textContent = "In progress now";
      signpost.dataset.tone = "running";
    } else if (task.finished_at && task.status === "completed") {
      signpost.textContent = `Completed at ${new Date(task.finished_at * 1000).toLocaleTimeString()}`;
      signpost.dataset.tone = "completed";
    } else if (task.finished_at && task.status === "completed_with_issues") {
      signpost.textContent = `Completed with issues at ${new Date(task.finished_at * 1000).toLocaleTimeString()}`;
      signpost.dataset.tone = "issues";
    } else if (task.status === "failed") {
      signpost.textContent = "Failed";
      signpost.dataset.tone = "failed";
    } else if (task.status === "canceled") {
      signpost.textContent = "Canceled";
      signpost.dataset.tone = "failed";
    } else {
      signpost.textContent = "Queued";
      signpost.dataset.tone = "pending";
    }
    node.querySelector(".task-timer").textContent = formatTimer(task);
    node.querySelector(".task-duration").textContent = task.finished_at
      ? new Date(task.finished_at * 1000).toLocaleTimeString()
      : "";
    node.querySelector(".task-command").textContent = (task.command || []).join(" ");
    renderTaskFiles(task, node.querySelector(".task-files"));
    renderTaskPreview(task, "falstad", node);
    renderTaskPreview(task, "ltspice", node);

    const issues = node.querySelector(".task-issues");
    if ((task.issue_messages || []).length) {
      task.issue_messages.forEach((issue) => {
        const item = document.createElement("li");
        item.textContent = issue;
        issues.appendChild(item);
      });
    } else {
      issues.innerHTML = "<li>No issues detected.</li>";
    }
    node.querySelector(".task-preview-debug").textContent = (task.preview_debug || []).join("\n") || "(no preview debug)";
    node.querySelector(".task-stdout").textContent = task.stdout || "(no stdout)";
    node.querySelector(".task-stderr").textContent = task.stderr || "(no stderr)";
    taskList.appendChild(node);
  }
}

function renderDebug(data) {
  debugError.textContent = data.error || "";
  debugLog.innerHTML = "";
  for (const item of data.debug_log || []) {
    const row = document.createElement("p");
    const when = new Date(item.timestamp * 1000).toLocaleTimeString();
    row.textContent = `${when} — ${item.message}`;
    debugLog.appendChild(row);
  }
}

function renderState(data) {
  state.latest = data;
  inputDir.value = data.input_dir || data.default_input_dir;
  outputRoot.value = data.output_root || data.default_output_root;
  ltspicePngEnabled.checked = Boolean(data.ltspice_png_enabled);
  overallValue.textContent = `${data.summary.finished} / ${data.summary.total}`;
  overallBar.style.width = `${data.summary.progress}%`;
  overallBar.dataset.active = data.summary.running > 0 ? "true" : "false";
  runStatus.textContent = data.run_status;
  const runningTask = (data.tasks || []).find((task) => task.status === "running");
  const completedTasks = (data.tasks || []).filter((task) => task.finished_at);
  completedTasks.sort((a, b) => (b.finished_at || 0) - (a.finished_at || 0));
  const mostRecentCompleted = completedTasks[0];
  currentTask.textContent = runningTask
    ? `${runningTask.agent_label} - ${runningTask.image_name}`
    : mostRecentCompleted
      ? `${mostRecentCompleted.agent_label} - ${mostRecentCompleted.image_name}`
      : "None";
  currentTaskMeta.textContent = runningTask
    ? `In progress now • started ${new Date(runningTask.started_at * 1000).toLocaleTimeString()}`
    : mostRecentCompleted
      ? `Most recent completion • ${new Date(mostRecentCompleted.finished_at * 1000).toLocaleTimeString()}`
      : "Waiting";

  if (data.started_at && !data.finished_at) {
    runTimer.textContent = `Elapsed ${formatSeconds((Date.now() / 1000) - data.started_at)}`;
  } else if (data.started_at && data.finished_at) {
    runTimer.textContent = `Finished in ${formatSeconds(data.finished_at - data.started_at)}`;
  } else {
    runTimer.textContent = "No active run";
  }

  renderAgentSummary(data.summary);
  renderAgentConfig(data.agent_config);
  renderToolConfig(data.tool_config);
  renderImages(data.images || []);
  renderTasks(data.tasks || []);
  renderDebug(data);
}

async function refreshState() {
  try {
    const data = await api("/api/state");
    renderState(data);
  } catch (error) {
    setMessage(error.message, true);
  }
}

async function startRun() {
  try {
    setMessage("");
    const data = await api("/api/start", {
      method: "POST",
      body: JSON.stringify({
        input_dir: inputDir.value,
        output_root: outputRoot.value,
        ltspice_png_enabled: ltspicePngEnabled.checked,
      }),
    });
    renderState(data);
  } catch (error) {
    setMessage(error.message, true);
  }
}

async function cancelRun() {
  try {
    const data = await api("/api/cancel", { method: "POST", body: "{}" });
    renderState(data);
  } catch (error) {
    setMessage(error.message, true);
  }
}

async function refreshResults() {
  try {
    const data = await api("/api/refresh", {
      method: "POST",
      body: JSON.stringify({
        input_dir: inputDir.value,
        output_root: outputRoot.value,
        ltspice_png_enabled: ltspicePngEnabled.checked,
      }),
    });
    renderState(data);
  } catch (error) {
    setMessage(error.message, true);
  }
}

document.getElementById("startButton").addEventListener("click", startRun);
document.getElementById("cancelButton").addEventListener("click", cancelRun);
document.getElementById("refreshButton").addEventListener("click", refreshResults);
previewModalClose.addEventListener("click", closePreview);
previewModal.addEventListener("click", (event) => {
  if (event.target === previewModal || event.target.classList.contains("preview-modal-backdrop")) {
    closePreview();
  }
});
window.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !previewModal.hidden) {
    closePreview();
  }
});

refreshState();
state.pollTimer = window.setInterval(refreshState, 1000);
