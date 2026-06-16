(function () {
  const POLL_INTERVAL = 30000;
  const badge = document.getElementById("notification-badge");
  const bell  = document.getElementById("notification-bell");
  if (!bell || !badge) return;

  function getCsrf() {
    const m = document.cookie.match(/csrftoken=([^;]+)/);
    return m ? m[1] : "";
  }

  function updateBadge(count) {
    if (count <= 0)      badge.textContent = "";
    else if (count > 99) badge.textContent = "99+";
    else                 badge.textContent = count;
  }

  async function fetchCount() {
    try {
      // data属性からURLを取得（後述）
      const url = bell.dataset.unreadUrl;
      const res = await fetch(url);
      if (res.ok) updateBadge((await res.json()).count);
    } catch (_) {}
  }

  bell.addEventListener("click", async () => {
    try {
      const url = bell.dataset.markReadUrl;
      await fetch(url, {
        method: "POST",
        headers: { "X-CSRFToken": getCsrf() },
      });
    } catch (_) {}
    updateBadge(0);
  });

  fetchCount();
  setInterval(fetchCount, POLL_INTERVAL);
})();