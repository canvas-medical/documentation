# Canvas Medical Documentation

Canvas Medical documentation is a Jekyll static site generator combined with modern Webpack tooling that builds comprehensive developer documentation for the Canvas Medical platform, including SDK guides, FHIR API documentation, and implementation examples.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Prerequisites and Installation
- Install Ruby 3.2+ and Node.js 20+
- Install bundler for user: `gem install bundler --user-install`
- Add bundler to PATH: `export PATH="$PATH:/home/runner/.local/share/gem/ruby/3.2.0/bin"`
- Configure bundler for local install: `bundle config set --local path 'vendor/bundle'`

### Bootstrap, Build, and Test the Repository
- **Install dependencies** (NEVER CANCEL - long-running operations):
  - `yarn install` -- takes 5 minutes. NEVER CANCEL. Set timeout to 10+ minutes.
  - `bundle install` -- takes 2.5 minutes. NEVER CANCEL. Set timeout to 5+ minutes.
- **Build the production site**:
  - `yarn build` -- takes 12.5 minutes to complete. NEVER CANCEL. Set timeout to 20+ minutes.
  - Built website will be in `_site` folder
- **Serve built site for testing**:
  - `yarn serve:dist` -- serves on http://localhost:8081
- **Clean build artifacts**:
  - `yarn clean:project` -- removes `_site` and `assets` folders

### Development Server
- **Start development server** (NEVER CANCEL - long-running operations):
  - `yarn dev` -- takes 3-5 minutes to start. NEVER CANCEL. Set timeout to 10+ minutes.
  - Serves on multiple ports:
    - http://localhost:3000 (BrowserSync proxy with live reload)
    - http://localhost:4001 (Jekyll development server)
    - http://localhost:8080 (Webpack dev server)
    - http://localhost:3001 (BrowserSync UI)
- Always use http://localhost:3000 for development as it provides live reload

### Linting and Code Quality
- **JavaScript linting**:
  - `npx eslint _js/ --no-ignore` -- lints JavaScript files
  - `npx eslint _js/ --fix` -- auto-fixes linting issues where possible
- **Expected linting issues**: The codebase has many ESLint errors related to browser globals (document, window) and indentation. This is normal.

### Testing
- **Code block validation**: `./test-code-blocks.py` -- requires `uv` package manager and additional Python dependencies
- Testing is minimal in this repository; focus on build validation and manual testing

## Validation
- **ALWAYS manually validate** any documentation changes by running the development server and checking affected pages
- **ALWAYS run through complete scenarios** after making changes:
  1. Start development server: `yarn dev`
  2. Navigate to http://localhost:3000
  3. Test navigation between API, SDK, and Guides sections
  4. Verify search functionality works
  5. Check responsive design on different screen sizes
- **Build validation**: Always run `yarn build` to ensure production build succeeds before committing
- **Screenshot validation**: Take screenshots of key pages to verify visual changes

## Key Project Structure

### Repository Root
```
├── README.md                    # Project documentation
├── package.json                 # Node.js dependencies and scripts
├── Gemfile                      # Ruby dependencies
├── _config.yml                  # Main Jekyll configuration
├── _config_apikeys.yml          # API keys configuration
├── _config_production.yml       # Production overrides
├── webpack.config.js            # Webpack entry point
├── devbox.json                  # Devbox environment configuration
└── test-code-blocks.py          # Python script for testing code examples
```

### Source Directories
```
├── collections/                 # Jekyll collections for content
│   ├── _api/                   # FHIR API documentation
│   ├── _documentation/         # General documentation
│   ├── _guides/                # Implementation guides
│   ├── _release-notes/         # Product release notes
│   └── _sdk/                   # Canvas SDK documentation
├── pages/                      # Standalone pages
├── _includes/                  # Jekyll includes/partials
├── _layouts/                   # Jekyll layouts
├── _js/                        # JavaScript source files
├── _scss/                      # Sass/SCSS stylesheets
├── _images/                    # Image assets
├── _static/                    # Static assets
└── config/                     # Build configuration files
```

### Build Output
```
├── _site/                      # Built Jekyll site (git-ignored)
├── assets/                     # Compiled Webpack assets (git-ignored)
└── vendor/bundle/              # Ruby gems (git-ignored)
```

### Important Configuration Files
- `config/webpack.common.js` -- shared Webpack configuration
- `config/webpack.dev.js` -- development Webpack configuration  
- `config/webpack.prod.js` -- production Webpack configuration
- `.eslintrc.js` -- ESLint configuration
- `_config.yml` -- main Jekyll site configuration

## Common Tasks

### Adding New Documentation
1. **API documentation**: Add files to `collections/_api/`
2. **SDK documentation**: Add files to `collections/_sdk/`
3. **Implementation guides**: Add files to `collections/_guides/`
4. **Release notes**: Add files to `collections/_release-notes/YYYY/YYYY QX/`
5. Always include proper front matter with title, layout, and other metadata

### Modifying Styles
1. Edit SCSS files in `_scss/` directory
2. Main stylesheet entry point is `_src/index.scss`
3. Development server provides live reload for CSS changes

### Adding JavaScript Functionality
1. Add JavaScript files to `_js/` directory
2. Import new files in `_js/index.js`
3. Follow existing code patterns for DOM manipulation
4. Run ESLint to check for common issues

### Working with Images
1. Add images to `_images/` directory
2. Reference with path `/assets/images/filename.ext` in content
3. Images are automatically optimized during build

## Timing Expectations and Performance
- **yarn install**: ~5 minutes (includes node-sass compilation)
- **bundle install**: ~2.5 minutes (when using vendor/bundle)
- **yarn build**: ~12.5 minutes (full production build with optimizations)
- **yarn dev startup**: ~3-5 minutes (includes initial webpack build and Jekyll compilation)
- **Live reload**: ~1-3 seconds for CSS changes, ~5-10 seconds for content changes

## Troubleshooting

### Common Build Issues
- **Node-sass compilation errors**: Normal during yarn install, takes several minutes
- **Permission errors with bundler**: Use `--user-install` flag and configure PATH
- **Jekyll build warnings**: Liquid syntax warnings and empty slugs are expected
- **Webpack deprecation warnings**: Expected in current build, does not affect functionality

### Development Server Issues
- **Port conflicts**: Development server uses ports 3000, 4001, 8080, 3001
- **BrowserSync proxy errors**: Normal when running in headless environment
- **Asset loading failures**: Some CDN assets may be blocked, site still functional

### Performance Considerations
- **Large asset processing**: Build includes extensive image optimization
- **Memory usage**: Node-sass and Jekyll compilation can use significant memory
- **Concurrent processes**: Development server runs multiple processes simultaneously

## Critical Reminders
- **NEVER CANCEL builds or long-running commands** - Set timeouts of 20+ minutes for builds
- **Always export PATH** for bundler: `export PATH="$PATH:/home/runner/.local/share/gem/ruby/3.2.0/bin"`
- **Always configure bundler path**: `bundle config set --local path 'vendor/bundle'`
- **Always test manually** after making changes by running the development server
- **Always run production build** before committing to ensure no build breakage