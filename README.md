# bbqs-standards

Documents of the [BBQS Working Group on Data Standards](https://brain-bbqs.org/working-groups/standards/),
maintained as Markdown so that changes can be reviewed and versioned in Git.

| Document | Source |
| --- | --- |
| [Guidelines for BBQS Data Standards](content/guidelines/index.md) | `content/guidelines/` |
| [Charter: BBQS DCAIC Working Group on Data Standards](content/charter/index.md) | `content/charter/` |

These documents were originally drafted in Google Docs
([guidelines](https://docs.google.com/document/d/1vIJ01La9G76FfGywS3IbG4o1GR4qquS31MoJ2B4_4os/edit),
[charter](https://docs.google.com/document/d/1WIVI8HZF4-IfZZ61UjCZx2K7NyYx_CaTuIHmhFo7eYw/edit)).
This repository is now the source of truth.

## Repository layout

```
content/              # Hugo content; everything the website renders lives here
  _index.md           # landing page for the section
  charter/            # one folder per document ("page bundle")
    index.md
  guidelines/
    index.md
    figures/
      guidelines-figures.pptx       # editable source for all figures
      data-standards-overview.svg   # Figure 1, rendered from the .pptx
hugo.yaml             # Hugo module config (exposes content/ to importing sites)
go.mod                # Hugo module definition
```

## Rendering on the BBQS website

The website ([brain-bbqs.github.io](https://github.com/brain-bbqs/brain-bbqs.github.io))
is built with Hugo and the Hextra theme, which is pulled in as a Hugo module. This
repository is also a Hugo module, so the website can import it the same way and choose
where the documents appear. In the website's `hugo.yaml`:

```yaml
module:
  imports:
  - path: github.com/imfing/hextra
  - path: github.com/brain-bbqs/bbqs-standards
    mounts:
      - source: content
        target: content/standards   # pages are served at /standards/...
```

then run `hugo mod get github.com/brain-bbqs/bbqs-standards` to record the version in the
website's `go.mod`/`go.sum`. To pick up new changes, run
`hugo mod get -u github.com/brain-bbqs/bbqs-standards` in the website repository.

### Previewing changes locally

From a checkout of the website, point the module at your local copy of this repository:

```bash
HUGO_MODULE_REPLACEMENTS="github.com/brain-bbqs/bbqs-standards -> /path/to/bbqs-standards" \
  hugo server
```

and open <http://localhost:1313/standards/>.

## Editing guidelines

- Each document starts with YAML front matter (`title`, `linkTitle`, `weight`, ...). The
  page title comes from `title`, so do not add a `# Title` heading to the body; start
  sections at `##`.
- Each document is a folder `<name>/` containing an `index.md` (a Hugo "page bundle";
  the file must be named `index.md` for Hugo to publish the page together with its
  figures). Keep figures in a `figures/` subfolder next to it and reference them with a
  relative path, e.g. `![alt text](figures/figure.svg)`. This works both on GitHub and on
  the website. No other configuration is needed to add a new document.
- Use plain GitHub-flavored Markdown. Avoid Hugo shortcodes so the files stay readable on
  GitHub.
- Wrap placeholders such as `<subject_id>` in backticks; otherwise they are treated as
  raw HTML on the website.

### Figures

Figures are kept as an editable source file plus a rendered SVG for display:

- `figures/*.pptx` is the source. Edit it in PowerPoint, Keynote, or Google Slides
  (*File > Import slides* / *File > Download > Microsoft PowerPoint*).
- `figures/*.svg` is the rendered version included in the document. After changing a
  slide, re-export it as SVG and replace the file. In Google Slides use
  *File > Download > Scalable Vector Graphics (.svg)* (exports the current slide); in
  PowerPoint use *File > Export* or *Save as Picture* with SVG.
- Use one slide per figure and name the SVG after its content (not its figure number), so
  figures can be reordered without renaming files.
- Commit the `.pptx` and `.svg` together so they stay in sync.
- In figure captions, link to the source file on GitHub
  (`https://github.com/brain-bbqs/bbqs-standards/blob/main/content/<doc>/figures/<file>.pptx`)
  rather than with a relative path, so readers of the website are sent to the version in
  this repository instead of a copy published by Hugo.

