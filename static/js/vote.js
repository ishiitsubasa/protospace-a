document.addEventListener('DOMContentLoaded', function () {
  var csrfMatch = document.cookie.match(/csrftoken=([^;]+)/);
  var csrf = csrfMatch ? csrfMatch[1] : '';

  // ---- 共感投票 ----
  var sympathySection = document.getElementById('sympathy-section');
  if (sympathySection) {
    var sympathyUrl = sympathySection.dataset.url;
    var selectedVote = null;
    var sympathySubmit = document.getElementById('sympathy-submit');
    var sympathyBtns = document.querySelectorAll('#sympathy-buttons .sympathy-btn');

    // 既に選択済みのボタンから初期値を読み取る
    sympathyBtns.forEach(function (btn) {
      if (btn.classList.contains('selected')) selectedVote = btn.dataset.value;
    });

    sympathyBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        sympathyBtns.forEach(function (b) { b.classList.remove('selected'); });
        btn.classList.add('selected');
        selectedVote = btn.dataset.value;
        sympathySubmit.disabled = false;
      });
    });

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
            sympathySubmit.disabled = false;
            if (!data.ok) return;
            var msg = document.getElementById('sympathy-voted-msg');
            if (msg) {
              msg.textContent = '投票済み（変更できます）';
            } else {
              msg = document.createElement('p');
              msg.id = 'sympathy-voted-msg';
              msg.className = 'vote-section__voted-msg';
              msg.textContent = '投票済み（変更できます）';
              sympathySubmit.insertAdjacentElement('afterend', msg);
            }
            renderSympathyResult(data.summary);
          });
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
    var selectedScore = null;
    var painSubmit = document.getElementById('pain-submit');
    var painBtns = document.querySelectorAll('#pain-buttons .pain-btn');
    var selectedLabel = document.getElementById('pain-selected-label');

    // 既に選択済みのボタンから初期値を読み取る
    painBtns.forEach(function (btn) {
      if (btn.classList.contains('selected')) selectedScore = parseInt(btn.dataset.value);
    });

    painBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        painBtns.forEach(function (b) { b.classList.remove('selected'); });
        btn.classList.add('selected');
        selectedScore = parseInt(btn.dataset.value);
        painSubmit.disabled = false;
        if (selectedLabel) selectedLabel.textContent = PAIN_LABELS[selectedScore];
      });
    });

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
            painSubmit.disabled = false;
            if (!data.ok) return;
            var msg = document.getElementById('pain-voted-msg');
            if (msg) {
              msg.textContent = '回答済み（あなたのスコア: ' + selectedScore + '）変更できます';
            } else {
              msg = document.createElement('p');
              msg.id = 'pain-voted-msg';
              msg.className = 'vote-section__voted-msg';
              msg.textContent = '回答済み（あなたのスコア: ' + selectedScore + '）変更できます';
              painSubmit.insertAdjacentElement('afterend', msg);
            }
            renderPainResult(data.summary);
          });
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
