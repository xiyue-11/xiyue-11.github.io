document.addEventListener("DOMContentLoaded", () => {
  const links = Array.from(
    document.querySelectorAll("a.js-lightbox, .js-lightbox a")
  );

  if (!links.length) return;

  const overlay = document.createElement("div");
  overlay.className = "lightbox-overlay";
  overlay.innerHTML = `
    <div class="lightbox-backdrop"></div>
    <figure class="lightbox-figure">
      <img class="lightbox-image" alt="">
    </figure>
  `;

  document.body.appendChild(overlay);

  const img = overlay.querySelector(".lightbox-image");
  const figure = overlay.querySelector(".lightbox-figure");
  const backdrop = overlay.querySelector(".lightbox-backdrop");
  const TRANSITION_MS = 280;

  function open(src) {
    if (!src) return;
    overlay.classList.remove("is-closing");
    img.src = src;
    overlay.classList.add("is-open");
    document.body.classList.add("lightbox-open");
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        overlay.classList.add("is-visible");
      });
    });
  }

  function close() {
    if (!overlay.classList.contains("is-open")) return;
    overlay.classList.remove("is-visible");
    overlay.classList.add("is-closing");
    setTimeout(() => {
      overlay.classList.remove("is-open", "is-closing");
      document.body.classList.remove("lightbox-open");
      img.removeAttribute("src");
    }, TRANSITION_MS);
  }

  links.forEach((link) => {
    link.addEventListener("click", (e) => {
      const href = link.getAttribute("href");
      const src = link.dataset.src || href;
      if (!src) return;
      e.preventDefault();
      open(src);
    });
  });

  overlay.addEventListener("click", (e) => {
    if (e.target === backdrop || e.target === overlay || !figure.contains(e.target)) {
      close();
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") close();
  });
});

