/**
 * Home Credit 风险分析项目展示网站 — 交互脚本
 */

document.addEventListener('DOMContentLoaded', function() {
    // DOM 元素
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('section[id]');

    // ==========================================
    // 移动端菜单切换
    // ==========================================
    function openMenu() {
        sidebar.classList.add('open');
        overlay.classList.add('active');
        menuToggle.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeMenu() {
        sidebar.classList.remove('open');
        overlay.classList.remove('active');
        menuToggle.classList.remove('active');
        document.body.style.overflow = '';
    }

    menuToggle.addEventListener('click', function() {
        if (sidebar.classList.contains('open')) {
            closeMenu();
        } else {
            openMenu();
        }
    });

    overlay.addEventListener('click', closeMenu);

    // 点击导航链接后关闭菜单（移动端）
    navLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                closeMenu();
            }
        });
    });

    // ==========================================
    // 滚动时导航高亮
    // ==========================================
    function updateActiveNav() {
        const scrollPos = window.scrollY + 120;

        sections.forEach(function(section) {
            const top = section.offsetTop;
            const bottom = top + section.offsetHeight;
            const id = section.getAttribute('id');

            if (scrollPos >= top && scrollPos < bottom) {
                navLinks.forEach(function(link) {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === '#' + id) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }

    // 使用 requestAnimationFrame 优化滚动性能
    let ticking = false;
    window.addEventListener('scroll', function() {
        if (!ticking) {
            window.requestAnimationFrame(function() {
                updateActiveNav();
                ticking = false;
            });
            ticking = true;
        }
    });

    // 初始化
    updateActiveNav();

    // ==========================================
    // 图片懒加载优化（点击放大）
    // ==========================================
    const images = document.querySelectorAll('.image-card img');

    images.forEach(function(img) {
        img.addEventListener('click', function() {
            // 简单的点击放大效果
            if (img.classList.contains('zoomed')) {
                img.classList.remove('zoomed');
                img.style.transform = '';
                img.style.cursor = 'zoom-in';
            } else {
                // 移除其他图片的放大状态
                images.forEach(function(other) {
                    other.classList.remove('zoomed');
                    other.style.transform = '';
                    other.style.cursor = 'zoom-in';
                });

                img.classList.add('zoomed');
                img.style.cursor = 'zoom-out';
            }
        });

        img.style.cursor = 'zoom-in';
        img.style.transition = 'transform 0.3s ease';
    });

    // ==========================================
    // 窗口大小改变处理
    // ==========================================
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            closeMenu();
        }
    });

    // ==========================================
    // 平滑滚动 polyfill（兼容旧浏览器）
    // ==========================================
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offset = window.innerWidth <= 768 ? 60 : 0;
                const top = target.offsetTop - offset;
                window.scrollTo({
                    top: top,
                    behavior: 'smooth'
                });
            }
        });
    });

    // ==========================================
    // 入场动画（Intersection Observer）
    // ==========================================
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('in-view');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // 为卡片添加动画类
    document.querySelectorAll('.card, .image-card, .feature-card, .model-card, .feature-item').forEach(function(el) {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(el);
    });

    // CSS 动画类
    const style = document.createElement('style');
    style.textContent = `
        .in-view {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
    `;
    document.head.appendChild(style);

    console.log('Home Credit Project Website loaded successfully');
});
