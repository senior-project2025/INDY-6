document.addEventListener('DOMContentLoaded', function () {
    const loginBtn = document.getElementById('loginBtn');
    const loginModal = document.getElementById('loginModal');
    const closeLogin = document.getElementById('closeLogin');

    const menuBtn = document.getElementById('menuBtn');
    const sidebar = document.getElementById('sidebar');
    const closeSidebar = document.getElementById('closeSidebar');

    const langBtn = document.getElementById('langBtn');
    const langModal = document.getElementById('langModal');
    const closeLang = document.getElementById('closeLang');
    const langForm = document.getElementById('langForm'); 

    const searchInput = document.getElementById('faqSearch');
    const tutorialSearchInput = document.getElementById('tutorialSearch');
    const tutorialCards = document.querySelectorAll('.tutorial-card')
    // --- Login Modal ---
    if (loginBtn) loginBtn.addEventListener('click', () => loginModal.classList.add('show'));
    if (closeLogin) closeLogin.addEventListener('click', () => loginModal.classList.remove('show'));
    window.addEventListener('click', (e) => {
        if (e.target === loginModal) loginModal.classList.remove('show');
    });

    // --- Sidebar ---
    if (menuBtn) menuBtn.addEventListener('click', () => sidebar.classList.add('open'));
    if (closeSidebar) closeSidebar.addEventListener('click', () => sidebar.classList.remove('open'));
    sidebar.querySelectorAll('a').forEach(a => a.addEventListener('click', () => sidebar.classList.remove('open')));

    // --- Language Modal ---
    if (langBtn) langBtn.addEventListener('click', () => langModal.classList.add('show'));
    if (closeLang) closeLang.addEventListener('click', () => langModal.classList.remove('show'));
    window.addEventListener('click', (e) => {
        if (e.target === langModal) langModal.classList.remove('show');
    });

    // --- Language selection ---
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const lang = btn.getAttribute('data-lang');
            fetch(`/set_language/${lang}`).then(() => {
                const elementsToTranslate = Array.from(document.querySelectorAll('[data-i18n], [data-translate-key], .translate-text'))
                    .filter(el => !el.classList.contains('no-translate') && !el.hasAttribute('data-no-translate'));

                const items = elementsToTranslate.map(el => {
                    const key = el.getAttribute('data-translate-key') || el.getAttribute('data-i18n') || `text:${el.innerText.slice(0, 60)}`;
                    return { key: key, text: el.innerText };
                });

                fetch('/translate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ items: items, target_language: lang })
                })
                    .then(res => res.json())
                    .then(data => {
                        data.translated.forEach(item => {
                            let el = document.querySelector(`[data-translate-key="${item.key}"]`) || document.querySelector(`[data-i18n="${item.key}"]`);
                            if (!el) {
                                el = Array.from(document.querySelectorAll('.translate-text'))
                                    .find(e => e.innerText.trim().startsWith(item.translated_text.slice(0, 8)) === false);
                            }
                            if (el && !el.classList.contains('no-translate')) el.innerText = item.translated_text;
                        });
                    })
                    .catch(err => console.error('Translation error:', err));
            });
        });
    });

    // --- Reload page after language form submit ---
    if (langForm) {
        langForm.addEventListener('submit', () => {
            setTimeout(() => window.location.reload(), 100);
        });
    }

    // --- FAQ Accordion ---
    const faqItems = document.querySelectorAll(".faq-item");
    faqItems.forEach(item => {
        const question = item.querySelector(".faq-question");
        question.addEventListener("click", () => {
            // Option 1: allow multiple open
            item.classList.toggle("active");

            // Option 2: if you want only one open at a time, uncomment below:
            /*
            faqItems.forEach(other => {
                if (other !== item) other.classList.remove("active");
            });
            item.classList.add("active");
            */
        });
    });
    
    //FAQ Search bar function
        if (searchInput){
            searchInput.addEventListener('input', () => {
                const query = searchInput.value.toLowerCase();
                faqItems.forEach(item => {
                    const question = item.querySelector('.faq-question').textContent.toLowerCase();
                    const answer = item.querySelector('.faq-answer').textContent.toLowerCase();
                        // -- displays
                    if (question.includes(query) || answer.includes(query)) {
                item.style.display = '';
            }
                    else {
                        item.style.display = 'none';
                    }
                })
            })
        }
                //ios/android page search
                if (tutorialSearchInput){
                tutorialSearchInput.addEventListener('input', () => {
                const query = tutorialSearchInput.value.toLowerCase();
                
                tutorialCards.forEach(card => {
                const category = card.querySelector('h3').textContent.toLowerCase();
                const items = Array.from(card.querySelectorAll('li')).map(li => li.textContent.toLowerCase());
                const match = category.includes(query) || items.some(item => item.includes(query));
                        // -- displays
                    if (match) {
                        card.style.display = '';
                     }
                    else {
                        card.style.display = 'none';
                    }
                })
            })
        }
});
