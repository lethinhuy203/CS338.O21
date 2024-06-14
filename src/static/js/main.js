// main.js

document.addEventListener("DOMContentLoaded", () => {
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const submitBtn = document.getElementById('submitBtn');

    // Thêm lớp dragover khi file được kéo vào
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    // Bỏ lớp dragover khi file được kéo ra
    dropZone.addEventListener('dragleave', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
    });

    // Xử lý khi file được thả vào drop zone
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            submitBtn.click(); // Tự động submit form khi file được thả vào
        }
    });

    // Mở hộp thoại chọn file khi click vào drop zone
    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    // Tự động submit form khi file được chọn
    fileInput.addEventListener('change', () => {
        submitBtn.click();
    });
});
