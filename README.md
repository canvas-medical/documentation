# Canvas Documentation

## Requirements
* Ruby 3.1.x, Bunder 2.x
* Node >16, Yarn 3.x

## Quick start

Install dependencies
```sh
yarn install
bundle install
```

Start development server
```
yarn start
```

## Development
To start the development server just run  `yarn start`

### Configuration
* The required configurations are in `_config.yml`
* Also edit `package.json` as the name is used in the meta tags
* If the `manifest.json` is used, please edit `config/manifest.json`

### Assets
* SCSS partials should be located in `_scss` for better reading
* Images should be in `_images` and the content of this folder will be moved to the `_site/assets/images` so you can access them with this path `/assets/images/**` 
* Javascript files are saved in `_src` and import them from `index.js` or you can also add them as a new entry point in your webpack configuration file

## Build

### Optimized website
To build the website run the following line

```sh
npm run build
```
The built website will be in `_site` folder.

You can also run a local server to test it with this command
```sh
npm run serve:dist
```

### PWA
If you want to build a PWA (including the manifest.json and the service worker) run the following. Please ensure to have configured this file `config/manifest.json`
The built website will be in `_site` folder.
```sh
npm run build:pwa
```

### Clean assets & \_site folders
This will remove the generated folders
```sh
npm run clean:project
```
