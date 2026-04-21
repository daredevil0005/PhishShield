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

    const data = await response.json();
    document.getElementById("result").innerText = data.result;

  } catch (err) {
    console.error(err);
    document.getElementById("result").innerText = "Error connecting to backend";
  }
});