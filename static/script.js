const input = document.getElementById("userText");
    const count = document.getElementById("charCount");
    const analyzeBtn = document.getElementById("analyzeBtn");
    const clearBtn = document.getElementById("clearBtn");
    const notice = document.getElementById("notice");
    const emptyState = document.getElementById("emptyState");
    const resultContent = document.getElementById("resultContent");

    const emojiMap = {
      sadness: "😢", joy: "😄", love: "❤️",
      anger: "😠", fear: "😨", surprise: "😲"
    };

    input.addEventListener("input", () => {
      count.textContent = `${input.value.length} / 2000`;
      hideNotice();
    });

    document.querySelectorAll(".sample").forEach(button => {
      button.addEventListener("click", () => {
        input.value = button.dataset.text;
        input.dispatchEvent(new Event("input"));
        input.focus();
      });
    });

    clearBtn.addEventListener("click", () => {
      input.value = "";
      input.dispatchEvent(new Event("input"));
      hideNotice();
      resultContent.classList.remove("visible");
      resultContent.style.display = "none";
      emptyState.style.display = "flex";
      input.focus();
    });

    function showNotice(message, type = "error") {
      notice.textContent = message;
      notice.className = `notice ${type}`;
    }
    function hideNotice() {
      notice.textContent = "";
      notice.className = "notice";
    }

    async function checkHealth() {
      const dot = document.getElementById("statusDot");
      const text = document.getElementById("statusText");
      try {
        const response = await fetch("/health");
        if (!response.ok) throw new Error("Health check failed");
        const data = await response.json();
        const ready = Boolean(data.model_loaded);
        dot.className = `dot ${ready ? "online" : "offline"}`;
        text.textContent = ready ? "Model ready" : "Model not loaded";
      } catch {
        dot.className = "dot offline";
        text.textContent = "API unavailable";
      }
    }

    function renderResult(data) {
      const emotion = data.predicted_emotion;
      document.getElementById("emotionEmoji").textContent = emojiMap[emotion] || "✳";
      document.getElementById("emotionName").textContent = emotion || "Unknown";
      document.getElementById("confidence").textContent =
        `${(Number(data.confidence) * 100).toFixed(1)}% model confidence`;

      const meters = document.getElementById("meters");
      meters.innerHTML = "";
      const probabilities = data.all_probabilities || data.all_probabilites || {};
      Object.entries(probabilities)
        .sort((a, b) => Number(b[1]) - Number(a[1]))
        .forEach(([label, value]) => {
          const percentage = Math.max(0, Math.min(100, Number(value) * 100));
          const row = document.createElement("div");
          row.className = "meter-row";
          const name = document.createElement("div");
          name.className = "meter-name";
          name.textContent = label;
          const track = document.createElement("div");
          track.className = "track";
          const fill = document.createElement("div");
          fill.className = "fill";
          track.appendChild(fill);
          const val = document.createElement("div");
          val.className = "meter-value";
          val.textContent = `${percentage.toFixed(1)}%`;
          row.append(name, track, val);
          meters.appendChild(row);
          requestAnimationFrame(() => { fill.style.width = `${percentage}%`; });
        });

      emptyState.style.display = "none";
      resultContent.style.display = "block";
      resultContent.classList.remove("visible");
      requestAnimationFrame(() => resultContent.classList.add("visible"));
    }

    analyzeBtn.addEventListener("click", async () => {
      const text = input.value.trim();
      hideNotice();

      if (!text) {
        showNotice("Add some text first, then run the analysis.");
        input.focus();
        return;
      }

      analyzeBtn.disabled = true;
      analyzeBtn.innerHTML = '<span class="spinner"></span>Analyzing';
      try {
        const response = await fetch("/predict", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text })
        });

        const data = await response.json().catch(() => ({}));
        if (!response.ok) {
          const detail = typeof data.detail === "string" ? data.detail : "The prediction request could not be completed.";
          throw new Error(detail);
        }
        if (!data.predicted_emotion || data.confidence === undefined) {
          throw new Error("The API response is missing prediction fields. Check the backend response schema.");
        }
        renderResult(data);
      } catch (error) {
        showNotice(`${error.message} Check that the FastAPI server and model are running.`);
      } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = 'Analyze emotion <span aria-hidden="true">↗</span>';
      }
    });

    input.addEventListener("keydown", event => {
      if ((event.ctrlKey || event.metaKey) && event.key === "Enter") analyzeBtn.click();
    });

    checkHealth();
    setInterval(checkHealth, 30000);
