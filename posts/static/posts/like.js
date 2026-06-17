const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

document.querySelectorAll('.like-btn[data-post-id]').forEach(btn => {
  btn.addEventListener('click', async () => {
    const postId = btn.dataset.postId;
    try {
      const res = await fetch(`/${postId}/like/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken },
      });
      if (res.status === 401) {
        alert('いいねするにはログインが必要です。');
        return;
      }
      if (!res.ok) return;
      const data = await res.json();
      btn.querySelector('.like-count').textContent = data.count;
      btn.classList.toggle('liked', data.liked);
    } catch (e) {
      console.error(e);
    }
  });
});
