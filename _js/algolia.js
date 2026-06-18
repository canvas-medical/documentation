import { algoliaId, algoliaIndex, algoliaSearchKey } from './apikeys';

window.addEventListener('load', () => {
    const searchClient = algoliasearch(algoliaId, algoliaSearchKey);
    const inputclear = document.querySelector('.ais-SearchBox-input');

    const search = instantsearch({
        indexName: algoliaIndex,
        searchClient,

        searchFunction(helper) {
            const searchResults = document.getElementById('search_container');
            if (helper.state.query === '' && searchResults.style.display === 'none' && overlay.style.display === 'none') {
                return;
            }
            searchResults.style.display = helper.state.query ? 'grid ' : 'none';

            helper.search();
        },
    });
    const refinementWidget = instantsearch.widgets.refinementList({
        container: '#refinementlist',
        attribute: 'collection',
    });

    let timerId;
    search.addWidget(
        instantsearch.widgets.searchBox({
            container: '#algolia-search',
            placeholder: 'Search',
            showLoadingIndicator: true,
            queryHook(query, refine) {
                clearTimeout(timerId);
                timerId = setTimeout(() => refine(query), 500);
            },
        }),
    );
    search.addWidget(
        instantsearch.widgets.hits({
            container: '#algolia-results',

            templates: {
                item(hit, { html, components }) {
                    return html `
            <div class="post-item">            
            ${components.Highlight({ attribute: 'name', hit })}
              <a class="post-link" href="${hit.url}">
              <div class="post-title-container"> 
                <div class="post-title">${hit.title}</div>
                <div class="post-collection">${hit.collection}</div>
              </div>
              <div class="post-snippet"><p>${hit.content}</p></div>
              </a>
              
            </div>

              
            `;
                },
            },
        }),
    );

    search.addWidget(
        instantsearch.widgets.pagination({
            container: '#pagination',
            maxPages: 20,
            // default is to scroll to 'body', we disable this behavior
            scrollTo: false,
            showFirstLast: false,
        }),
    );

    search.addWidgets([refinementWidget]);

    search.start();
});