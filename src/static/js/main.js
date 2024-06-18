// main.js
document.addEventListener("DOMContentLoaded", () => {
    // Xử lý sự kiện cho logo để chuyển hướng về trang home.html
    if (document.getElementById('logo-frame')) {
        const logoFrame = document.getElementById('logo-frame');
        logoFrame.addEventListener('click', () => {
        window.location.href = '/';
        });
    }

    // Xử lý ẩn hiện confidence score
    if (document.querySelector('.toggle')) {
      const toggle = document.querySelector('.toggle');
      const togglePlaceholder = toggle.querySelector('.toggle-placeholder');
      togglePlaceholder.style.display = 'block';
      const confScore = toggle.querySelector('.confidence-score');
      confScore.style.display = 'none';
      toggle.addEventListener('click', () => {
        const temp = togglePlaceholder.style.display;
        console.log(togglePlaceholder.style.display);
        togglePlaceholder.style.display = confScore.style.display;
        confScore.style.display = temp;
      });
  }

    // Kiểm tra nếu đang ở trang home.html
    if (document.getElementById('read-more')) {
        const readMore = document.getElementById('read-more');
        const aboutUsSection = document.getElementById('about-us-section');
      
        // Thêm sự kiện click vào "Read more"
        readMore.addEventListener('click', function() {
          // Lấy tọa độ Y của phần "About" so với đầu trang
          const aboutUsPosition = aboutUsSection.getBoundingClientRect().top;
      
          // Cuộn trang mượt mà đến phần "About us"
          window.scrollTo({
            top: aboutUsPosition,
            behavior: 'smooth'
          });
        });
      }      
    // Kiểm tra nếu đang ở trang upload.html
    if (document.getElementById('dropZone')) {
      const dropZone = document.getElementById('dropZone');
      const fileInput = document.getElementById('fileInput');
      const submitBtn = document.getElementById('submitBtn');
      var loader = document.querySelector('.loader-container')
      const customCombobox = document.querySelector('.custom-combobox')

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
        // an drop zone va hien loader
        dropZone.style.display = 'none'; 
        customCombobox.style.display = 'none';
        loader.style.display = 'flex';
      });
  
      // Mở hộp thoại chọn file khi click vào drop zone
      dropZone.addEventListener('click', () => {
        fileInput.click();
      });
  
      // Tự động submit form khi file được chọn
      fileInput.addEventListener('change', () => {
        submitBtn.click();
        dropZone.style.display = 'none'; 
        customCombobox.style.display = 'none';
        loader.style.display = 'flex';
      });
    }
    // Xử lý sự kiện cho trang result.html
    if (document.getElementById('image-box')) {
        const imageBox = document.getElementById('image-box');
        const infoBox = document.getElementById('info');
        const fileInput = document.getElementById('fileInput');
        const uploadForm = document.getElementById('uploadForm');
        const customCombobox = document.querySelector('.custom-combobox')
        var loader = document.querySelector('.loader-container')

        imageBox.addEventListener('click', () => {
        // Kích hoạt hộp thoại chọn file
            fileInput.click();
        });

        fileInput.addEventListener('change', () => {
        // Tự động submit form khi file được chọn
            uploadForm.submit();
        // an drop zone va hien loader
            imageBox.style.display = 'none'; 
            infoBox.style.display = 'none';
            customCombobox.style.display = 'none';
            loader.style.display = 'flex';
        });
    }
  });
  