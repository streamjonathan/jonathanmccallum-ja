(function () {
  var player = document.getElementById('jcb-player');
  var pageLink = document.getElementById('jcb-page-link');
  var buttons = document.querySelectorAll('.audio-bible-chapters button');
  if (!player || !buttons.length) return;
  buttons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      player.src = btn.getAttribute('data-src');
      pageLink.href = btn.getAttribute('data-page');
      buttons.forEach(function (b) { b.classList.remove('is-active'); });
      btn.classList.add('is-active');
      player.play();
    });
  });
})();
