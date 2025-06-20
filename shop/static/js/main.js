var swiper = new Swiper(".mySwiper", {
    loop: true,
    spaceBetween: 10,
    slidesPerView: 4,
    freeMode: true,
    watchSlidesProgress: true,
});
var swiper2 = new Swiper(".mySwiper2", {
    loop: true,
    spaceBetween: 10,
    navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
    },
    thumbs: {
        swiper: swiper,
    },
});


document.addEventListener("DOMContentLoaded", () => {
    const slides = document.querySelectorAll(".slider__image");
    const paginators = document.querySelectorAll(".slider__paginator");
    const [nextBtn, prevBtn] = document.querySelectorAll(".slider__button");

    let currentIndex = 0;

    function showSlide(index) {
        if (index < 0) index = slides.length - 1;
        if (index >= slides.length) index = 0;
        currentIndex = index;

        slides.forEach((slide, i) => {
            slide.classList.toggle("slider__image_active", i === index);
        });

        paginators.forEach((pag, i) => {
            pag.classList.toggle("slider__paginator_active", i === index);
        });
    }

    nextBtn.addEventListener("click", () => showSlide(currentIndex - 1));
    prevBtn.addEventListener("click", () => showSlide(currentIndex + 1));

    paginators.forEach((paginator, index) => {
        paginator.addEventListener("click", () => showSlide(index));
    });

    showSlide(0); // начальный слайд
});