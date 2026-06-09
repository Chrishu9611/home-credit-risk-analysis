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
    // 图片 Lightbox 放大查看器
    // ==========================================
    (function() {
        // 创建 Lightbox DOM
        var overlay = document.createElement('div');
        overlay.className = 'lightbox-overlay';
        overlay.innerHTML =
            '<div class="lightbox-content">' +
                '<button class="lightbox-close" aria-label="关闭">&times;</button>' +
                '<img class="lightbox-img" src="" alt="">' +
                '<div class="lightbox-caption"></div>' +
            '</div>' +
            '<div class="lightbox-hint">按 ESC 或点击任意处关闭</div>';
        document.body.appendChild(overlay);

        var lightboxImg = overlay.querySelector('.lightbox-img');
        var lightboxCaption = overlay.querySelector('.lightbox-caption');
        var closeBtn = overlay.querySelector('.lightbox-close');

        function openLightbox(img) {
            lightboxImg.src = img.src;
            lightboxImg.alt = img.alt || '';

            // 尝试从相邻的 caption 获取标题
            var card = img.closest('.image-card');
            if (card) {
                var captionEl = card.querySelector('.image-caption');
                lightboxCaption.textContent = captionEl ? captionEl.textContent.trim() : '';
                lightboxCaption.style.display = captionEl ? 'block' : 'none';
            }

            overlay.classList.add('active');
            document.body.classList.add('lightbox-open');
        }

        function closeLightbox() {
            overlay.classList.remove('active');
            document.body.classList.remove('lightbox-open');
            // 延迟清空图片，避免关闭动画时闪烁
            setTimeout(function() {
                lightboxImg.src = '';
            }, 300);
        }

        // 绑定所有图片卡片
        var images = document.querySelectorAll('.image-card img');
        images.forEach(function(img) {
            img.addEventListener('click', function(e) {
                e.preventDefault();
                openLightbox(img);
            });
        });

        // 关闭事件
        closeBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            closeLightbox();
        });

        overlay.addEventListener('click', function(e) {
            if (e.target === overlay) {
                closeLightbox();
            }
        });

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && overlay.classList.contains('active')) {
                closeLightbox();
            }
        });
    })();

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
