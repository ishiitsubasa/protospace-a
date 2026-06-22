document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.topic-dropdown').forEach(function (dropdown) {
    const postId = dropdown.dataset.postId;
    const list = dropdown.querySelector('.topic-dropdown__list');
    const panel = dropdown.querySelector('.topic-dropdown__panel');
    let loaded = false;
    let hideTimer = null;

    function showPanel() {
      clearTimeout(hideTimer);
      panel.style.display = 'block'; // または classList.add('is-open')
    }

    function hidePanel() {
      hideTimer = setTimeout(function () {
        panel.style.display = 'none'; // または classList.remove('is-open')
      }, 150); // 少し遅延させてパネルへの移動を許容
    }

    // ボタン（親要素）へのホバー
    dropdown.addEventListener('mouseenter', function () {
      showPanel();
      if (loaded) return;
      loaded = true;
      fetch(`/discussions/posts/${postId}/discussions/`)
        .then(function (res) { return res.json(); })
        .then(function (data) {
          if (data.topics.length === 0) {
            list.innerHTML = '<p class="topic-dropdown__empty">まだ議題がありません。</p>';
            return;
          }
          const currentId = dropdown.dataset.currentTopicId ? parseInt(dropdown.dataset.currentTopicId) : null;
          list.innerHTML = data.topics
            .map(function (t) {
              const isCurrent = currentId && t.id === currentId;
              return '<a href="/discussions/' + t.id + '/" class="topic-dropdown__item' + (isCurrent ? ' topic-dropdown__item--current' : '') + '">' + t.title + '</a>';
            })
            .join('');
        })
        .catch(function () {
          list.innerHTML = '<p class="topic-dropdown__empty">取得できませんでした。</p>';
        });
    });

    dropdown.addEventListener('mouseleave', hidePanel);

    // パネル自体にもイベントを付けて、パネル上にいる間は閉じない
    panel.addEventListener('mouseenter', function () {
      clearTimeout(hideTimer);
    });
    panel.addEventListener('mouseleave', hidePanel);
  });
});