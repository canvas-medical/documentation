# Canvas Documentation

## Requirements
* Ruby 3.1.x, Bundler 2.x
* Node >16, Yarn 3.x

## Quick start

### With Devbox

[![Built with Devbox](https://jetpack.io/img/devbox/shield_galaxy.svg)](https://jetpack.io/devbox/docs/contributor-quickstart/)

1. [Install Devbox](https://www.jetpack.io/devbox/docs/contributor-quickstart/#install-devbox)
2. Run `devbox run dev`

### Manually

Install dependencies
```sh
yarn install
bundle install
```

Start development server
```
yarn dev
```

## Development
To start the development server just run  `yarn dev`

### Configuration
* The required configurations are in `_config.yml`
* Also edit `package.json` as the name is used in the meta tags
* If the `manifest.json` is used, please edit `config/manifest.json`

### Assets
* SCSS partials should be located in `_scss` for better reading
* Images should be in `_images` and the content of this folder will be moved to the `_site/assets/images` so you can access them with this path `/assets/images/**`
* Javascript files are saved in `_js` and import them from `index.js` or you can also add them as a new entry point in your webpack configuration file

## Build

### Optimized website
To build the website run the following line

```sh
yarn build
```
The built website will be in `_site` folder.

You can also run a local server to test it with this command
```sh
yarn serve:dist
```

### PWA
If you want to build a PWA (including the manifest.json and the service worker) run the following. Please ensure to have configured this file `config/manifest.json`
The built website will be in `_site` folder.
```sh
yarn build:pwa
```

### Clean assets & \_site folders
This will remove the generated folders
```sh
yarn clean:project
```

### Update Algolia search index

Run this command to update Algolia's search index:
```sh
ALGOLIA_API_KEY='admin_api_key' bundle exec jekyll algolia --config _config.yml,_config_apikeys.yml
```
