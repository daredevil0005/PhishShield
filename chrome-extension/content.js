chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "showWarning") {

    const warning = document.createElement("div");
    warning.innerText = "⚠️ PHISHING DETECTED!\n" + request.message;

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
  }
});