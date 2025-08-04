// Copy share link functionality
function copyShareLink(chatId) {
    fetch(`/get_share_link/${chatId}`)
        .then(response => response.json())
        .then(data => {
            if (data.share_url) {
                document.getElementById('shareUrl').value = data.share_url;
                const modal = new bootstrap.Modal(document.getElementById('shareLinkModal'));
                modal.show();
            } else {
                alert('Error generating share link');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error generating share link');
        });
}

// Copy to clipboard functionality
function copyToClipboard() {
    const shareUrl = document.getElementById('shareUrl');
    shareUrl.select();
    shareUrl.setSelectionRange(0, 99999); // For mobile devices
    
    navigator.clipboard.writeText(shareUrl.value).then(function() {
        // Show success feedback
        const copyBtn = event.target.closest('button');
        const originalHTML = copyBtn.innerHTML;
        copyBtn.innerHTML = '<i class="bi bi-check"></i>';
        copyBtn.classList.remove('btn-outline-secondary');
        copyBtn.classList.add('btn-success');
        
        setTimeout(() => {
            copyBtn.innerHTML = originalHTML;
            copyBtn.classList.remove('btn-success');
            copyBtn.classList.add('btn-outline-secondary');
        }, 2000);
        
        // Show toast notification
        showToast('Link copied to clipboard!', 'success');
    }).catch(function(err) {
        console.error('Could not copy text: ', err);
        showToast('Failed to copy link', 'error');
    });
}

// Show toast notification
function showToast(message, type) {
    const toastContainer = document.getElementById('toastContainer') || createToastContainer();
    
    const toastHTML = `
        <div class="toast align-items-center text-bg-${type === 'success' ? 'success' : 'danger'} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    const toastElement = toastContainer.lastElementChild;
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

// Create toast container if it doesn't exist
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    document.body.appendChild(container);
    return container;
}

// Auto-resize textarea
document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.getElementById('chat_content');
    if (textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    }
});

// File upload handling for chat content
function handleFileUpload(event) {
    const file = event.target.files[0];
    if (file && file.type === 'text/plain') {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('chat_content').value = e.target.result;
            
            // Auto-fill title if empty
            const titleInput = document.getElementById('chat_title');
            if (!titleInput.value) {
                const filename = file.name.replace(/\.[^/.]+$/, "");
                titleInput.value = filename;
            }
        };
        reader.readAsText(file);
    } else {
        showToast('Please select a valid text file (.txt)', 'error');
    }
}

// Add file upload functionality if needed
document.addEventListener('DOMContentLoaded', function() {
    // Create file input for drag and drop
    const chatContent = document.getElementById('chat_content');
    if (chatContent) {
        // Add drag and drop functionality
        chatContent.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('border-primary');
        });
        
        chatContent.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.classList.remove('border-primary');
        });
        
        chatContent.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('border-primary');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                const file = files[0];
                if (file.type === 'text/plain') {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        chatContent.value = e.target.result;
                        
                        // Auto-fill title if empty
                        const titleInput = document.getElementById('chat_title');
                        if (!titleInput.value) {
                            const filename = file.name.replace(/\.[^/.]+$/, "");
                            titleInput.value = filename;
                        }
                    };
                    reader.readAsText(file);
                } else {
                    showToast('Please drop a valid text file (.txt)', 'error');
                }
            }
        });
    }
});
