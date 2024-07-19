function applyFilters() {
    const category = document.getElementById('category').value.toLowerCase();
    const year = document.getElementById('year').value;
    const title = document.getElementById('title').value.toLowerCase();
    const price = document.getElementById('price').value;

    const books = document.querySelectorAll('.book');

    books.forEach(book => {
        const bookCategory = book.getAttribute('data-category').toLowerCase();
        const bookYear = book.getAttribute('data-year');
        const bookTitle = book.getAttribute('data-title').toLowerCase();
        const bookPrice = book.getAttribute('data-price');

        let categoryMatch = category ? bookCategory === category : true;
        let yearMatch = year ? bookYear === year : true;
        let titleMatch = title ? bookTitle.includes(title) : true;
        let priceMatch = price ? bookPrice <= price : true;

        if (categoryMatch && yearMatch && titleMatch && priceMatch) {
            book.style.display = 'block';
        } else {
            book.style.display = 'none';
        }
    });
}
