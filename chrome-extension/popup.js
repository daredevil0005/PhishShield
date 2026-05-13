document.getElementById("checkBtn").addEventListener("click", async () => {
  try {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    let url = tab.url;

    const response = await fetch("http://127.0.0.1:5000/api/check", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url: url })
    });

    const text = await response.text();
    let data;
    try {
      data = JSON.parse(text);
    } catch {
      document.getElementById("result").innerText = "Invalid response from server";
      return;
    }

    if (!response.ok) {
      const msg = (data && data.error) || response.statusText || "Request failed";
      document.getElementById("result").innerText = msg;
      return;
    }

    const result = data && typeof data.result === "string" ? data.result : "No result";
    document.getElementById("result").innerText = result;

  } catch (err) {
    console.error(err);
    document.getElementById("result").innerText = "Error connecting to backend";
  }
});
