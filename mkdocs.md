site_name: Documentation Portal

theme:
  name: material
  logo: logo.svg
  favicon: logo.svg
  features:
    - navigation.sections
    - navigation.expand
    - navigation.top
    - search.suggest
    - search.highlight
    - content.code.copy
  palette:
    - scheme: slate
      primary: blue
      accent: blue
      toggle:
        icon: fontawesome/solid/sun
        name: Switch to light mode
    - scheme: default
      primary: blue
      accent: blue
      toggle:
        icon: fontawesome/solid/moon
        name: Switch to dark mode

plugins:
  - search

extra_css:
  - styles.css

nav:
  - Home: index.md