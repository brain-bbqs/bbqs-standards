# BBQS Standards

> [!WARNING]
> **This repository is in active development.** It is a port of the BBQS Standards Working
> Group documents, and the content has not been fully validated yet. Until this repository
> is officially released, the Google Docs linked below remain the current documents.

Documents of the [BBQS Working Group on Data Standards](https://brain-bbqs.org/working-groups/standards/),
maintained as Markdown so that changes can be reviewed and versioned in Git.

| Document | Source |
| --- | --- |
| [Guidelines for BBQS Data Standards](content/guidelines/index.md) | `content/guidelines/` |
| [Charter: BBQS DCAIC Working Group on Data Standards](content/charter/index.md) | `content/charter/` |

These documents were originally drafted in Google Docs
([guidelines](https://docs.google.com/document/d/1vIJ01La9G76FfGywS3IbG4o1GR4qquS31MoJ2B4_4os/edit),
[charter](https://docs.google.com/document/d/1WIVI8HZF4-IfZZ61UjCZx2K7NyYx_CaTuIHmhFo7eYw/edit)).
Once this repository is released, it becomes the source of truth and the Google Docs will
be retired.

## Repository layout

```
content/              # the documents; everything the website renders lives here
  charter/            # one folder per document
    index.md
  guidelines/
    index.md
    figures/
      guidelines-figures.pptx       # editable source for all figures
      data-standards-overview.svg   # Figure 1, rendered from the .pptx
scripts/check_docs.py # checks the conventions below (runs in CI on every PR)
```

## On the BBQS website

Once released, the documents will be published at
<https://brain-bbqs.org/working-groups/standards>. The website ([brain-bbqs/bbqs-app](https://github.com/brain-bbqs/bbqs-app)) downloads
`content/` from `main` of this repository every time it builds (on each deploy and at
least once a day), so merged changes appear on the site within a day. Nothing needs to be
changed in the website repository to update or add a document.

On the website side, `scripts/fetch-standards-docs.mjs` does the download and
`src/pages/StandardsDoc.tsx` renders the pages. To preview your edits in the site before
merging, run this from a checkout of `bbqs-app`:

```bash
BBQS_STANDARDS_PATH=/path/to/bbqs-standards npm run dev
```

and open <http://localhost:8080/working-groups/standards>.

## Checking documents

Because the website follows `main` directly, every pull request runs
`scripts/check_docs.py`. It checks that each document has the required front matter, that
relative links and images point to existing files, and that there is no raw HTML. To run it
locally:

```bash
pip install pyyaml
python scripts/check_docs.py
```

## Editing guidelines

- Each document is a folder `<name>/` containing an `index.md`. Keep figures in a
  `figures/` subfolder next to it and reference them with a relative path, e.g.
  `![alt text](figures/figure.svg)`.
- Each document starts with front matter. Keep every field on a single `key: value`
  line (the website does not parse multi-line YAML):

  ```yaml
  ---
  title: "Guidelines for BBQS Data Standards"   # page title
  short_title: Data Standards Guidelines        # label for navigation and links
  description: One sentence shown in listings.
  order: 1                                      # position in listings
  ---
  ```

  The page title comes from `title`, so do not add a `# Title` heading to the body;
  start sections at `##`.
- Use plain GitHub-flavored Markdown, without raw HTML or site-specific syntax, so the
  files read the same on GitHub and on the website.
- Wrap placeholders such as `<subject_id>` in backticks; otherwise they are treated as
  HTML tags and disappear.

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
  this repository instead of a copy published with the website.

