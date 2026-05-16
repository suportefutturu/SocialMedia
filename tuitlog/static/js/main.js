// Tuitlog — JavaScript Minimalista e Discreto

document.addEventListener('DOMContentLoaded', function() {
    
    // =========================================================================
    // DROPDOWN DE COMPARTILHAMENTO
    // =========================================================================
    const shareButtons = document.querySelectorAll('.share-toggle');
    
    shareButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation();
            const menu = this.nextElementSibling;
            const isActive = menu.classList.contains('active');
            
            // Fechar todos os outros menus
            document.querySelectorAll('.share-menu').forEach(m => {
                if (m !== menu) m.classList.remove('active');
            });
            
            menu.classList.toggle('active', !isActive);
        });
    });
    
    // Fechar menus ao clicar fora
    document.addEventListener('click', function() {
        document.querySelectorAll('.share-menu').forEach(menu => {
            menu.classList.remove('active');
        });
    });
    
    // =========================================================================
    // UPLOAD DRAG & DROP
    // =========================================================================
    const uploadArea = document.querySelector('.upload-area');
    const fileInput = document.getElementById('image-upload');
    const preview = document.getElementById('upload-preview');
    
    if (uploadArea && fileInput) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, preventDefaults, false);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.add('dragover');
            }, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.remove('dragover');
            }, false);
        });
        
        uploadArea.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            
            if (files.length > 0) {
                fileInput.files = files;
                handleFiles(files[0]);
            }
        }, false);
        
        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });
        
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                handleFiles(this.files[0]);
            }
        });
        
        function handleFiles(file) {
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                };
                reader.readAsDataURL(file);
            }
        }
    }
    
    // =========================================================================
    // AUTO-HIDE FLASH MESSAGES
    // =========================================================================
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.transition = 'all 0.3s ease';
            message.style.opacity = '0';
            message.style.transform = 'translateX(100%)';
            setTimeout(() => message.remove(), 300);
        }, 5000);
    });
    
    // =========================================================================
    // CONFIRMAÇÃO DE EXCLUSÃO DE COMENTÁRIO
    // =========================================================================
    const deleteCommentButtons = document.querySelectorAll('.comment-delete-btn');
    
    deleteCommentButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Tem certeza que deseja excluir este comentário?')) {
                e.preventDefault();
            }
        });
    });
    
    // =========================================================================
    // LAZY LOADING PARA IMAGENS
    // =========================================================================
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('loading');
                    observer.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
    
    // =========================================================================
    // FORMULÁRIO DE COMENTÁRIO - PREVENIR SUBMISSÃO VAZIA
    // =========================================================================
    const commentForm = document.querySelector('.comment-form form');
    
    if (commentForm) {
        commentForm.addEventListener('submit', function(e) {
            const textarea = this.querySelector('textarea[name="text"]');
            if (textarea && textarea.value.trim() === '') {
                e.preventDefault();
                textarea.focus();
                textarea.style.borderColor = 'var(--color-error)';
                setTimeout(() => {
                    textarea.style.borderColor = '';
                }, 2000);
            }
        });
    }
    
    // =========================================================================
    // CONTADOR DE CARACTERES PARA LEGENDA
    // =========================================================================
    const captionTextarea = document.querySelector('textarea[name="caption"]');
    
    if (captionTextarea) {
        const maxLength = 500;
        const counter = document.createElement('div');
        counter.className = 'caption-counter';
        counter.style.cssText = 'font-size: 0.75rem; color: var(--color-text-muted); text-align: right; margin-top: 0.5rem;';
        counter.textContent = `0/${maxLength}`;
        
        captionTextarea.maxLength = maxLength;
        captionTextarea.parentNode.appendChild(counter);
        
        captionTextarea.addEventListener('input', function() {
            counter.textContent = `${this.value.length}/${maxLength}`;
        });
    }
    
});
