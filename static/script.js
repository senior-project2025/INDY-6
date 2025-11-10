document.addEventListener('DOMContentLoaded', function(){
  const loginBtn = document.getElementById('loginBtn');
  const loginModal = document.getElementById('loginModal');
  const closeLogin = document.getElementById('closeLogin');
  const menuBtn = document.getElementById('menuBtn');
  const sidebar = document.getElementById('sidebar');
  const closeSidebar = document.getElementById('closeSidebar');

  if (loginBtn) loginBtn.addEventListener('click', () => loginModal.style.display = 'flex');
  if (closeLogin) closeLogin.addEventListener('click', () => loginModal.style.display = 'none');
  window.addEventListener('click', (e) => {
    if (e.target === loginModal) loginModal.style.display = 'none';
  });

  if (menuBtn) menuBtn.addEventListener('click', () => sidebar.classList.add('open'));
  if (closeSidebar) closeSidebar.addEventListener('click', () => sidebar.classList.remove('open'));
  // close when clicking a link
  sidebar.querySelectorAll('a').forEach(a => a.addEventListener('click', () => sidebar.classList.remove('open')));
});

//faq questions
document.addEventListener('DOMContentLoaded', () => {
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        question.addEventListener('click', () => {
            const wasOpen = item.classList.contains('open');
            faqItems.forEach(i => i.classList.remove('open'));
            if (!wasOpen) {
                item.classList.add('open');
            }
        });
    });
});
