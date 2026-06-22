document.addEventListener('DOMContentLoaded', function () {
  var csrfMatch = document.cookie.match(/csrftoken=([^;]+)/);
  var csrf = csrfMatch ? csrfMatch[1] : '';

  // フェードで表示/非表示を切り替えるヘルパー
  function fadeIn(el) {
    el.style.display = '';
    el.style.opacity = '0';
    el.style.transition = 'opacity 0.3s';
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        el.style.opacity = '1';
      });
    });
  }

  function fadeOut(el, callback) {
    el.style.transition = 'opacity 0.3s';
    el.style.opacity = '0';
    setTimeout(function () {
      el.style.display = 'none';
      if (callback) callback();
    }, 300);
  }

  // フォーム → 結果へ切り替え
  function showResult(formView, resultView) {
    fadeOut(formView, function () { fadeIn(resultView); });
  }

  // 結果 → フォームへ切り替え（再投票可）
  function showForm(formView, resultView) {
    fadeOut(resultView, function () { fadeIn(formView); });
  }

  // ---- 共感投票 ----
  var sympathySection = document.getElementById('sympathy-section');
  if (sympathySection) {
    var sympathyUrl = sympathySection.dataset.url;
    var sympathyVoted = sympathySection.dataset.voted === 'true';
    var selectedVote = null;
    var sympathySubmit = document.getElementById('sympathy-submit');
    var sympathyBtns = document.querySelectorAll('#sympathy-buttons .sympathy-btn');
    var sympathyFormView = document.getElementById('sympathy-form-view');
    var sympathyResultView = document.getElementById('sympathy-result-view');
    var sympathyBackBtn = document.getElementById('sympathy-back-btn');

    // 初期表示: 投票済みなら結果を表示（状態③）
    if (sympathyVoted && sympathyFormView && sympathyResultView) {
      sympathyFormView.style.display = 'none';
      sympathyResultView.style.display = '';
    } else if (sympathyResultView) {
      sympathyResultView.style.display = 'none';
    }

    // 既に選択済みのボタンから初期値を読み取る
    sympathyBtns.forEach(function (btn) {
      if (btn.classList.contains('selected')) selectedVote = btn.dataset.value;
    });

    // ボタン選択
    sympathyBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        sympathyBtns.forEach(function (b) { b.classList.remove('selected'); });
        btn.classList.add('selected');
        selectedVote = btn.dataset.value;
        if (sympathySubmit) sympathySubmit.disabled = false;
      });
    });

    // 投票送信
    if (sympathySubmit) {
      sympathySubmit.addEventListener('click', function () {
        if (!selectedVote) return;
        sympathySubmit.disabled = true;

        var body = new FormData();
        body.append('vote_type', selectedVote);

        fetch(sympathyUrl, {
          method: 'POST',
          headers: { 'X-CSRFToken': csrf, 'X-Requested-With': 'XMLHttpRequest' },
          body: body,
        })
          .then(function (res) { return res.json(); })
          .then(function (data) {
            if (!data.ok) { sympathySubmit.disabled = false; return; }
            renderSympathyResult(data.summary);
            // 状態②: 結果へ自動切替
            showResult(sympathyFormView, sympathyResultView);
          });
      });
    }

    // 「戻る」ボタン
    if (sympathyBackBtn) {
      sympathyBackBtn.addEventListener('click', function () {
        showForm(sympathyFormView, sympathyResultView);
      });
    }
  }

  function renderSympathyResult(s) {
    var result = document.getElementById('sympathy-result');
    if (!result) return;
    if (s.total === 0) {
      result.innerHTML = '<p class="vote-section__empty">まだ投票がありません</p>';
      return;
    }
    var yesPct   = Math.round(s.yes   / s.total * 100);
    var maybePct = Math.round(s.maybe / s.total * 100);
    var noPct    = Math.round(s.no    / s.total * 100);

    var deptHtml = '';
    if (s.dept_breakdown && Object.keys(s.dept_breakdown).length) {
      deptHtml = '<div class="dept-grid">';
      for (var dept in s.dept_breakdown) {
        var c = s.dept_breakdown[dept];
        var dt = c.yes + c.maybe + c.no;
        var dp = dt > 0 ? Math.round(c.yes / dt * 100) : 0;
        deptHtml += '<div class="dept-card">' +
          '<p class="dept-card__name">' + dept + '</p>' +
          '<div class="stack-bar stack-bar--sm">' +
          '<div class="stack-bar__yes" style="width:' + Math.round(c.yes/dt*100) + '%"></div>' +
          '<div class="stack-bar__maybe" style="width:' + Math.round(c.maybe/dt*100) + '%"></div>' +
          '<div class="stack-bar__no" style="width:' + Math.round(c.no/dt*100) + '%"></div>' +
          '</div>' +
          '<p class="dept-card__rate">共感 ' + dp + '%（' + dt + '票）</p>' +
          '</div>';
      }
      deptHtml += '</div>';
    }

    result.innerHTML =
      '<div class="sympathy-highlight">' +
        '<span class="sympathy-highlight__pct">' + yesPct + '%</span>' +
        '<span class="sympathy-highlight__label">が共感</span>' +
      '</div>' +
      '<div class="stack-bar">' +
        '<div class="stack-bar__yes" style="width:' + yesPct + '%"></div>' +
        '<div class="stack-bar__maybe" style="width:' + maybePct + '%"></div>' +
        '<div class="stack-bar__no" style="width:' + noPct + '%"></div>' +
      '</div>' +
      '<div class="stack-bar__legend">' +
        '<span class="legend-yes">共感する ' + yesPct + '%</span>' +
        '<span class="legend-maybe">どちらとも ' + maybePct + '%</span>' +
        '<span class="legend-no">共感しない ' + noPct + '%</span>' +
        '<span class="legend-total">' + s.total + '票</span>' +
      '</div>' +
      deptHtml;
  }

  // ---- 課題スコア ----
  var PAIN_LABELS = ['', '全く感じない', 'あまり感じない', 'どちらとも', 'やや感じている', '強く感じている'];

  var painSection = document.getElementById('pain-section');
  if (painSection) {
    var painUrl = painSection.dataset.url;
    var painVoted = painSection.dataset.voted === 'true';
    var selectedScore = null;
    var painSubmit = document.getElementById('pain-submit');
    var painBtns = document.querySelectorAll('#pain-buttons .pain-btn');
    var selectedLabel = document.getElementById('pain-selected-label');
    var painFormView = document.getElementById('pain-form-view');
    var painResultView = document.getElementById('pain-result-view');
    var painBackBtn = document.getElementById('pain-back-btn');

    // 初期表示: 投票済みなら結果を表示（状態③）
    if (painVoted && painFormView && painResultView) {
      painFormView.style.display = 'none';
      painResultView.style.display = '';
    } else if (painResultView) {
      painResultView.style.display = 'none';
    }

    // 既に選択済みのボタンから初期値を読み取る
    painBtns.forEach(function (btn) {
      if (btn.classList.contains('selected')) selectedScore = parseInt(btn.dataset.value);
    });

    // ボタン選択
    painBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        painBtns.forEach(function (b) { b.classList.remove('selected'); });
        btn.classList.add('selected');
        selectedScore = parseInt(btn.dataset.value);
        if (painSubmit) painSubmit.disabled = false;
        if (selectedLabel) selectedLabel.textContent = PAIN_LABELS[selectedScore];
      });
    });

    // 回答送信
    if (painSubmit) {
      painSubmit.addEventListener('click', function () {
        if (!selectedScore) return;
        painSubmit.disabled = true;

        var body = new FormData();
        body.append('score', selectedScore);

        fetch(painUrl, {
          method: 'POST',
          headers: { 'X-CSRFToken': csrf, 'X-Requested-With': 'XMLHttpRequest' },
          body: body,
        })
          .then(function (res) { return res.json(); })
          .then(function (data) {
            if (!data.ok) { painSubmit.disabled = false; return; }
            renderPainResult(data.summary);
            // 状態②: 結果へ自動切替
            showResult(painFormView, painResultView);
          });
      });
    }

    // 「戻る」ボタン
    if (painBackBtn) {
      painBackBtn.addEventListener('click', function () {
        showForm(painFormView, painResultView);
      });
    }
  }

  function renderPainResult(s) {
    var result = document.getElementById('pain-result');
    if (!result) return;
    if (s.total === 0) {
      result.innerHTML = '<p class="vote-section__empty">まだ回答がありません</p>';
      return;
    }

    var deptHtml = '';
    if (s.dept_breakdown && Object.keys(s.dept_breakdown).length) {
      deptHtml = '<div class="dept-bar-list">';
      for (var dept in s.dept_breakdown) {
        var avg = s.dept_breakdown[dept];
        var pct = Math.round(avg / 5 * 100);
        deptHtml += '<div class="dept-bar-row">' +
          '<span class="dept-bar-row__name">' + dept + '</span>' +
          '<div class="dept-bar-wrap"><div class="dept-bar-fill" style="width:' + pct + '%"></div></div>' +
          '<span class="dept-bar-row__val">' + avg + '</span>' +
          '</div>';
      }
      deptHtml += '</div>';
    }

    result.innerHTML =
      '<div class="pain-metrics">' +
        '<div class="pain-metric"><span class="pain-metric__value">' + s.avg + '</span><span class="pain-metric__label">平均スコア</span></div>' +
        '<div class="pain-metric"><span class="pain-metric__value">' + s.high_rate + '%</span><span class="pain-metric__label">スコア4以上の割合</span></div>' +
        '<div class="pain-metric"><span class="pain-metric__value">' + s.total + '</span><span class="pain-metric__label">回答数</span></div>' +
      '</div>' +
      deptHtml;
  }
});
