---
layout: default
title: ディレクション辞書
permalink: /
---

<h1>ディレクション辞書</h1>

<p>Webディレクションの実務で使う用語・業務・考え方を、<strong>1項目あたり1ページ</strong>でまとめた辞書です。一般社団法人ディレクションサポート協会（DiSA）が制作しています。</p>

<p>全138項目。企画・プロデュースから、情報設計、制作進行、サービス運営、ツール、採用まで。各ページはすべて同じ型（10秒でわかる要点まとめ／概要／なぜ重要なのか／実務のポイント／スキルアップのヒント）で書かれています。</p>

<div class="toc">
{% assign entries = site.pages | where_exp:"p","p.number" | sort:"number" %}
{% assign chapters = "AI時代のディレクションについて,企画・プロデュース,情報設計・仕様設計,制作・開発ディレクション,サービス運営・運用,プロモーション,ライティング,ツール,採用" | split:"," %}
{% for ch in chapters %}
  {% assign group = entries | where:"chapter", ch %}
  <h2>{{ ch }}（{{ group.size }}項目）</h2>
  <ul>
  {% for e in group %}
    {% assign ps = e.title | split: "　" %}{% assign nm = ps | last %}
    <li><span class="n">{{ e.number }}</span>{% if ps.size > 2 %}<span class="mid">{{ ps[1] }}</span>{% endif %}<a href="{{ e.url | relative_url }}">{{ nm }}</a></li>
  {% endfor %}
  </ul>
{% endfor %}
</div>
