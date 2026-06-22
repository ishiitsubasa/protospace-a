document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.topic-dropdown').forEach(function (dropdown) {
    const postId = dropdown.dataset.postId;
    const createUrl = dropdown.dataset.createUrl;
    const list = dropdown.querySelector('.topic-dropdown__list');
    const panel = dropdown.querySelector('.topic-dropdown__panel');
    const form = dropdown.querySelector('.topic-dropdown__form');
    const input = dropdown.querySelector('.topic-dropdown__form-input');
    const createBtn = dropdown.querySelector('.topic-dropdown__create-btn');
    const cancelBtn = dropdown.querySelector('.topic-dropdown__form-cancel');
    const submitBtn = dropdown.querySelector('.topic-dropdown__form-submit');
    let loaded = false;
    let hideTimer = null;

    function showPanel() {
      clearTimeout(hideTimer);
      panel.style.display = 'block';
    }

    function hidePanel() {
      hideTimer = setTimeout(function () {
        panel.style.display = 'none';
        closeForm();
      }, 150);
    }

    function openForm() {
      form.style.display = 'block';
      createBtn.style.display = 'none';
      input.focus();
    }

    function closeForm() {
      form.style.display = 'none';
      createBtn.style.display = '';
      input.value = '';
    }

    function loadTopics() {
      if (loaded) return;
      loaded = true;
      fetch('/discussions/posts/' + postId + '/discussions/')
        .then(function (res) { return res.json(); })
        .then(function (data) {
          const currentId = dropdown.dataset.currentTopicId ? parseInt(dropdown.dataset.currentTopicId) : null;
          if (data.topics.length === 0) {
            list.innerHTML = '<p class="topic-dropdown__empty">まだ議題がありません。</p>';
            return;
          }
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
    }

    dropdown.addEventListener('mouseenter', function () {
      showPanel();
      loadTopics();
    });
    dropdown.addEventListener('mouseleave', hidePanel);
    panel.addEventListener('mouseenter', function () { clearTimeout(hideTimer); });
    panel.addEventListener('mouseleave', hidePanel);

    createBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      openForm();
    });

    cancelBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      closeForm();
    });

    submitBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      const title = input.value.trim();
      if (!title) return;

      submitBtn.disabled = true;
      submitBtn.textContent = '作成中...';

      const csrfToken = document.cookie.split(';')
        .map(function (c) { return c.trim(); })
        .find(function (c) { return c.startsWith('csrftoken='); });
      const csrf = csrfToken ? csrfToken.split('=')[1] : '';

      const formData = new FormData();
      formData.append('title', title);
      formData.append('csrfmiddlewaretoken', csrf);

      fetch(createUrl, {
        method: 'POST',
        body: formData,
        redirect: 'follow',
      })
        .then(function (res) {
          if (res.redirected) {
            window.location.href = res.url;
          } else {
            return res.text().then(function () {
              loaded = false;
              loadTopics();
              closeForm();
            });
          }
        })
        .catch(function () {
          submitBtn.disabled = false;
          submitBtn.textContent = '作成する';
        });
    });

      input.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') closeForm();
      });
  });
});
