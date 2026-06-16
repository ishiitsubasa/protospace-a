document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.like-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var url = btn.dataset.url;
      var csrfToken = document.cookie.match(/csrftoken=([^;]+)/);
      if (!csrfToken) return;

      fetch(url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken[1],
          'X-Requested-With': 'XMLHttpRequest',
        },
      })
        .then(function (res) { return res.json(); })
        .then(function (data) {
          btn.querySelector('.like-count').textContent = data.count;
          if (data.liked) {
            btn.classList.add('liked');
          } else {
            btn.classList.remove('liked');
          }
        });
    });
  });
});
