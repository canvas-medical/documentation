# Canvas Documentation

## Features

**Improved workflow**
* Webpack working along with Jekyll
* BrowserSync live reload

**Optimized Style and SASS**
* SASS Style
* PostCSS Auto Preffixer
* CSS minified

**ES6 & Optimization**
* ES6 Babel
* JS minified and uglified
* ES Lint

**Images optimized**
* Imagemin, images optimizations

**Quick setup**
* Theme color in config
* Favicon generated automatically
* Google Analytics setup in config file (optional)
* Cookie consent setup in config file (optional)

**SEO Ready**
* SEO Plugin Jekyll
* Sitemap generated

**Progressive Web Apps (optional)**
* Generation of the Manifest
* Generation of Service worker


## Prerequisites
The following tools should be installed before starting:
* Ruby 3.1.x, Bunder 2.x
* Node 18.x

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

### Folder structure
```
.
├── 404.html
├── about.md
├── blog.md
├── config <--- This folder contains the different Webpack config files
│   ├── manifest.json <--- Please edit this file if you want a PWA
│   ├── postcss.config.js <--- Post css config
│   ├── sw.config.js <--- The service worker config file
│   ├── webpack.common.js <--- The common Webpack config file for all the environment
│   ├── webpack.dev.js <--- Dev Webpack environment config file
│   ├── webpack.prod.js <--- Prod Webpack environment config file
│   └── webpack.pwa.js
├── _config.yml <--- The Jekyll config file that you need to set up
├── Gemfile
├── Gemfile.lock
├── _images <--- Put all your images here, you will access them with this path /assets/images/
│   ├── icon.png <--- Replace this with your icon
│   └── large-icon.png <--- Replace this with your Facebook Open Graph picture
├── icon.png <--- Same with this one
├── _includes
├── index.md
├── _layouts
│   ├── blog.html
│   ├── home.html
│   ├── page.html
│   └── post.html
├── LICENSE
├── package.json <--- Update this file with your information especially the name which is used for the meta tags
├── README.md
├── _scss <--- Put your partials here
│   └── _default.scss
├── _src <--- This folder contains your JS and SASS entry points
│   ├── index.js
│   ├── index.scss
│   └── template
│       └── default.html <--- Here is the main default template, feel free to edit it but do not delete it
├── webpack.config.js
└── package-lock.json
```
You can see above the basic structure and the main differences with the official Jekyll folder structure

### Configurations
* The required configurations are all in `_config.yml`
* Also edit `package.json` the name is used in the meta tags
* If you want a `manifest.json` file please edit `config/manifest.json`
* Replace the different icon by yours in `_images` and in the root folder

### Assets
* SCSS partials should be located in `_scss` for better reading
* Put all your images in `_images` the content of this folder will be moved to the `_site/assets/images` so you can access them with this path `/assets/images/**` in your templates, check the examples
* Put all your Javascript files inside `_src` and import them from `index.js` or you can also add them as a new entry point in your webpack configuration file

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

## Other documentations
* [Jekyll](https://jekyllrb.com/)
* [Webpack](https://webpack.js.org/)
* [Jekyll SEO tag](https://github.com/jekyll/jekyll-seo-tag)
* [BrowserSync Webpack plugin](https://www.npmjs.com/package/browser-sync-webpack-plugin)
* [PostCSS](http://postcss.org/)
