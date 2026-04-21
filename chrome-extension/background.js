chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.url && tab.url.startsWith("http")) {

    fetch("http://127.0.0.1:5000/api/check", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url: tab.url })
    })
    .then(res => res.json())
    .then(data => {
      if (data.result.includes("Phishing")) {

        chrome.scripting.executeScript({
          target: { tabId: tabId },
          func: (message) => {
            const warning = document.createElement("div");
            warning.innerText = "⚠️ PHISHING DETECTED!\n" + message;

            warning.style.position = "fixed";
            warning.style.top = "0";
            warning.style.left = "0";
            warning.style.width = "100%";
            warning.style.background = "red";
            warning.style.color = "white";
            warning.style.padding = "15px";
            warning.style.fontSize = "18px";
            warning.style.textAlign = "center";
            warning.style.zIndex = "9999";

            document.body.prepend(warning);
          },
          args: [data.result]
        });

      }
    })
    .catch(err => console.log(err));
  }
});