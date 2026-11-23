---
title: "アーティストを紹介する"
slug: suggest-an-artist
---

イエスに従うミュージシャンやアーティストの話を聞くのが大好きです。書いてほしい人、インタビューしてほしい人、リアクション動画を作ってほしい人がいたら、ここで教えてください。

名前とリンクだけで十分です。あとは、なぜその人なのかを一言添えてください。届いたものはすべて読みます。本当にありがとうございます。

知っている人がいますか？写真をタップすると、フォームに自動で入ります。あとは、なぜその人なのかを一言添えて送ってください。

<div class="suggest-carousel" role="list" aria-label="紹介できるミュージシャンやアーティスト">
{% for artist in suggest_carousel %}
  <button type="button" class="suggest-pick" role="listitem" data-artist="{{ artist.name }}" data-link="{{ artist.profile }}" title="{{ artist.name }} を紹介する">
    <img src="{{ artist.img }}" alt="{{ artist.name }}" loading="lazy" width="150" height="150">
    <span class="suggest-pick__name">{{ artist.name }}</span>
    <span class="suggest-pick__note">{{ artist.note }}</span>
  </button>
{% endfor %}
</div>

<p class="suggest-carousel__more">または、下で新しい人を紹介してください。聞くべきだと思う人は、どなたでも。</p>

このサイトは18歳未満の方を対象としていません。

<form id="suggest-form" class="suggest-form">
  <label for="suggest-artist">アーティストの名前</label>
  <input id="suggest-artist" name="artist" type="text" maxlength="200" placeholder="誰をチェックすればいいですか？" required>

  <label for="suggest-link">ソーシャルメディアのプロフィールリンク</label>
  <input id="suggest-link" name="link" type="url" maxlength="500" placeholder="https://www.instagram.com/…" required>

  <fieldset class="suggest-kinds">
    <legend>その人と何をしましょうか？</legend>
    <label><input type="checkbox" name="kind" value="write"> 記事を書く</label>
    <label><input type="checkbox" name="kind" value="interview"> インタビューする</label>
    <label><input type="checkbox" name="kind" value="reaction"> リアクション動画を作る</label>
  </fieldset>

  <label for="suggest-why">なぜその人ですか？</label>
  <textarea id="suggest-why" name="why" rows="3" maxlength="500" placeholder="一言で十分です…"></textarea>

  <label for="suggest-name">あなたのお名前 <span class="optional">(任意)</span></label>
  <input id="suggest-name" name="fromName" type="text" maxlength="100" placeholder="お礼を言えるように">

  <label for="suggest-from-link">あなたのソーシャルメディアのプロフィールリンク <span class="optional">(任意)</span></label>
  <input id="suggest-from-link" name="fromLink" type="url" maxlength="500" placeholder="https://www.instagram.com/…">

  <button id="suggest-button" type="button">紹介を送る</button>

  <p id="suggest-result" aria-live="polite"></p>
</form>
