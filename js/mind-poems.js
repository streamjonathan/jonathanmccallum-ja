// Mind Poems (Japanese) — one poem a day (v1).
// Which poem shows today: poem index = (dayOfMonth - 2) mod 6, so the
// 2nd shows the day-2 poem, the 3rd the day-3 poem, ... cycling every
// 6 days (day 1 shows the day-7 poem). This matches the main site.
// Previous / Next flip between the 6 poems; "今日の詩" goes back to
// today's poem. Without JavaScript the page still shows the day-2
// poem in the card and all 6 poems in the list below.
// NOTE: the Japanese translations below are unreviewed drafts —
// meaning-first, line breaks kept, English originals kept alongside.
(function () {
  var POEMS = [
    { day: 2, accent: "gold", boxed: false,
      ja: ["愛はあなたとともに", "いつまでも", "あなたは自由", "イエスのうちに"],
      en: ["Love is with", "you, forever", "you are free", "in Jesus"] },
    { day: 3, accent: "silver", boxed: false,
      ja: ["ヒースの丘は", "燃えるように", "風の草原の", "下に広がる"],
      en: ["The heather", "fell and flaming", "across the windy", "meadow below"] },
    { day: 4, accent: "bronze", boxed: true,
      ja: ["日差しの浜、清らかに", "どよめき、炎 +", "美しさはいつまでも", "さらに"],
      en: ["Sunlit shore, clean", "roar, flame +", "beauty forever", "more"] },
    { day: 5, accent: "gold", boxed: false,
      ja: ["りんごを食べた", "でも、そう単純ではなく", "実は消化され", "天国が地上に", "失われたのか、先送りにされたのか", "（それは）", "造り主へと向かう"],
      en: ["apple eaten", "but not exactly", "fruit digested", "heaven on earth", "lost or postponed", "(turns) to the", "creator."] },
    { day: 6, accent: "silver", boxed: false,
      ja: ["雪が降る、光", "低く、すべての天が", "上にも下にも", "わたしたちは座っている", "とても大きな世界に"],
      en: ["snow fall, light", "low, all heavens", "above and below", "we sit in a world", "so big"] },
    { day: 7, accent: "bronze", boxed: false,
      ja: ["雲が集まる", "それでも落ちて", "流れていく", "天の涙とともに"],
      en: ["the clouds gather", "yet they fall to", "flow with the", "tears of heaven"] },
  ];

  var card = document.getElementById("mind-poem-card");
  var num = document.getElementById("mind-poem-num");
  var label = document.getElementById("mind-poem-label");
  var jaEl = document.getElementById("mind-poem-ja");
  var enEl = document.getElementById("mind-poem-en");
  if (!card || !num || !label || !jaEl || !enEl) return;

  function todayIndex() {
    var d = new Date().getDate();
    return (((d - 2) % 6) + 6) % 6;
  }

  var current = todayIndex();

  function show(index) {
    current = (((index % 6) + 6) % 6);
    var p = POEMS[current];
    num.textContent = String(p.day);
    num.className = "mind-poems__day mind-poems__accent--" + p.accent;
    label.textContent = p.day + "日目の詩";
    jaEl.innerHTML = "";
    enEl.innerHTML = "";
    p.ja.forEach(function (line, i) {
      if (i) jaEl.appendChild(document.createElement("br"));
      jaEl.appendChild(document.createTextNode(line));
    });
    p.en.forEach(function (line, i) {
      if (i) enEl.appendChild(document.createElement("br"));
      enEl.appendChild(document.createTextNode(line));
    });
    if (p.boxed) card.classList.add("mind-poems__card--boxed");
    else card.classList.remove("mind-poems__card--boxed");
  }

  show(current);

  var prev = document.getElementById("mind-poem-prev");
  var next = document.getElementById("mind-poem-next");
  var todayBtn = document.getElementById("mind-poem-today");
  if (prev) prev.addEventListener("click", function () { show(current - 1); });
  if (next) next.addEventListener("click", function () { show(current + 1); });
  if (todayBtn) todayBtn.addEventListener("click", function () { show(todayIndex()); });
})();
