// Simple carousel implementation
const carousel = document.querySelector('.carousel');
let isDown = false;
let startX;
let scrollLeft;

carousel.addEventListener('mousedown', (e) => {
  isDown = true;
  startX = e.pageX - carousel.offsetLeft;
  scrollLeft = carousel.scrollLeft;
});

carousel.addEventListener('mouseleave', () => {
  isDown = false;
});

carousel.addEventListener('mouseup', () => {
  isDown = false;
});

carousel.addEventListener('mousemove', (e) => {
  if (!isDown) return;
  e.preventDefault();
  const x = e.pageX - carousel.offsetLeft;
  const walk = (x - startX) * 3; // Scroll speed
  carousel.scrollLeft = scrollLeft - walk;
});

// Hero text animation
const heroText = document.querySelector('.hero-content h1');
setTimeout(() => {
  heroText.style.opacity = '1';
  heroText.style.transform = 'translateY(0)';
}, 500);
