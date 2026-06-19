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
    // ページ遷移前に既読APIを叩く（失敗しても遷移は続ける）
    try {
        const url = bell.dataset.markReadUrl;
        await fetch(url, {
            method: "POST",
            headers: { "X-CSRFToken": getCsrf() },
        });
    } catch (_) {}
    // hrefへの遷移はそのまま走る
  });

  fetchCount();
  setInterval(fetchCount, POLL_INTERVAL);

  // 詳細ページ: 画面に映ったコメントを既読にする
  const container = document.querySelector('[data-mark-comments-read-url]');
  if (container) {
    const markUrl = container.dataset.markCommentsReadUrl;
    const pending = new Set();
    let timer = null;

    function flush() {
      if (pending.size === 0) return;
      const ids = Array.from(pending);
      pending.clear();
      fetch(markUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
        body: JSON.stringify({ comment_ids: ids }),
      })
        .then(r => r.ok ? r.json() : null)
        .then(data => { if (data) updateBadge(data.remaining); })
        .catch(() => {});
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = parseInt(entry.target.dataset.commentId, 10);
          if (id) pending.add(id);
          observer.unobserve(entry.target);
        }
      });
      clearTimeout(timer);
      timer = setTimeout(flush, 800);
    }, { threshold: 0.5 });

    document.querySelectorAll('.comment-observe[data-comment-id]').forEach(el => {
      observer.observe(el);
    });
  }
})();