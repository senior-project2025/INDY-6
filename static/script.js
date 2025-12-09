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
    const tutorialCards = document.querySelectorAll('.tutorial-card');

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

    // --- NEW LANGUAGE SELECTION (clean + animated reload) ---
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const lang = btn.getAttribute('data-lang');
            const overlay = document.getElementById('loadingOverlay');

            // Show loading overlay + fade animation
            overlay.style.display = "flex";
            document.body.classList.add("fade-out");

            // Update language server-side
            await fetch(`/set_language/${lang}`);

            // Smooth transition then reload
            setTimeout(() => {
                window.location.reload();
            }, 350);
        });
    });

    // (Optional old form submit reload — keep it safe)
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
            item.classList.toggle("active");
        });
    });

    // FAQ Search
    if (searchInput) {
        searchInput.addEventListener('input', () => {
            const query = searchInput.value.toLowerCase();
            faqItems.forEach(item => {
                const question = item.querySelector('.faq-question').textContent.toLowerCase();
                const answer = item.querySelector('.faq-answer').textContent.toLowerCase();
                if (question.includes(query) || answer.includes(query)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }

    // iOS/Android tutorial search
    if (tutorialSearchInput) {
        tutorialSearchInput.addEventListener('input', () => {
            const query = tutorialSearchInput.value.toLowerCase();

            document.querySelectorAll('.tutorial-card').forEach(card => {
                const videos = card.querySelectorAll('.video-card');
                let anyMatch = false;

                videos.forEach(video => {
                    const title = video.querySelector('.video-title').textContent.toLowerCase();
                    if (title.includes(query)) {
                        video.style.display = "";
                        anyMatch = true;
                    } else {
                        video.style.display = "none";
                    }
                });

                card.style.display = anyMatch ? "" : "none";
            });
        });
    }


    // --- DARK MODE ---
    const themeSwitch = document.getElementById('theme-switch');
    const themeIcon = themeSwitch?.querySelector('.theme-icon');
    const themeText = themeSwitch?.querySelector('.theme-text');

    const applyDarkModeUI = () => {
        if (!themeIcon || !themeText) return;
        const isDark = document.documentElement.classList.contains('darkmode');
        themeIcon.textContent = isDark ? "☀️" : "🌙";
        themeText.textContent = isDark ? "Light mode" : "Dark mode";
    };

    const enableDarkmode = () => {
        document.documentElement.classList.add('darkmode');
        localStorage.setItem('darkmode', 'active');
        applyDarkModeUI();
    };

    const disableDarkmode = () => {
        document.documentElement.classList.remove('darkmode');
        localStorage.setItem('darkmode', 'inactive');
        applyDarkModeUI();
    };

    let darkmode = localStorage.getItem('darkmode');
    if (darkmode === "active") {
        enableDarkmode();
    } else {
        applyDarkModeUI();
    }

    if (themeSwitch) {
        themeSwitch.addEventListener('click', () => {
            const isDark = document.documentElement.classList.contains('darkmode');
            isDark ? disableDarkmode() : enableDarkmode();
        });
    }

    // --- VIDEO MODAL ---
    const videoModal = document.getElementById("videoModal");
    const tutorialVideo = document.getElementById("tutorialVideo");
    const closeVideo = document.querySelector(".close-video");

    document.querySelectorAll(".video-card").forEach(card => {
        card.addEventListener("click", () => {
            const src = card.getAttribute("data-video");
            tutorialVideo.src = src;
            videoModal.classList.add("show");
            tutorialVideo.play();
        });
    });

    closeVideo.addEventListener("click", () => {
        tutorialVideo.pause();
        tutorialVideo.currentTime = 0;
        videoModal.classList.remove("show");
    });

    videoModal.addEventListener("click", (e) => {
        if (e.target === videoModal) {
            tutorialVideo.pause();
            tutorialVideo.currentTime = 0;
            videoModal.classList.remove("show");
        }
    });
});
