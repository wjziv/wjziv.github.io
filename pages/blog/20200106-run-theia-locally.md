title: Build Theia Locally on Linux
date: 2020-01-06
hero:
description: Browser-based IDE, compatible with VSCode add-ons.
tags:
    - How-to
    - Theia
    - IDE

Refer to the Theia build instructions:
https://theia-ide.org/docs/composing_applications/

AHEAD OF TIME, make sure that `yarn` is installed:
https://yarnpkg.com/lang/en/docs/install/#debian-stable

Upon running `yarn`...

These errors occurred:

```bash
warning @theia/typescript > @theia/filesystem > trash > xdg-trashdir > @sindresorhus/df > execa > cross-spawn-async@2.2.5: cross-spawn no longer requires a build toolchain, use it instead

warning @theia/git > @theia/scm > @types/p-debounce@1.0.1: This is a stub types definition. p-debounce provides its own type definitions, so you do not need this installed.

warning @theia/cli > @theia/application-manager > css-loader > cssnano > postcss-merge-rules > browserslist@1.7.7: Browserslist 2 could fail on reading Browserslist >3.0 config used in other tools.

warning @theia/cli > @theia/application-manager > css-loader > cssnano > autoprefixer > browserslist@1.7.7: Browserslist 2 could fail on reading Browserslist >3.0 config used in other tools.

warning @theia/cli > @theia/application-manager > webpack-cli > jscodeshift > babel-preset-es2015@6.24.1: 🙌  Thanks for using Babel: we recommend using babel-preset-env now: please read https://babeljs.io/env to update!

warning @theia/cli > @theia/application-manager > webpack-cli > webpack-addons > jscodeshift > babel-preset-es2015@6.24.1: 🙌  Thanks for using Babel: we recommend using babel-preset-env now: please read https://babeljs.io/env to update!

warning @theia/cli > @theia/application-manager > webpack-cli > jscodeshift > nomnom@1.8.1: Package no longer supported. Contact support@npmjs.com for more info.

warning @theia/cli > @theia/application-manager > webpack-cli > webpack-addons > jscodeshift > nomnom@1.8.1: Package no longer supported. Contact support@npmjs.com for more info.

warning @theia/cli > @theia/application-manager > css-loader > cssnano > postcss-merge-rules > caniuse-api > browserslist@1.7.7: Browserslist 2 could fail on reading Browserslist >3.0 config used in other tools.

warning @theia/cli > @theia/application-manager > css-loader > cssnano > postcss-merge-rules > postcss-selector-parser > flatten@1.0.2: I wrote this module a very long time ago; you should use something else.
```

Note:

This error was noted:
`.yarn-metadata.json: Unexpected end of JSON input".`

To fix this, run `yarn cache clean` to un-corrupt cache. Retry yarn install.

Add to the package.json file anything relevant:
http://taobao.mirrors.alibaba.ir/~theia


Note: This IDE is barebones and intended for use by somebody who likes to build further.

For personal development, look into code-server