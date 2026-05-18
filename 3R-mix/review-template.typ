#let ink = rgb("#1c232b")
#let muted = rgb("#5d6875")
#let soft = rgb("#f4f7fb")
#let band = rgb("#e7eef7")
#let accent = rgb("#2f5f8f")
#let light-line = rgb("#c9d2dc")
#let rule = 0.75pt + light-line

#let review(
  title: "",
  subtitle: none,
  authors: (),
  date: none,
  abstract: none,
  keywords: none,
  body,
) = {
  set document(title: title, author: authors)
  set page(
    paper: "a4",
    margin: (x: 24mm, y: 22mm),
    header: context if counter(page).get().at(0) > 1 {
      text(size: 8.5pt, fill: muted)[#title]
      h(1fr)
      text(size: 8.5pt, fill: muted)[#counter(page).display()]
    },
  )
  set text(
    font: ("Times New Roman", "SimSun"),
    lang: "zh",
    size: 10.5pt,
    fill: ink,
  )
  set par(justify: true, first-line-indent: 2em, leading: 0.66em, spacing: 0.52em)
  show heading: it => {
    if it.level == 1 {
      v(1.0em)
      text(size: 15pt, weight: "bold", fill: ink)[#it.body]
      v(0.15em)
      line(length: 100%, stroke: 0.65pt + light-line)
      v(0.65em)
    } else if it.level == 2 {
      v(0.55em)
      text(size: 12pt, weight: "bold", fill: ink)[#it.body]
      v(0.25em)
    } else {
      v(0.35em)
      text(size: 10.5pt, weight: "bold", fill: ink)[#it.body]
      v(0.15em)
    }
  }
  set table(
    stroke: 0.35pt + light-line,
    inset: 5.5pt,
  )
  show table: it => {
    set text(size: 8.7pt)
    it
  }
  show figure: set block(above: 1.1em, below: 1.1em)
  set figure.caption(position: bottom)
  show figure.caption: it => {
    set par(first-line-indent: 0pt, justify: true)
    v(0.25em)
    text(size: 9pt)[*#it.supplement #it.counter.display(it.numbering).* #it.body]
  }
  set bibliography(title: none, style: "american-psychological-association")

  align(center)[
    #v(2em)
    #text(size: 20pt, weight: "bold")[#title]
    #if subtitle != none [
      #v(0.55em)
      #text(size: 12pt, fill: muted)[#subtitle]
    ]
    #v(1.6em)
    #text(size: 10.5pt)[#authors.join("，")]
    #if date != none [
      #v(0.3em)
      #text(size: 9.5pt, fill: muted)[#date]
    ]
  ]
  v(1.2em)
  line(length: 100%, stroke: rule)
  v(0.9em)

  if abstract != none [
    #set par(first-line-indent: 0pt, justify: true, leading: 0.62em)
    #text(weight: "bold")[摘要] #abstract
    #v(0.5em)
  ]
  if keywords != none [
    #set par(first-line-indent: 0pt)
    #text(weight: "bold")[关键词：] #keywords
  ]
  v(0.8em)
  line(length: 100%, stroke: rule)
  v(1.2em)
  outline(title: [目录], depth: 2)
  pagebreak()

  body
}

#let thick-table(columns, ..cells) = table(
  columns: columns,
  stroke: 0.45pt + light-line,
  inset: 6pt,
  fill: (x, y) => if y == 0 { rgb("#eef3f8") } else if calc.rem(y, 2) == 0 { rgb("#fbfcfe") } else { white },
  ..cells,
)

#let route-box(body, fill: soft) = box(
  width: 100%,
  inset: 7pt,
  stroke: 0.65pt + light-line,
  fill: fill,
  radius: 2pt,
  body,
)
