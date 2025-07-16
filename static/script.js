// --- Select2 og butikkvalg ---
function getStoreFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('butikk') || '';
}

function applyActiveStoreFromURL($butikkVelger) {
    const butikk = getStoreFromURL();
    if (butikk) {
        $butikkVelger.val(butikk).trigger('change.select2');
    }
}

function setStore() {
    const valgtButikk = $('#butikk-velger').val();
    const params = new URLSearchParams(window.location.search);

    if (params.get('butikk') === valgtButikk) return;

    params.delete('side');
    params.set('butikk', valgtButikk);
    window.location.href = `${window.location.pathname}?${params.toString()}`;
}


// --- Produktsøk ---
document.addEventListener('DOMContentLoaded', () => {
    const $butikkVelger = $('#butikk-velger');

    if ($butikkVelger.length) {
        $butikkVelger.select2({
            placeholder: "Velg butikk...",
            width: 'style'
        });

        $butikkVelger.on('select2:open', function () {
            let searchBox = document.querySelector('.select2-container--open .select2-search__field');
            if (searchBox) searchBox.focus();
        });

        applyActiveStoreFromURL($butikkVelger);
        $butikkVelger.on('change', setStore);
    }

    const params = new URLSearchParams(window.location.search);
    const søkeverdi = params.get('produkt_sok');
    const søkefelt = document.getElementById('produkt-sok');
    if (søkefelt && søkeverdi) {
        søkefelt.value = søkeverdi;
    }

    const søkeskjema = document.getElementById('produkt-sok-skjema');
    if (søkeskjema) {
        søkeskjema.addEventListener('submit', function (e) {
            e.preventDefault();
            const søkeverdi = søkefelt.value;
            if (søkeverdi) {
                params.delete('produkt');
                params.delete("side");
                params.set('produkt_sok', søkeverdi);
            } else {
                params.delete('produkt_sok');
            }
            window.location.href = `/?${params.toString()}`;
        });
    }
});
