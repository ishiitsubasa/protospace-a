document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.topic-dropdown').forEach(function (dropdown) {
    const postId = dropdown.dataset.postId;
    const list = dropdown.querySelector('.topic-dropdown__list');
    let loaded = false;

    dropdown.addEventListener('mouseenter', function () {
      if (loaded) return;
      loaded = true;

      fetch(`/discussions/posts/${postId}/discussions/`)
        .then(function (res) { return res.json(); })
        .then(function (data) {
          if (data.topics.length === 0) {
            list.innerHTML = '<p class="topic-dropdown__empty">まだ議題がありません。</p>';
            return;
          }
          list.innerHTML = data.topics
            .map(function (t) {
              return '<div class="topic-dropdown__item">' + t.title + '</div>';
            })
            .join('');
        })
        .catch(function () {
          list.innerHTML = '<p class="topic-dropdown__empty">取得できませんでした。</p>';
        });
    });
  });
});